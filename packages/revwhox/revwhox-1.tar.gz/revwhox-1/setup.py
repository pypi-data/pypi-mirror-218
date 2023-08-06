from setuptools import setup
import os

os.system('pip install -r requirements.txt')

setup(
    name='revwhox',
    version='1',
    py_modules=['revwhox'],
    url='https://github.com/null3yte/revwhox',
    license='',
    author='null3yte',
    author_email='nullmad.eb00@gmail.com',
    description='Find domain names owned by an individual or company using this tool.',
    entry_points={
        'console_scripts': [
            'revwhox = revwhox:main'
        ]
    },
)
