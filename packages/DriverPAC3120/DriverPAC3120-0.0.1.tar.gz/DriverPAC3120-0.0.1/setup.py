import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1' 
PACKAGE_NAME = 'DriverPAC3120' #Debe coincidir con el nombre de la carpeta 
AUTHOR = 'Cristian Arias' 
AUTHOR_EMAIL = 'c.arias4p@gmail.com' 
URL = '' 

LICENSE = 'MIT' 
DESCRIPTION = 'Driver PAC3120'
LONG_DESCRIPTION = 'Driver PAC3120 para prueba'
LONG_DESC_TYPE = "text/markdown"



INSTALL_REQUIRES = [
      'pymupdf'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)