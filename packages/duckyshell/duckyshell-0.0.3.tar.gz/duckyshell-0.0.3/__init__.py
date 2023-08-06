from setuptools import setup

setup(
    name='duckyshell',
    version='0.0.3',
    description='Hak5 USB Rubber Ducky CLI',
    author='Daniel Boye',
    author_email='danielboye888@gmail.com',
    packages=['duckyshell'],
    entry_points={
        'console_scripts': [
            'duckyshell = main.py:main'
        ]
    },
)
