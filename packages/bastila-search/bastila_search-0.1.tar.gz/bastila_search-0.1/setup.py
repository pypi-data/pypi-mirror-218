from setuptools import setup

setup(
    name='bastila_search',
    version='0.1',
    description='A python script that catches commits that introduce predefined deprecated patterns',
    url='https://github.com/GetBastila/bastila-hook',
    author='Bastila',
    author_email='hello@bastila.app',
    license='MIT',
    packages=['bastila_search'],
    install_requires=[
        'requests',
    ],
    zip_safe=False
)
