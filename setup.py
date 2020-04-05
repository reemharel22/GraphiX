from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

ext = Extension("GraphiX", sources=["GraphiX_contour.pyx"])
#setup(ext_modules=cythonize("GraphiX_contour.pyx"))
setup(ext_modules=[ext], cmdclass={'build_ext': build_ext})
