from setuptools import setup, find_packages

VERSION = '0.0.8'
DESCRIPTION = 'Backlink Builder'
LONG_DESCRIPTION = 'A free dofollow link builder for high DA sites.'

# Setup Parameters
setup(
    name="momoposter",
    version=VERSION,
    author="Momo Poster",
    author_email="<momo@cleardex.io>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['telegraph', 'spintax'],
    keywords=['python', 'backlink builder', 'seo', 'poster', 'link builder', 'momoposter'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)