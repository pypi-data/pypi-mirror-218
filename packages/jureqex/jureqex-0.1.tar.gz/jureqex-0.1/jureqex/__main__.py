import argparse
import os

from .requirement_extractor import extract_requirements, compare_with_freeze

def main():
    """
    Extracts requirements from a Jupyter notebook file and takes the versions 
    from the installed packages.
    
    :return: None
    """
    parser = argparse.ArgumentParser(prog ='jureqex',
                                     description="Extracts requirements from a Jupyter notebook \
                                                 file and takes the versions from the installed packages.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--path", help="Path to the folder where the Jupyter notebook is", required=True)
    parser.add_argument("--name", help="Name of the Jupyter notebook", required=True)
    parser.add_argument("--save", help="Path with the name where the requirements are going to be saved", required=True)
    args = vars(parser.parse_args())
    
    path_requiremts =  os.path.join(args["save"])
    nb_path = os.path.join(args["path"], args["name"])

    notebook_requiremts = extract_requirements(nb_path)

    req_directory, req_name = os.path.split(path_requiremts)
    path_notebook_requirements = os.path.join(req_directory, 'notebook_'+req_name)

    file=open(path_notebook_requirements,'w')
    file.writelines(f'# Requirements for {args["name"]}\n')
    for item in sorted(notebook_requiremts):
        file.writelines(item + '\n')
    file.close()

    requiremts = compare_with_freeze(nb_path)

    file=open(path_requiremts,'w')
    file.writelines(f'# Requirements for {args["name"]}\n')
    for item in sorted(requiremts):
        file.writelines(item + '\n')
    file.close()    

if __name__ == "__main__":
    main()
    
