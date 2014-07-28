from setuptools import setup, find_packages

kwargs = {
    'packages': find_packages(exclude=['tests', '*.tests',
                                       '*.tests.*', 'tests.*']),
    'include_package_data': True,
    'install_requires': [
        'django>=1.4,<1.7',
    ],
    'name': 'django-synchroniser',
    'version': __import__('synchronise').get_version(),
    'author': 'Jan Willems',
    'author_email': 'jw@elevenbits.com',
    'description': 'django-synchroniser synchronises Bitbucket Mecurial'
                   'base projects to GitHub (Git based) projects',
    'license': 'GPLv3',
    'keywords': 'synchronise synchronise bitbucket github',
    'url': 'https://github.com/elevenbits/django-synchroniser',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
}

setup(**kwargs)