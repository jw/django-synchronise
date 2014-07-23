import configparser
from os.path import join
from tempfile import TemporaryDirectory

import hgapi


def add_hggit_extension_and_git_path(hg_repo_path, git_path):
    """
    Add hggit extension to the hgrc and add git_path to its paths section.
    This is required to inform git of the hg changesets on the hg repository.
    :param hg_repo_path: The path of the hgrc
    :param git_path: The path of the github repo
    :return:
    """
    hgrc = join(hg_repo_path, '.hg', 'hgrc')
    config = configparser.ConfigParser()
    config.read(hgrc)
    # add hgit extension
    if 'extensions' in config.sections():
        if 'hggit' not in config['extensions']:
            config['extensions']['hggit']
    else:
        config['extensions'] = {}
        config['extensions']['hggit'] = ''
    # add git_path to the paths section
    if 'paths' in config.sections():
        if 'github' not in config['paths']:
            config['paths']['github'] = git_path
    else:
        config['paths'] = {}
        config['paths'][git_path] = ''
    # write the hgrc
    with open(hgrc, 'w') as config_file:
        config.write(config_file)


def hg_to_git(hg_path, git_path):
    """
    Convert the Bitbucket repo to a Github repo. First clone the hg_path,
    then add the hggit extension to this clone, and lastly push the clone
    to github.
    :param hg_path: The Bitbucket Mercurial based repository.
    :param git_path: The Github (obviously Git based) repository.
    :return:
    """
    print('Converting {} to {}.'.format(hg_path, git_path))
    with TemporaryDirectory(prefix='hg-') as hg_repo_path:
        print('hgapi.hg_clone({}, {})'.format(hg_path, hg_repo_path))
        hg_repo = hgapi.hg_clone(hg_path, hg_repo_path)
        add_hggit_extension_and_git_path(hg_repo_path, git_path)
        print('Bookmarking...')
        hg_repo.hg_bookmarks(action=hgapi.Repo.BOOKMARK_CREATE, name='master')
        print('Pushing...')
        hg_repo.hg_push('github')


def git_to_hg(git_path, hg_path):
    print('Converting {} to {}.'.format(git_path, hg_path))
    raise NotImplemented


def git_to_git(git_path, other_git_path):
    print('Converting {} to {}.'.format(git_path, other_git_path))
    raise NotImplemented
