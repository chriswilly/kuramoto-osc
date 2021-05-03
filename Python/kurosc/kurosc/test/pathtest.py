import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve().parents[2])
# rel imports when in package
if __name__ == '__main__' and __package__ is None:
    __package__ = 'kuosc'



print(Path(__file__).resolve())
print(__package__)

from kurosc.lib.plotformat import setup
