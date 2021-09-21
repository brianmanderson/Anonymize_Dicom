__author__ = 'Brian M Anderson'
# Created on 9/15/2020


from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='PlotScrollNumpyArrays',
    author='Brian Mark Anderson',
    author_email='b5anderson@health.ucsd.edu',
    version='0.0.1',
    description='Tools for plotting NumPy arrays, typically from DICOM and including overlap of dose/mask',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'AnonymizeDicom': 'src/AnonymizeDicom'},
    packages=['AnonymizeDicom'],
    include_package_data=True,
    url='https://github.com/brianmanderson/Plot_And_Scroll_Images',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
    install_requires=required,
)
