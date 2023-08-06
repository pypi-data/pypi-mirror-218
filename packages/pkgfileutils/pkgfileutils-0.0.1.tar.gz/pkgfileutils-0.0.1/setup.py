from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'DZ Python package'
LONG_DESCRIPTION = 'DZ Python package'

setup(
    name="pkgfileutils",
    version=VERSION,
    author="User",
    author_email="<youremail@email.com>",
    url="http://github.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'dz package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)