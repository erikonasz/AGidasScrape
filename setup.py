from setuptools import setup, find_packages

setup(
    name='AGidasScraper',
    version='0.1',
    packages=['AGidasScraper'],
    install_requires=[
        'beautifulsoup4',
        'webdriver-manager',
        're',
        'csv'
    ],
    entry_points={
        'console_scripts': [
            'AGidasScraper = AGidasScraper.ascrape:main'
        ]
    }
)