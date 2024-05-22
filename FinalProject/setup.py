from setuptools import Extension, setup

module = Extension("mysymnmf", sources=['symnmfmodule.c', 'symnmf.c', 'matrixmath.c'])
setup(name='mysymnmf',
      version='1.0',
      description= 'Python wrapper for C symnmf',
      ext_modules=[module])