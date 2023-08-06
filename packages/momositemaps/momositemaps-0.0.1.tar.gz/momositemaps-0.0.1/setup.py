from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Sitemap Builder'
LONG_DESCRIPTION = 'A free sitemap builder to handle millions of links.'

# Setup Parameters
setup(
    name="momositemaps",
    version=VERSION,
    author="Momo Sitemaps",
    author_email="<momo@cleardex.io>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['mysql-connector'],
    keywords=['python', 'sitemap builder', 'seo', 'sitemaps', 'link indexer'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)