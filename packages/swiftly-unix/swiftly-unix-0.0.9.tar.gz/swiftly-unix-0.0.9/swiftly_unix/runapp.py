import os

def run_app(app_name=None, project_name=None, venv_location=None):
    to_run = ""
    if app_name == None:
        to_run = project_name
    else:
        to_run = app_name

    if not to_run.startswith("."):
        venv_dir = os.path.dirname(venv_location)
        to_run = os.path.join(venv_dir, to_run)

    return to_run