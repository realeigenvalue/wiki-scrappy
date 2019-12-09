import json

"""class for all the helper functions for the program
"""
class Helper(object):
    '''
    classdocs
    '''
        
    def __init__(self):
        '''
        Constructor
        '''
    
    """Given a json file extract and create a list of dictionaries
    """
    def load_structure(self, filename):
        with open(filename) as data_file:    
            data = json.load(data_file)
            #pprint(data)
            return data