try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version
from pathlib import Path
import importlib.util
import zipfile
import pip
import os

try:
    import wget
except Exception as e:
    pip.main(['install', 'wget'])
    import wget

version_check_dict = {'ktrain' : '0.31.10',
                      'tensorflow' : '2.10.0',
                      'allennlp-models' : '2.10.0',
                      'allennlp' : '2.10.0',
                      'torch' : '1.11.0',
                      'torchtext':'0.5.0',
                      'nltk' : '3.7',
                      'opennmt-py' : '2.3.0',
                      'wget':'3.2',
                      'keras': '2.12.0',
                      'gensim': '4.2.0'}

def download_from_s3(CACHE_DIRECTORY, url_, extract_archive=False):
    """Download the model/data from web

    Args:
        CACHE_DIRECTORY (Path object): path of the directory where all the models 
                                  and supporting data is stored
        url_ (str): web URL from where the model/data is to be downloaded 
        extract_archive (boolean): to unzip the downloaded file
    """
    file = url_.split('/')[-1]
    if Path.exists(Path(CACHE_DIRECTORY)):
        
        if file in os.listdir(CACHE_DIRECTORY):
            return 
        else: 
            print('Downloading model' )
            _ = wget.download(url_, out = str(CACHE_DIRECTORY))
            
            if extract_archive:
                path_to_zip_file = CACHE_DIRECTORY /  file
                with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                    zip_ref.extractall(CACHE_DIRECTORY)
    else:
        os.makedirs(CACHE_DIRECTORY)
        print('Downloading model' )
        _ = wget.download(url_, out = str(CACHE_DIRECTORY))

        if extract_archive:
            path_to_zip_file = CACHE_DIRECTORY / file
            with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                zip_ref.extractall(CACHE_DIRECTORY)
    
    return 


def install(package):
    """install a python package

    Args:
        package (str): _package name
    """
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

def check_version(package_name):
    """check if the desired package version is in the envirnment

    Args:
        package_name (str): package name for which the version is to be checked

    Returns:
        boolean: True: if the package is found with the desired version
                 else: False       
    """
    desired_version = version_check_dict[package_name]
    if version(package_name) == desired_version:
        return True
    else:
        return False
    
def check_and_install(package_name):
    """check if the desired package version is in the envirnment.
    if not foung=d this function will install that package.

    Args:
        package_name (str):package name that needs to be isntalled

    Returns:
        boolean: True: if the package is installed properly
    """
    version = version_check_dict[package_name]
    if importlib.util.find_spec(package_name) is None:
        print(package_name +" is not installed")
        install(package_name + '==' + version)
        return True
    else:
        if not check_version(package_name):
            print('package found but not right version')
            install(package_name + '==' + version)
            return True
        else:
            return True
