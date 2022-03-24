# pip install GitPython==3.*
from git import GitCommandError, Repo

from programlib import Program

GIT_USER = 'Vadim Liventsev'
GIT_EMAIL = 'hello@vadim.me'
GITHUB_USERNAME = 'vadim0x60'
GITHUB_PASSWORD = 'GITHUB_PASSWORD'
GITHUB_REPO = 'programlib.git'

github_remote = f'https://{GITHUB_USERNAME}:{GITHUB_PASSWORD}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}'

def upload_file(repo, filename, message=None):
    if not message:
        message = f'added {filename}'

    repo.index.add(filename)
    repo.index.commit(message)
    repo.remotes.origin.pull()
    repo.remotes.origin.push()

def ensure_correct_repo(remote, path):
    try:
        repo = Repo.clone_from(remote, path)
    except GitCommandError:
        repo = Repo(path)
    assert repo.remotes.origin.url == remote

    repo.config_writer().set_value('user', 'name', GIT_USER).release()
    repo.config_writer().set_value('user', 'email', GIT_EMAIL).release()
    return repo

# Create a program
program = Program(source='print("Hello, world!")', language='Python')

# Test it
assert program.run() == ['Hello, world!']

# Upload it to GitHub
repo = ensure_correct_repo(github_remote, 'programs')
program.save('programs/hello.py')
upload_file(repo, 'hello.py')