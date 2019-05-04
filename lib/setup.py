from setuptools import setup, find_packages


setup(
    name='reminder',
    url='https://github.com/fadich/reminder',
    author='Fadi A.',
    author_email='royalfadich@gmail.com',
    version='0.1.0',
    description='Reminder chat utils',
    packages=find_packages(),
    zip_safe=False,
    requires=[
        'aiohttp',
    ]
)
