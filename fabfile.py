
# This deployment file needs to stay Python 2, since Fabric still is... :(

from fabric.api import run, env
from fabric.decorators import task
from fabric.operations import require, sudo
from fabric.colors import red, green, yellow
from fabric.utils import abort
from fabric.context_managers import settings, cd

from ConfigParser import SafeConfigParser as ConfigParser, NoOptionError
from os.path import join, dirname, realpath, isfile, exists


CONFIGURATION_FILE = 'django-synchroniser.properties'


# deployment properties
env.prefix = '/var/www'
env.remote = env.path = "%(prefix)s/django-synchroniser" % env
env.local = dirname(realpath(__file__))


def _create_environment(filename, environment):
    """
    Create the correct env keys for an environment using a given configuration
    filename. Also the properties of the project are retrieved.
    @param filename: the filename to be read as configuration.
    @param environment: the section in the filename to be used as
    configuration file.
    """
    if not isfile(filename):
        print(red('Configuration file {} does not exist.'.format(filename)))
        abort('Could not find configuration file {}.'.format(filename))
    config = ConfigParser()
    config.read(filename)
    if environment in config.sections():
        env.settings = environment
        _add_environment_properties(config, environment)
    else:
        print(red('Could not find the [{}] section in {}.'.format(environment,
                                                                  filename)))
        abort('Could not find the [{}] section in {}.'.format(environment,
                                                              filename))


def _add_environment_properties(config, section):
    """
    Get the database entries of a environment section from a config parser.
    @param config: a ConfigParser.
    @param section: a section in an ini file, e.g. staging, or production.
    """
    try:
        env.user = config.get(section, "user.username")
        env.password = config.get(section, "user.password")
        env.dbuser = config.get(section, "db.username")
        env.dbpassword = config.get(section, "db.password")
        env.dbname = config.get(section, "db.name")
        env.hosts = [config.get(section, "host")]
        return True
    except NoOptionError as noe:
        print(red('Could not find the {} key in the {} section.'.format(
            noe.option,
            noe.section)
        ))
        abort('Could not find the {} key in the {} section.'.format(
            noe.option,
            noe.section)
        )



@task
def production():
    """
    Build for a Production environment.
    Files will come from the repository.
    """
    _create_environment(join('conf', CONFIGURATION_FILE), 'production')


@task
def staging():
    """
    Build for a Staging environment.
    Files will come from the repository.
    """
    _create_environment(join('conf', CONFIGURATION_FILE), 'staging')


@task
def development():
    """
    Build for a Development environment.
    Files will come from the repository, or (when in tip) from the users
    drive.
    """
    _create_environment(join('conf', CONFIGURATION_FILE), 'development')


@task
def tip():
    """
    Deploy the tip.
    """
    env.branch = 'tip'


@task
def revision(revision="tip"):
    """
    Deploy a certain revision.  Default is the tip.
    """
    env.branch = revision


@task
def deploy():
    """
    Install everything we need, then fire up the system.
    """

    require('settings', provided_by=[production, staging, development])
    require('branch', provided_by=[tip, revision])

    print(green("Fabricating %s in %s environment..." %
                (env.branch, env.settings)))

    if env.settings == "development" and env.branch == "tip":
        print(green("Deploying hot development trunk..."))
        copy_current()

    print(green("Checking to see if uwsgi is an upstart job..."))
    handle_uwsgi_upstart()

    print(green("Updating nginx and uwsgi configuration..."))
    update_webserver_and_uwsgi_configuration()

    print(green("Setup complete."))


def uwsgi_is_upstart_job():
    if exists("/etc/init/uwsgi.conf"):
        output = run("initctl list", quiet=True)
        if "uwsgi" in output:
            return True
        else:
            return False
    else:
        return False


def handle_uwsgi_upstart():
    """Make sure that uwsgi is an upstart job."""
    if uwsgi_is_upstart_job():
        print(green("uwsgi seems to be an upstart job. Leaving as is."))
    else:
        print(green("Forcing uwsgi to be an upstart job..."))
        sudo("cp %(path)s/conf/uwsgi.conf /etc/init" % env)
        sudo("initctl reload-configuration")
        if uwsgi_is_upstart_job():
            print(green("Good. uwsgi is now an upstart job."))
        else:
            print(red("Could not make uwsgi an upstart job. Please check."))


def update_webserver_and_uwsgi_configuration():
    # remove default first if it is there
    if exists("/etc/nginx/sites-enabled/default"):
        with settings(warn_only=True):
            sudo("rm /etc/nginx/sites-enabled/default")
    # update nginx
    sudo("mkdir -p /etc/nginx/sites-available" % env)
    # api.conf
    sudo("cp %(path)s/conf/api.conf /etc/nginx/sites-available" % env)
    sudo("ln -sf %(path)s/conf/api.conf /etc/nginx/sites-enabled" % env)
    # update uwsgi
    sudo("mkdir -p /etc/uwsgi/apps-available" % env)
    sudo("mkdir -p /etc/uwsgi/apps-enabled" % env)
    sudo("cp %(path)s/conf/synchroniser.ini /etc/uwsgi/apps-available" % env)
    sudo("ln -sf %(path)s/conf/synchroniser.ini /etc/uwsgi/apps-enabled" % env)


def checkout_latest():
    """Get latest version from repository."""
    sudo('hg clone '
         'https://%(account)s@%(repo)s/%(account)s/%(name)s '
         '%(path)s' % env, user="www-data")


def checkout_revision(revision):
    """Clone a revision."""
    sudo('hg clone -r %(branch)s '
         'https://%(account)s@%(repo)s/$(account)s/%(name)s '
         '%(path)s' % env, user="www-data")


def install_requirements():
    """
    Install the required packages using pip.
    """
    sudo('pip install -r %(path)s/requirements.txt'.format(env))
    print(green("Some required packages are installed."))
    print(yellow("Some packages might be missing."))
    print(yellow("You still need to do check this yourself for now..."))


def copy_current():
    """
    Copy the current code to the server area.
    """
    sudo('cp -r %(local)s %(prefix)s' % env)
    sudo("chown www-data:www-data --recursive %(path)s" % env)