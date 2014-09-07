# Synchronise #

This is the synchronise module.

### Overview ###

This module allows you to synchronise BitBucket Mercurial to GitHub Git 
projects.

### How do you make the synchonisation work? ###

There is an example directory.  Install it and follow these rules to 
synchronise your project called <project> on Bitbucket with user called 
<user> to Github:

1. Make sure your Bitbucket repository is Mercurial based. Your project 
   can be private or public.
2. In the Settings of your project (click the cogwheel), select the 
   Hooks section.  Select the 'POST' hook and point it to the URL you 
   installed this module in.  
   The URL needs to be public.  If that would be a problem, there is already 
   a synchroniser installed at 
   `http://api.elevenbits.org:8000/synchronise/`.  You can use that
   if you want to.
3. Make sure you have a GitHub project with the same username and the 
   same projectname, i.e. <user> and <project> respectively.
   *Note: Soon you'll be able to use different names for both users and 
   projects on the GitHub side.*
4. In the GitHub select your <project> and visit its Settings page.
   Add 'Synchroniser' as Collaborator.
5. Done!

From now on, when you do a push to your Bitbucket project, the module will 
be informed by the POST and push it to GitHub as the Synchroniser collaborator.
This will immediately make sure the GitHub project will be synchronised with
the Butbucket one.

### How does it work? ###

Each time a Mercurial push arrives at Bitbucket, it will send a request
to the URL specified in the POST hook of the pushed project.

The JSON content of the POST is clearly explained
[at the Bitbucket website](https://confluence.atlassian.com/display/BITBUCKET/POST+hook+management).

The '/synchronise/' link will parse the JSON and see if it is a valid POST.

When it is a valid POST it will clone the Mercurial repository specified in 
it using [hgapi](https://bitbucket.org/haard/hgapi). Then it will make
sure that the [hggit](https://bitbucket.org/durin42/hg-git) extension is 
enabled and an extra `github` path is added. After bookmarking the tip 
as master (via `hg bookmark master`), it will push the repo to GitHub (via
`hg push github`). Since Synchroniser is a collaborator the push will succeed.

See the code for more information.

### Error codes ###

Successful synchonisation request will return 200 with an informational
message.  The synchroniser will return 400 when a request was unsuccessfully
handled.

Some examples when a 400 would be returned:
- When invalid request arrives (e.g. no JSON payload)
- The github project specified in the request does not exist
- The user specified in the request the user does not exist
- No Synchroniser collaborator is specified in the GitHub project

A 500 will be returned when something bad happened at the server side, and
is not caused by an invalid request.  For example the hggit plugin is not
available or hgapi misbehaved.

### Can I create my own Synchroniser? ###

Yes you can! All the code is available here. When you have a server 
available, you can point the POST hook to your own machine.

Here is a first draft of the installation process using `nginx` and `uwsgi`:

* Make sure `nginx` and `uwsgi` are installed.
* Add a new site configuration in `/etc/nginx`.
* Add a new uwsgi configuration in `/etc/uwsgi`.
* Restart both `nginx` and `uwsgi`.
* Enjoy your synchronisation server!

#### Notes ####

* This is a Django project, and uses only Python based dependencies: hgapi
  and hggit.
* The database is not really needed.  The default sqlite3 will do for now.
* To install UWSGI:
   - Do not install using your distribution methods. So, do not use `apt-get`,
     `yum` or `pakman`.
   - Please download the latest uwsgi: http://projects.unbit.it/downloads/uwsgi-2.0.6.tar.gz
   - Build plugins for it:
     `python2.7 uwsgiconfig.py --plugin plugins/python core python27`
     `python3.4 uwsgiconfig.py --plugin plugins/python core python34`
   - Create two ini files, one for Python 2.7 (two.ini), another one for Python
     3 (three.ini):

##### two.ini #####  

[uwsgi]
plugin-dir = /home/jw/plugins
plugin = python27
chdir = /home/jw/apps/two
master = true
threads = 2
processes = 4
http-socket = :9090
wsgi-file = foobar.py

##### three.ini #####

[uwsgi]
plugin-dir = /home/jw/plugins
plugin = python34
chdir = /home/jw/apps/three
master = true
threads = 2
processes = 4
http-socket = :8080
wsgi-file = fizzbuzz.py

Start the uwsgi emperor with `uwsgi --emperor <path where the ini files live>`
and see the system handle to different python releases!

### Contribution guidelines ###

* Please write tests for me?
* Do not hesitate to do a code review.
* When writing code, do follow [PEP8](http://legacy.python.org/dev/peps/pep-0008/).
  But use `'` before `"`; so `print('Hello there')` and 
  `foo = '"Hej!", said Fritz'` are valid, while `print("Foobar")` is not. 

### Who do I talk to? ###

* Mail jw@elevenbits.com for info, help, support,...
* Leave requests and bug reports on the issues page
