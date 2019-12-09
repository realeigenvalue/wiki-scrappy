import unittest
import urllib2
import json

class Test(unittest.TestCase):
            
    def test_index(self):
        answer = "\"Welcome to Assignment2.1 Web API!\"\n"
        actual = urllib2.urlopen('http://127.0.0.1:5000/').read()
        self.assertEquals(answer, actual, 'index is wrong')
        
    def test1(self):
        answer = [{u'movies': [u'along came a spider', u'batman begins', u'bruce almighty', u'the big bounce', u'london has fallen', u'the dark knight', u'the bucket list', u'dreamcatcher', u'the dark knight rises', u'evan almighty', u'gone baby gone'], u'age': u'80', u'grossing': u'776711666.667', u'name': u'morgan freeman'}]
        actual = urllib2.urlopen('http://127.0.0.1:5000/actors?name=morgan%20freeman').read()
        actual = json.loads(actual)
        self.assertEquals(answer, actual, 'get is wrong')
    
    def test2(self):    
        answer = [{u'grossing': u'1085000000.0', u'release_date': u'2012-07-16', u'actors': [u'christian bale', u'michael caine', u'gary oldman', u'anne hathaway', u'tom hardy', u'marion cotillard', u'joseph gordon-levitt', u'morgan freeman'], u'name': u'the dark knight rises'}, {u'grossing': u'1005000000.0', u'release_date': u'2008-07-14', u'actors': [u'christian bale', u'michael caine', u'gary oldman', u'aaron eckhart', u'maggie gyllenhaal', u'morgan freeman'], u'name': u'the dark knight'}]
        actual = urllib2.urlopen('http://127.0.0.1:5000/movies?name=the%20dark%20knight').read()
        actual = json.loads(actual)
        self.assertEquals(answer, actual, 'get is wrong')
        
    def test3(self):
        answer = {u'movies': [u'the a-team', u'taken 3', u'the nut job', u'batman begins', u'non-stop', u'battleship', u'clash of the titans', u'the chronicles of narnia:\nthe lion, the witch, and the wardrobe', u'run all night', u'gun shy', u'the grey'], u'age': u'65', u'grossing': u'1005975000.0', u'name': u'liam neeson'}
        actual = urllib2.urlopen('http://127.0.0.1:5000/actors/liam%20neeson').read()
        actual = json.loads(actual)
        self.assertEquals(answer, actual, 'get is wrong')
        
    def test4(self):
        answer = {u'grossing': u'1005000000.0', u'release_date': u'2008-07-14', u'actors': [u'christian bale', u'michael caine', u'gary oldman', u'aaron eckhart', u'maggie gyllenhaal', u'morgan freeman'], u'name': u'the dark knight'}
        actual = urllib2.urlopen('http://127.0.0.1:5000/movies/the%20dark%20knight').read()
        actual = json.loads(actual)
        self.assertEquals(answer, actual, 'get is wrong')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()