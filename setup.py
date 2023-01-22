from setuptools import setup, find_packages


setup(
    name='AGidasScraper',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'webdriver-manager',
    ],
    entry_points={
        'console_scripts': [
            'AGidasScraper = AGidasScraper.ascrape:main'
        ]
    },
    author = "erikonasz",
    author_email = "erikuzas123@gmail.com",
    description = "Autogidas scraper",
    url = "https://github.com/erikonasz/AGidasScrape"
)
