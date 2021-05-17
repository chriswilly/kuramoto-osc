from multiprocessing import Process

import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve())
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kurosc'


from main import run

# def run(set:str = 'global_sync',
#         config_file:str = 'model_config.json'):




if __name__=='__main__':
    sets = ('test_set0','test_set1','test_set2')

    processes = []

    for s in sets:
       p = Process(target=run, args=(s,))
       p.start()
       p.join()
       processes.append(p)
