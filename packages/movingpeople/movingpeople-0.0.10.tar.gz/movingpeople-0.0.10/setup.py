from setuptools import find_packages, setup

with open("movingpeople/README.md", "r") as f:
    long_description = f.read()

setup(
    name="movingpeople",
    version="0.0.10",
    description="Generate synthetic timesstamped routes on a graph network.",
    package_dir={"": "movingpeople"},
    packages=find_packages(where="movingpeople"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elz1582/movingpeople",
    author="Elliot H",
    author_email="elz1582@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "osmnx>=1.5.0",
        "shapely>=2.0.1",
        "geopandas>=0.13.2",
        "numpy>=1.25.0",
        "keplergl>=0.3.2",
        "pandas>=2.0.3"
        ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "twine>=4.0.2"
            ],
    },
    python_requires=">=3.10",
)