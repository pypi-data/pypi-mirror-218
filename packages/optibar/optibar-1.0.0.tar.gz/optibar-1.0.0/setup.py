from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.0'
DESCRIPTION = 'Make Advanced And Customizable ProgressBar'
ld = """# OptiBar 1.0.0
Make Advanced And Customizable ProgressBar
## Fast, Optimized And Professonial
Hello, welcome, the optibar module is very fast and allows
you to customize to some extent to create an advanced bar,
this website will teach you how you can create an advanced bar
with this module, of course this module for now Made for
pip users only"""
setup (
    name="optibar",
    version=VERSION,
    author="VenzTechnolo",
    author_email="venztechnolo@gmail.com",
    description=DESCRIPTION,
    long_description=ld,
    packages=find_packages(),
    py_modules=["colorama"],
    keywords=["python", "progress", "progressbar", "bar", "python3"],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta"
    ]
)