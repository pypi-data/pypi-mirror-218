import os
import subprocess
import configparser
from swiftly_unix.makeapp import makeapp
from swiftly_unix.gitignore import GITIGNORE

def get_venv_location():
    config = configparser.ConfigParser()
    config.read('swiftly.config.py')
    project_name = config.get('DEFAULT', 'PROJECT_NAME')

    venv_name = f'venv{project_name}'
    venv_exists = os.path.exists(venv_name)

    if not venv_exists:
        subprocess.run(['python3', '-m', 'venv', venv_name])

        # Add the virtual environment to the .gitignore file
        if not os.path.exists('.gitignore'):
            with open('.gitignore', 'w') as f:
                f.write(GITIGNORE)
        with open('.gitignore', 'a') as f:
            f.write(f'\n{venv_name}/')

    venv_location = os.path.abspath(venv_name)
    return venv_location



def pull_changes(git_status):
    not_to_pull = ["fatal: not a git repository", "Your branch is up to date with"]
    
    for i, message in enumerate(not_to_pull):
        not_to_pull[i] = message in git_status
        
    return not (False in not_to_pull)

def check_new_packages(available_packages):
    with open('requirements.txt', 'r') as f:
        required_packages = f.read().splitlines()

    available_packages = set(available_packages.split())
    required_packages = set(required_packages)

    return not required_packages.issubset(available_packages)

def is_repo(name):
    repo_markers = ["https://", "http://", ".git", "git@"]
    
    repo_check = [marker in name for marker in repo_markers]
    return True in repo_check

def initialise(name):
    if is_repo(name):
        name = name.split('/')[-1].replace('.git', '')

    if not os.path.exists(name):
        os.makedirs(name)
    os.chdir(name)

    if not os.path.exists('requirements.txt'):
        with open('requirements.txt', 'w') as f:
            pass

    if not os.path.exists('swiftly.config.py'):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'PROJECT_NAME': name}
        with open('swiftly.config.py', 'w') as f:
            config.write(f)

    makeapp(name)
    venv_location = get_venv_location()

    return venv_location
