from multiprocessing import Process

import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve())
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kurosc'


from main import run

# def run(set:str = 'global_sync',
#         config_file:str = 'model_config.json'):

sets = ('local_sync','global_sync','test_set0')

processes = []

for s in sets:
   p = Process(target=run, args=(s,))
   p.start()
   processes.append(p)
#
# for p in processes:
#    p.join()
