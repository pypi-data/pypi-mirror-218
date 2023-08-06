import sys
import setuptools
#from setuptools import setup, Extension, Distribution
#from distutils import sysconfig
#import numpy

long_description="Liten AI"
with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = '0.0.6'
def get_version():
    return __version__

setuptools.setup(
    # This is the module name
    name='litenai',
    # This is the version of the module
    version=get_version(),
    # Name of Author
    author='HK Verma',
    # Author email address
    author_email='hkverma@litendata.com',
    # Small description
    description='Liten AI Data Platform',
    # Long description
    long_description=long_description,
    long_description_content_type='text/markdown',
    # URL for github
    # url='https://github.com/litenai/',
    # Find packages
    package_dir={'liten': 'liten','resources':'resources'},
    packages=['liten','resources'],
    include_package_data=True,
    package_data={
        "liten": ['*.pyc'],
        "resources" : ['*.ipynb'],
    },
    # Add all the packages required by liten
    install_requires = [
        'botocore',
        'boto3',
        'langchain',
       # 'minio',
        'openai',
        'pandas',
        'panel',
        'hvplot',
        'python-dotenv',
        'tiktoken'
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
