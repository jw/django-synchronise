from django.http import HttpResponse

import configparser
from os.path import join
from tempfile import TemporaryDirectory

import hgapi

import logging
logger = logging.getLogger(__name__)


def print_payload(payload, length):
    """
    Convert the payload to a string, and replace each whitespace section
    with a single space. Return it with a specified length.
    :param payload: A dict.
    :param length: The required length.
    :return: The processed payload of the specified length.
    """
    clean = ' '.join(str(payload).split())
    if len(clean) <= length:
        return clean
    else:
        return '"' + clean[0:length] + '..."'


def is_bitbucket_hg_payload(payload):
    """
    Check to see of the payload is a BitBucket POST from a Mercurial based
    project
    :param payload: The payload as a dist
    :return: True when it is a BitBucket POST from a Mercurial payload; False
    otherwise.
    """

    logger.debug('Checking {} for bitbucket and hg...'.
                 format(print_payload(payload, 20)))
    result = False
    try:
        if 'bitbucket' in payload['canon_url']:
            repo = payload['repository']
            if repo['scm'] == 'hg':
                logger.debug('This is a Bitbucket Mercurial repository POST.')
                result = True
    except KeyError:
        pass  # no canon_url or scm in payload
    return result


def bitbucket_hg_payload(payload, project=None, user=None):
    """
    Prepare a BitBucket Mercurial based project for synchronisation via
    HgGit
    :param payload: The payload as a dict
    :param project: The project string
    :param user: The userstring
    :return:
    """
    repo = payload['repository']
    # use default user and project when not given
    if user is None:
        user = repo['owner']
    if project is None:
        project = repo['name']
    # hg_path should be ssh://hg@bitbucket.org/<name>/<project>,
    hg_path = 'ssh://hg@bitbucket.org/{}/{}'.format(repo['owner'],
                                                    repo['name'])
    # git_path should be git+ssh://git@github.com/<user>/<project>.git
    git_path = 'git+ssh://git@github.com/{}/{}.git'.format(user, project)
    try:
        hg_to_git(hg_path, git_path)
    except hgapi.HgException as he:
        HttpResponse("Could not convert: {}.".format(he),
                     status=500, reason='HgApi problem: {}'.format(he))
    message = "Converted {} successfully".format(project)
    return HttpResponse(message, status=200, reason=message)


def synchronise(payload, user=None, project=None):
    """
    Synchronised the given payload.
    :param payload: The payload as a dict
    :param user: The user
    :param project: The project
    :return: A HttpResponse, either 200 when successful, 400 or 500 otherwise.
    """
    if is_bitbucket_hg_payload(payload):
        return bitbucket_hg_payload(payload, project, user)
    return HttpResponse('No proper JSON in payload. Discarding it.',
                        status=400, reason='No proper JSON in payload.')


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
    logger.debug('Converting {} to {}.'.format(hg_path, git_path))
    with TemporaryDirectory(prefix='hg-') as hg_repo_path:
        logger.debug('Cloning {} to {}...'.format(hg_path, hg_repo_path))
        hg_repo = hgapi.hg_clone(hg_path, hg_repo_path)
        add_hggit_extension_and_git_path(hg_repo_path, git_path)
        logger.debug('Bookmarking the clone...')
        hg_repo.hg_bookmarks(action=hgapi.Repo.BOOKMARK_CREATE, name='master')
        logger.debug('Pushing it to github...')
        hg_repo.hg_push('github')


def git_to_hg(git_path, hg_path):
    logger.debug('Converting {} to {}.'.format(git_path, hg_path))
    raise NotImplemented


def git_to_git(git_path, other_git_path):
    logger.debug('Converting {} to {}.'.format(git_path, other_git_path))
    raise NotImplemented
