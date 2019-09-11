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
    install_requires=[
        'aiohttp==3.5.4',
        'tree-guardian==0.1.4-dev',
    ],
    scripts=[
        'bin/reminder-dev-server',
    ]
)
