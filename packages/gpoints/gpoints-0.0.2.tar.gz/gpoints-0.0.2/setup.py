from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'From graph Image as input, get corresponding points'
LONG_DESCRIPTION = '4 argumnents: 1.Path to image 2.Range of horizontal value 3.Range of vertical value 4. 0/1'
# Setting up

setup(
    name="gpoints",
    version=VERSION,
    author="Ujjawal Kumar (India)",
    author_email="<kumarujjawal3621@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'points', 'stock price', 'Image', 'numpy array'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)