from setuptools import setup


requires = ["requests>=2.14.2"]


setup(
    name='Reprypt',
    version='2.0.0',
    description='Encryption Module',
    url='https://github.com/tasuren/reprypt',
    author='tasuren',
    author_email='tasuren5@gmail.com',
    license='MIT',
    keywords='encrypt decrypt',
    packages=[
        "reprypt"
    ],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)