import configparser

def run_app(app_name=None):
    to_run = ""
    if app_name == None:
        config = configparser.ConfigParser()
        config.read('swiftly.config.py')
        project_name = config.get('DEFAULT', 'PROJECT_NAME')
        to_run = project_name
        
    else:
        to_run = app_name
    
    return to_run
