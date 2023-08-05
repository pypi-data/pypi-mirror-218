# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 12:15:45 2023

@author: Franco, Bruno Agustín 

"""

### AGREGAR RELATIVE IMPORTS

### OCULTAR TRAZABILIDAD DEL TRAINING

from setuptools import setup, find_namespace_packages

with open('README.md') as file:         #sirve para incluir el REEDME
    long_description = file.read()

short_description = 'A tool to simplify your DP4+ calculations'

setup(
    name='dp4plus_app',
    version='0.1.12',
    
    author='Bruno A. Franco',
    author_email='bruno.agustin.franco@gmail.com',
    url='https://github.com/RosarioCCLab/DP4plus-App',
    description =short_description	,
    long_description = long_description,
    long_description_content_type ="text/markdown",
    license ='MIT',
    
    python_requires=">=3.8",
    
    install_requires=[
                    'requests',
                    'importlib-metadata; python_version == "3.8"',
                    'numpy', 
                    'openpyxl', 
                    'xlsxwriter',
                    'pandas',
                    'pathlib', 
                    'scikit-learn', 
                    'scipy', 
                    'tk',
                    'Pillow',
                    'odfpy'],
    
    entry_points={ 'gui_scripts': ['dp4plus = dp4plus_app.main:main'],
                    'console_scripts':['dp4plus-exe = dp4plus_app.main:create_exe'],},
                 
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "dp4plus_app" : ["*"],
        "dp4plus_app.nmr_examples" : ["*"],
        "dp4plus_app.UserGuide" : ["*"],
        "dp4plus_app.nmr_custom": ["*"],
        "dp4plus_app.nmr_custom.opt_B3LYP": ["*"],
        "dp4plus_app.nmr_custom.opt_MMFF": ["*"], },
    
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    keywords = 'nmr', 
     
)