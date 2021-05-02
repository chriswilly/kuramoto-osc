from setuptools import setup
__version__ = None
exec(open('kuramotoNeighbor/version.py').read())


setup(name='kuramotoNeighbor',  # 'kuramotoNeighbor'
      version=__version__,
      description='AMATH 575 project on weakly coupled phase synchonous oscillators\
                   with distance delay and decay and second order interrupting interactions',
      url='https://github.com/chriswilly/kuramoto-osc',
      author=['Michael Willy',
              'Tomek Fraczek',
              'Yundong Lin',
              'Blake Fletcher'],
      author_email=['michael  willy at gmail dot com','add yours here'],
      license='MIT',
      packages=['kuramotoNeighbor'],
      zip_safe=False
      )
