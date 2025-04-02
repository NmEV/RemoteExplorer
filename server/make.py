import pickle
from plg_def import plugin

with open('protect.pkl', 'wb') as f:
    pickle.dump(plugin, f)
