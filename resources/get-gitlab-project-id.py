import gitlab
from envparse import env

GITLAB_URL = env('GITLAB_URL')
GITLAB_TOKEN = env('GITLAB_TOKEN')
GITLAB_PROJECT = env('GITLAB_PROJECT')

gl = gitlab.Gitlab(GITLAB_URL, GITLAB_TOKEN)

def get_id():
    project = gl.projects.get(GITLAB_PROJECT)
    print(project.id)

def main():
    get_id()

main()
