import os

def makeapp(app_name):
    dirs = app_name.split('.')
    for i in range(len(dirs)):
        path = '/'.join(dirs[:i+1])
        if not os.path.exists(path):
            os.makedirs(path)

        with open(os.path.join(path, '__init__.py'), 'w') as f:
            pass
        with open(os.path.join(path, '__main__.py'), 'w') as f:
            pass
        with open(os.path.join(path, f'{dirs[i]}.py'), 'w') as f:
            pass
        with open(os.path.join(path, 'tests.py'), 'w') as f:
            pass