import scrapy.cmdline
import graph as g
import helper as hl
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter

    
def main():
    #scrapy.cmdline.execute(argv=['scrapy', 'runspider', 'wikipedia.py', '-o', 'data.json'])
    graph = g.Graph(hl.Helper().load_structure('data.json'))
    test_console_output(graph)
    hub_actors(graph, 4)
    age_money(graph)
    
    
def hub_actors(graph, number):
    hubs = graph.top_x_hub_actors(number)
    subgraph = {}
    for hub in hubs:
        subgraph[hub] = graph.get_connections()[hub]
    G=nx.from_dict_of_lists(subgraph)
    nx.draw(G, with_labels=True)
    plt.show()
    """answer top 4 = [u'james marsden', u'liam neeson', u'morgan freeman', u'steve carell']
    """
    
def age_money(graph):
    age_vs_money = []    
    for item in graph.age_vs_money():
        age_vs_money.append((item[0], item[1]))
    age_vs_money = sorted(age_vs_money,key=itemgetter(0))
    
    ages = [item[0] for item in age_vs_money]
    values = [item[1] for item in age_vs_money]
    
    grossing = []
    grossing.append(sum([values[i] for i in range(len(ages)) if ages[i] < 12]))
    grossing.append(sum([values[i] for i in range(len(ages)) if (12 <= ages[i]) and (ages[i] <= 17)]))
    grossing.append(sum([values[i] for i in range(len(ages)) if (18 <= ages[i]) and (ages[i] <= 24)]))
    grossing.append(sum([values[i] for i in range(len(ages)) if (25 <= ages[i]) and (ages[i] <= 34)]))
    grossing.append(sum([values[i] for i in range(len(ages)) if (35 <= ages[i]) and (ages[i] <= 44)]))
    grossing.append(sum([values[i] for i in range(len(ages)) if (45 <= ages[i]) and (ages[i] <= 54)]))
    grossing.append(sum([values[i] for i in range(len(ages)) if (55 <= ages[i]) and (ages[i] <= 64)]))
    grossing.append(sum([values[i] for i in range(len(ages)) if 65 < ages[i]]))
    
    objects = ('Under 12', '12-17', '18-24', '25-34', '35-44', '45-54', '55-64', 'Over 65')
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, grossing, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.xlabel('age group')
    plt.ylabel('grossing')
    plt.title('age vs grossing')
    plt.show()
    """age group 45-54 generated most amount of money, middle aged actors
    generated more money than young and old actors
    """
    
def test_console_output(graph):
    
    """Console output from program
    """
    
    print('number of movies and actors:')
    pprint((graph.get_number_of_movies(), graph.get_number_of_actors()))
    
    print('movie grossing output:')
    pprint(graph.movie_grossing('10,000 bc'))
    
    print('movie worked in output:')
    pprint(graph.movies_worked_in('liam neeson'))
    
    print('actors in movie output:')
    pprint(graph.actors_in_movie('batman begins'))
    
    print('top actors output:')
    pprint(graph.top_x_actors(10))
    
    print('oldest actors output:')
    pprint(graph.oldest_x_actors(10))
    
    print('movies given year output:')
    pprint(graph.movies_given_year(2016))
    
    print('actors given year output:')
    pprint(graph.actors_given_year(2016))
    
if  __name__ =='__main__':
    main()