from setuptools import find_packages, setup

setup(
    name="padme-conductor",
    version="0.1.9",
    description="A library which supports the creation of so-called Trains for the Personal Health Train infrastructure.",
    py_modules=["padme_conductor"],
    packages=find_packages(),
    author="Martin Goerz, Sascha Welten",
    author_email="welten@dbis.rwth-aachen.de",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sawelt/padme-conductor",
    include_package_data=True,
    classifiers=["Intended Audience :: Science/Research"],
    install_requires=["psycopg2", "fhirpy~=1.2.1"],
    keywords=["Personal Health Train", "PADME"],
)
