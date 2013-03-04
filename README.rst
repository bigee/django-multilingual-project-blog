Django Multilingual Project Blog
================================

This is a central reusable app that contains templates, templatetags, 
context processors, middlewares, urls and fixtures for a multilingual project
blog (i.e. for scientific research projects).

This app basically contains a massive requirements text, making use of many
reusable apps that have been created for this project. It contains a few things
that tie together several of the other reusable apps and would be too
insignificant or specific to be turned into their own reusable apps.

The idea is that you can create a new Django project, provide a sufficient
``settings.py``, load the fixtures and run ``manage.py runserver`` and you
should see a fully fledged project blog with a nice but generic bootstrap
theme.

Then you would override the base template to provide your own logo and footer
and that's it.


Installation
------------

The preferred way to install this app is to place it next to your own apps
as a git submodule:

    # cd into your repo root
    $ git submodule add git://github.com/buildee/django-multilingual-project-blog.git path/to/folder/where/your/manage.py/resides
    $ git submodule --init
    $ git submodule --update

This is because this app has a ton of dependencies which are managed in a
``requirements.txt`` file. By adding this as a submodule you can easily install
this ``requirements.txt`` as part of your deployment process.

This app depends on a ton of other apps, so the easiest way to add everything
to your ``INSTALLED_APPS`` would be this::

    from multilingual_project_blog.settings import add_project_blog_apps

    INSTALLED_APPS = [
        ...
        # your installed_apps
    ]    

    INSTALLED_APPS = add_project_blog_apps(INSTALLED_APPS)

Run the South migrations::

    ./manage.py migrate


Roadmap
-------

Check the issue tracker on github for milestones and features to come.
