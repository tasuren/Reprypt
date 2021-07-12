from setuptools import setup
from os.path import exists


if exists("README.md"):
    with open("README.md", "r") as f:
        long_description = f.read()


requires = []


setup(
    name='Reprypt',
    version='2.1.1',
    description='Encryption Module',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tasuren/reprypt',
    author='tasuren',
    author_email='tasuren5@gmail.com',
    license='MIT',
    keywords='encrypt decrypt encryption',
    packages=[
        "reprypt"
    ],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
