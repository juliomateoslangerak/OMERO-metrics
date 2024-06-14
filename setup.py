from setuptools import find_packages, setup

setup(
    name="omero-metrics",
    version="0.1.0",
    description="A webapp to follow microscope performance over time",
    packages=find_packages(),
    keywords=["omero"],
    install_requires=[
        "django-plotly-dash",
        "dpd_static_support",
        "dash-bootstrap-components",
        "django-bootstrap4",
        "dash_mantine_components",
        "dash-iconify",
        "omero-py==5.19.2",
        "microscopemetrics_schema @ git+https://github.com/juliomateoslangerak/microscopemetrics-schema.git@dev",
    ],
)
