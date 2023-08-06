import os

def run_app(app_name=None, project_name=None):
    to_run = ""
    if app_name == None:
        to_run = project_name
    else:
        to_run = app_name

    return to_run