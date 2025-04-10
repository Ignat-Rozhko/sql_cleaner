from setuptools import setup, find_packages

setup(
    name="sql_cleaner",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sql_cleaner=sql_cleaner.cli:main',
        ],
    },
    python_requires='>=3.6',
    description="A tool for cleaning SQL files by removing specific table inserts and references",
    author="Ignat Rozhko",
) 