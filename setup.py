"""setuptools"""
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()


setup(
    name='one-expense-tracker',
    version='0.0.1',
    author='Onyeka Emmanuel Nwizu',
    author_email='nwizuemmanuel200@gmail.com',
    description='A cli app for expense tracking',
    long_description=long_description,
    url='https://github.com/NwizuEmmanuel/expense-tracker',
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'one-ex-tracker = expense_tracker.main:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
