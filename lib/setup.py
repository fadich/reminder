from setuptools import setup, find_packages


setup(
    name='reminder',
    version='0.1.0',
    description='Reminder chat utils',
    packages=find_packages(),
    requires=[
        'aiohttp',
    ]
)
