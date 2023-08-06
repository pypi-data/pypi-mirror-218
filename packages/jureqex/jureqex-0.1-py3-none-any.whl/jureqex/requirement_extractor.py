import argparse
import os
import re

import nbformat

from yarg import json2package
from yarg.exceptions import HTTPError
import requests
import logging

def requiremts_from_code(code):
    """
    Extracts the required libraries and modules from the given code.

    Parameters:
    - code (str): The code from which the required libraries and modules are to be extracted.

    Returns:
    - List[str]: A list of required libraries and modules extracted from the code.
    """
    # Finds in the code the import library names
    import_pattern = r'^\s*(import|from)\s+(\w+)'
    imports = re.findall(import_pattern, code, re.MULTILINE)
    imports = [library[-1] for library in imports if library]

    # Finds in the code the installed libraries with 'pip install'   
    installation_pattern =  r'pip\s+install\s+(-[^\s]+\s+)?["\']?([^<>=\s]+)'
    installations = re.findall(installation_pattern, code, re.MULTILINE)
    installations = [library[-1] for library in installations if library]

    # Finds in the code the libraries that have been loaded with '%load' (colab magic command)
    load_pattern =  r'%load\s+(\w+)'
    loads = re.findall(load_pattern, code, re.MULTILINE)
    loads = [library[-1] for library in loads if library]

    return imports + installations + loads

def fix_requiremts(requiremts):
    """
    Fix the given list of requirements. Some of the libraries have different
    names when are imported than when they are installed, therefore we need to
    fix them.

    Parameters:
        requiremts (list): A list of requirements to be fixed.

    Returns:
        list: A list of fixed requirements.
    """
    fixed_requirements = []
    for r in requiremts:
        if r == 'sklearn':
            fixed_requirements.append('scikit-learn')
        elif r == 'skimage':
            fixed_requirements.append('scikit-image')
        elif r == 'PIL':
            fixed_requirements.append('Pillow')
        elif r == '__future__':
            fixed_requirements.append('future')
        elif r == 'memory_profiler':
            fixed_requirements.append('memory-profiler')
        else:
            fixed_requirements.append(r)

    return fixed_requirements

def extract_requirements(path_nb):
    """
    Extracts requirements from a Jupyter notebook file.

    Args:
        path_nb (str): The path to the Jupyter notebook file.

    Returns:
        list: A list of unique requirements extracted from the notebook.
    """
    colab_nb = nbformat.read(path_nb, as_version=4)

    requiremts = []
    for cell in colab_nb.cells:
        if cell.cell_type == "code":
            code = cell.source
            cell_requirements = requiremts_from_code(code)
            requiremts += cell_requirements
        elif cell.cell_type == "markdown":
            pass
    
    requiremts = list(set(requiremts))
    requiremts = fix_requiremts(requiremts)
    
    return requiremts
    
def compare_with_freeze(path_nb, requirement_list=[]):
    """
    Compare the requirements of a Jupyter notebook with the installed packages.
    
    Parameters:
        path_nb (str): The path to the Jupyter notebook file.
        requirement_list (list, optional): A list of required packages to compare with. Defaults to an empty list.
    
    Returns:
        list: A list of required packages with their corresponding versions.
    """
    # First of all, the requirements from the notebook have to be loaded
    requirements = requirement_list if requirement_list else extract_requirements(path_nb)
    
    # Then, the requirements from 'pip freeze' are loaded
    try: from pip._internal.operations import freeze
    except ImportError: # pip < 10.0
        from pip.operations import freeze
    pkgs = freeze.freeze()

    # We save the libraries and their versions in a dictionary
    libraries_with_version = {}
    for pkg in pkgs: 
        if '@' in pkg:
            # Means that the library is in a local file
            continue
        elif '==' in pkg:
            library = pkg.split('==')[0]
            version = pkg.split('==')[1]
            libraries_with_version[library] = version
        else:
            print(pkg)
            raise Exception("Wrong library name.")
        
    # Then, we compare the requirements from the notebook with the ones from 'pip freeze'
    requirements_with_version = []
    for req in requirements:
        if req in list(libraries_with_version.keys()):
            version = libraries_with_version[req]

            # Following code is taken form https://github.com/bndr/pipreqs/blob/a1f83d27d9a42aa95b481e2fa94716702266110c/pipreqs/pipreqs.py#L173C5-L173C21
            # In case the version obtained from 'pip freeze' is not available in Pypi, we use the latest version
            try:
                response = requests.get(
                    "{0}{1}/json".format("https://pypi.python.org/pypi/", req), proxies=None)
                if response.status_code == 200:
                    if hasattr(response.content, 'decode'):
                        data = json2package(response.content.decode())
                    else:
                        data = json2package(response.content)
                elif response.status_code >= 300:
                    raise HTTPError(status_code=response.status_code,
                                    reason=response.reason)
            except HTTPError:
                logging.warning(
                    'Package "%s" does not exist or network problems', item)
                continue

            if version in data._releases.keys() and req!="ipywidgets":  
                actual_version = version
            else:
                actual_version = data.latest_release_id

            requirements_with_version.append(f'{req}=={actual_version}')

    return requirements_with_version
