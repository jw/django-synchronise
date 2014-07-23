__version_info__ = {
    'major': 0,
    'minor': 1,
    'micro': 0,
    'releaselevel': 'beta',
    'serial': 42
}


def get_version(short=False):
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    version = ["{}.{}.{}".format(__version_info__['major'],
                                 __version_info__['minor'],
                                 __version_info__['micro'])]
    if __version_info__['releaselevel'] != 'final' and not short:
        version.append('{}{}'.format(__version_info__['releaselevel'][0],
                                     __version_info__['serial']))
    return ''.join(version)

__version__ = get_version()
