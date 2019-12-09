from operator import itemgetter
from networkx.classes import graph
from astroid.protocols import objects
from pprint import pprint

class Graph(object):
    '''
    classdocs
    '''
    dictionary = {}
    
    """Dictionary to hold actor connections for hub actors
    """
    connections = {}
    
    def __init__(self, dictionary=None):
        if dictionary != None:
            self.update_dictionary(dictionary)
    
    """Updates the graph given a dictionary, duplicate values not allowed
    """
    def update_dictionary(self, dictionary):
        for movie in dictionary:
            movie_name = movie['movie_name']
            release_date = movie['release_date']
            grossing = movie['grossing']
            actors = movie['actors']
            if self.dictionary.has_key(movie_name) == False:
                self.dictionary[movie_name] = [(release_date, grossing)]
            for actor in actors:
                actor_name = actor[0]
                actor_age = actor[1]
                if self.dictionary.has_key(actor_name) == False:
                    self.dictionary[actor_name] = [(actor_age,)]
            self.update_edges(movie_name, actors)
            
            """Hub actor graph construction 
            """
            for actor1 in actors:
                actor1_name = actor1[0]
                if self.connections.has_key(actor1_name) == False:
                    self.connections[actor1_name] = []
                for actor2 in actors:
                    if actor1 != actor2:
                        actor2_name = actor2[0]
                        if actor2_name not in self.connections[actor1_name]:
                            self.connections[actor1_name].append(actor2_name)
    
    """Gets all of the vertices key from the dictionary from the graph
    """
    def get_vertices(self):
        return list(self.dictionary.keys())
    
    """Gets the number of movie vertices
    """
    def get_number_of_movies(self):
        result = 0
        for key in self.dictionary.keys():
            if len(self.dictionary[key][0]) == 2:
                result += 1
        return result
    
    """Gets the number of actor vertices
    """
    def get_number_of_actors(self):
        result = 0
        for key in self.dictionary.keys():
            if len(self.dictionary[key][0]) == 1:
                result += 1
        return result
    
    """Updates the neighbor list for each vertex, helper function to update_dictionary
    """
    def update_edges(self, movie_name, actors):
        i = 1
        for actor in actors:
            actor_name = actor[0]
            actor_age = actor[1]
            
            grossing = self.dictionary[movie_name][0][1]

            weight = float(grossing) / i
            
            self.dictionary[movie_name].append((actor_name, weight))
            self.dictionary[actor_name].append((movie_name, weight))
            
            movie_neighbor = []
            for item in self.dictionary[movie_name]:
                if item not in movie_neighbor:
                    movie_neighbor.append(item)
            self.dictionary[movie_name] = movie_neighbor
            
            actor_neighbor = []
            for item in self.dictionary[actor_name]:
                if item not in actor_neighbor:
                    actor_neighbor.append(item)
            self.dictionary[actor_name] = actor_neighbor
            
            i = i + 1
    
    """Gets the dictionary behind the graph useful for testing
    """
    def get_graph(self):
        return self.dictionary
    
    """Gets the dictionary behind the connections useful for hub actors
    """
    def get_connections(self):
        return self.connections
    
    """Give a movie and get how much it made as a float
    """
    def movie_grossing(self, movie_name):
        if self.dictionary.has_key(movie_name):
            return float(self.dictionary[movie_name][0][1])
        return -1
    
    """Give an actor get all the movies the actor worked in
    """
    def movies_worked_in(self, actor_name):
        if self.dictionary.has_key(actor_name):
            result = []
            edges = self.dictionary[actor_name]
            for i in range(1, len(edges)):
                result.append(edges[i][0])
            return result
        return -1
    
    """Give a movie get all the actors that worked in this movie
    """
    def actors_in_movie(self, movie_name):
        if self.dictionary.has_key(movie_name):
            result = []
            edges = self.dictionary[movie_name]
            for i in range(1, len(edges)):
                result.append(edges[i][0])
            return result
        return -1
    
    """Give number of top actors by [value = total of weights for each actor]
    If the number given is too big we return as much as we can
    """
    def top_x_actors(self, number):
        result = []
        for key in self.dictionary.keys():
            if len(self.dictionary[key][0]) == 1:
                result.append((key, self.calculate_value(key)))                
        result = sorted(result,key=itemgetter(1),reverse=True)
        ret = []
        if(number > len(result)):
            for item in result:
                ret.append(item[0])
            return ret
        for item in result[0:number]:
            ret.append(item[0])
        return ret
    
    """Calculates the value of an actor as sum of weights of edges incident to actor
    """
    def calculate_value(self, actor_name):
        if self.dictionary.has_key(actor_name):
            value = 0
            edges = self.dictionary[actor_name]
            for i in range(1, len(edges)):
                value += float(edges[i][1])
            return value
        return -1
    
    """Gets the top oldest actors
    If the number given is too big we return as much as we can
    """
    def oldest_x_actors(self, number):
        result = []
        for key in self.dictionary.keys():
            if len(self.dictionary[key][0]) == 1:
                result.append((key, int(self.dictionary[key][0][0])))
        result = sorted(result,key=itemgetter(1),reverse=True)
        ret = []
        if(number > len(result)):
            for item in result:
                ret.append(item[0])
            return ret
        for item in result[0:number]:
            ret.append(item[0])
        return ret
    
    """Get all the movies that was released in the given year
    """
    def movies_given_year(self, year):
        result = []
        for key in self.dictionary.keys():
            if len(self.dictionary[key][0]) == 2:
                the_year = int(self.dictionary[key][0][0].split('-')[0])
                if the_year == year:
                    #result.append((key, year))
                    result.append(key)
        return result
    
    """Get all the actors that acted in the given year by scanning the list of
    neighbors for each actor
    """
    def actors_given_year(self, year):
        result = []
        for key in self.dictionary.keys():
            if len(self.dictionary[key][0]) == 1:
                edges = self.dictionary[key]
                for i in range(1, len(edges)):
                    the_year = int(self.dictionary[edges[i][0]][0][0].split('-')[0])
                    if the_year == year:
                        #result.append((key, the_year))
                        result.append(key)
                        break
        return result
    
    """Gets the top hub actors
    If the number given is too big we return as much as we can
    """
    def top_x_hub_actors(self, number):
        result = []
        for key in self.connections.keys():
            result.append((key, len(self.connections[key])))
        result = sorted(result,key=itemgetter(1),reverse=True)
        ret = []
        if(number > len(result)):
            for item in result:
                ret.append(item[0])
            return ret
        for item in result[0:number]:
            ret.append(item[0])
        return ret
    
    """Constructs age vs money tuple for each actor in the graph
    """
    def age_vs_money(self):
        result = []
        for key in self.dictionary.keys():
            if len(self.dictionary[key][0]) == 1:
                actor_age = int(self.dictionary[key][0][0])
                actor_value = self.calculate_value(key)
                result.append((actor_age, actor_value))
        return result
    
    """Get an actor as an dictionary object given name
    """
    def get_actor_object(self, actor_name):
        if self.dictionary.has_key(actor_name) == True and len(self.dictionary[actor_name][0]) == 1:
            name = actor_name
            age = self.dictionary[actor_name][0][0]
            grossing = str(self.calculate_value(actor_name))
            temp = self.dictionary[actor_name][1:]
            movies = []
            for movie in temp:
                movies.append(movie[0])
            return {'name': name, 'age': age, 'grossing': grossing, 'movies': movies}
        return -1
    
    """Get an movie as an dictionary object given movie name
    """
    def get_movie_object(self, movie_name):
        if self.dictionary.has_key(movie_name) == True and len(self.dictionary[movie_name][0]) == 2:
            name = movie_name
            release_date = self.dictionary[movie_name][0][0]
            grossing = self.dictionary[movie_name][0][1]
            temp = self.dictionary[movie_name][1:]
            actors = []
            for actor in temp:
                actors.append(actor[0])
            return {'name': name, 'release_date': release_date, 'grossing': grossing, 'actors': actors}
        return -1
    
    """Get all actors as actor objects as a list
    """
    def get_all_actors(self):
        result = []
        for key in self.dictionary.keys():
            if len(self.dictionary[key][0]) == 1:
                result.append(self.get_actor_object(key))
        return result
    
    """Get all movies as movie objects as a list
    """
    def get_all_movies(self):
        result = []
        for key in self.dictionary.keys():
            if len(self.dictionary[key][0]) == 2:
                result.append(self.get_movie_object(key))
        return result
    
    """Filters out actors that do not meet given attribute as a set
    """
    def filter_actors(self, attr, attr_value):
        result = []
        for actor in self.get_all_actors():
            include = False
            if attr == 'name':
                if attr_value in actor[attr]:
                    include = True
            elif attr == 'age' or attr == 'grossing':
                if actor[attr] == attr_value:
                    include = True
            elif attr == 'movies':
                for actors_movie in actor[attr]:
                    for movie in attr_value:    
                        if movie in actors_movie:
                            include = True
                            break
            else:
                include = False
            if include == True:
                result.append(actor)
        return result
    
    """Filters out movies that do not meet given attribute as a set
    """
    def filter_movies(self, attr, attr_value):
        result = []
        for movie in self.get_all_movies():
            include = False
            if attr == 'name' or attr == 'release_date':
                if attr_value in movie[attr]:
                    include = True
            elif attr == 'grossing':
                if movie[attr] == attr_value:
                    include = True
            elif attr == 'actors':
                for movie_actors in movie[attr]:
                    for actor in attr_value:
                        if actor in movie_actors:
                            include = True
                            break
            else:
                include = False
            if include == True:
                result.append(movie)
        return result