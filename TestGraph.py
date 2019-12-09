import unittest
from app import graph as g
from app import helper

class Test(unittest.TestCase):
    
    def test_movie_grossing(self):
        test_dictionary = helper.Helper().load_structure('test.json')
        graph = g.Graph(test_dictionary)
        answer = 52100000.0
        actual = graph.movie_grossing('the finest hours')
        self.assertEqual(answer, actual, 'movie grossing is wrong')
    
    def test_movies_worked_in(self):
        test_dictionary = helper.Helper().load_structure('test.json')
        graph = g.Graph(test_dictionary)
        answer = [u'zoolander 2']
        actual = graph.movies_worked_in('owen wilson')
        self.assertEqual(answer, actual, 'movies actor worked is wrong')
    
    def test_actors_in_movie(self):
        test_dictionary = helper.Helper().load_structure('test.json')
        graph = g.Graph(test_dictionary)
        answer = [u'chris pine', u'casey affleck', u'ben foster', u'holliday grainger', u'john ortiz', u'eric bana']
        actual = graph.actors_in_movie('the finest hours') 
        self.assertEqual(answer, actual, 'actors in movie is wrong')
    
    def test_top_x_actors(self):
        test_dictionary = helper.Helper().load_structure('test.json')
        graph = g.Graph(test_dictionary)
        answer = [u'dakota johnson', u'chlo grace moretz', u'owen wilson']
        actual = graph.top_x_actors(3)
        self.assertEqual(answer, actual, 'top actors is wrong')
    
    def test_calculate_value(self):
        test_dictionary = helper.Helper().load_structure('test.json')
        graph = g.Graph(test_dictionary)
        answer = 56700000.0
        actual = graph.calculate_value('owen wilson')
        self.assertEqual(answer, actual, 'calculate value is wrong')
    
    def test_oldest_x_actors(self):
        test_dictionary = helper.Helper().load_structure('test.json')
        graph = g.Graph(test_dictionary)
        answer = [u'fred willard', u'charles dance', u'jeremy irons']
        actual = graph.oldest_x_actors(3)
        self.assertEqual(answer, actual, 'oldest actors is wrong')
    
    def test_movies_given_year(self):
        test_dictionary = helper.Helper().load_structure('test.json')
        graph = g.Graph(test_dictionary)
        answer = [u'the benefactor']
        actual = graph.movies_given_year(2015)
        self.assertEqual(answer, actual, 'movies given year is wrong')
    
    def test_actors_given_year(self):
        test_dictionary = helper.Helper().load_structure('test.json')
        graph = g.Graph(test_dictionary)
        answer = [u'dakota fanning', u'richard gere', u'theo james', u'clarke peters']
        actual = graph.actors_given_year(2015)
        self.assertEqual(answer, actual, 'actors given year is wrong')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()