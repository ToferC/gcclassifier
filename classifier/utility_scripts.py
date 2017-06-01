# utility scripts

import pickle
import os

data_path = '/home/chris/data/'
output_path = '/home/chris/data/'

def save_obj(obj, name):
    with open(os.path.join(data_path, "{}.pkl".format(name)), 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name):
    with open(os.path.join(data_path, "{}.pkl".format(name)), 'rb') as f:
        return(pickle.load(f))