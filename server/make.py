import pickle
from plg_def import plugin

with open('p1.pkl', 'wb') as f:
    pickle.dump(plugin, f)