from setuptools import find_packages, setup

setup(
    name="omero-metrics",
    version="0.1.0",
    description="A webapp to follow microscope performance over time",
    packages=find_packages(),
    keywords=["omero"],
    install_requires=[
        "pandas"
        "microscopemetrics_schema @ git+https://github.com/juliomateoslangerak/microscopemetrics-schema.git@dev",
    ],
)
