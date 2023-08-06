# setup.py
from setuptools import setup, find_packages

setup(
    name='murkrow',
    version='0.14.0',
    description='Install chatlab instead!',
    author='Kyle Kelley',
    author_email='rgbkrk@gmail.com',
    url='https://github.com/rgbkrk/chatlab',
    packages=find_packages(),
    install_requires=[
        'chatlab',
    ],
)

