from Cython.Build import cythonize
import setuptools

extensions = [setuptools.Extension("superpang.lib.Compressor", sources=["src/superpang/lib/Compressor.pyx"]),
              setuptools.Extension("superpang.lib.cutils", sources=["src/superpang/lib/cutils.pyx"]),
              setuptools.Extension("superpang.lib.vtools", sources=["src/superpang/lib/vtools.pyx"])]

setuptools.setup(
    ext_modules = cythonize(extensions),
    setup_requires = ['cython']
    )


# pushing stuff to pip :
# rm -r build/* dist/* SuperPang.egg-info/ SuperPang/lib/*c SuperPang/lib/*so
# python3 setup.py sdist --cythonize
# python3 -m twine upload --repository pypi dist/*
# rm -r dist/* SuperPang.egg-info/ SuperPang/lib/*c
