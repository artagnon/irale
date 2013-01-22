# Dependencies

* postgresql 9.1
* postgis 2.0.2
* django 1.5b2
* python-psycopg2 2.4.5

On a Debian Sid system,

    # Install postgresql, python-psycopg2, and the dependencies
    # required for building postgis
    $ apt-get install postgresql python-psycopyg2 build-essential
    libxml2-dev libproj-dev libjson0-dev xsltproc docbook-xsl
    docbook-mathml libgdal-dev postgresql-server-dev-all

    # Debian repositories only have postgis 1.5, so install it using
    # the tarball from the site
    $ http://download.osgeo.org/postgis/source/postgis-2.0.2.tar.gz
    $ tar xf postgis-2.0.2.tar.gz
    $ cd postgis-2.0.2
    $ ./configure
    $ make
    $ make install

    # Debian repositories only have Django 1.4, so use pip to install
    # it in ~/.local
    $ pip install --user git+git://github.com/django/django.git@1.5b2

    # Make sure that your $PATH and $PYTHONPATH are set correctly
    $ export PATH=$PATH:~/.local/bin
    $ export PYTHONPATH=$PYTHONPATH:~/.local/lib

# Database setup

First, get Postgresql to trust all local connections.  For this, edit
pg_hba.conf to contain these lines:

    local   all             postgres                                trust
    local   all             all                                     trust
    host    all             all             127.0.0.1/32            trust
    host    all             all             ::1/128                 trust

Create a superuser account with your UNIX login:

    $ sudo -u postgres createuser -s $USER

Create a database call irale belonging to this new user:

    $ createdb irale

Make it a spatial database for use with PostGIS:

    $ psql irale
    irale=# CREATE EXTENSION postgis;
    irale=# CREATE EXTENSION postgis_topology;

Tell Django about your db user:

    $ echo "user = '$USER'" >irale/localsettings.py

Generate the db schema:

    $ python manage.py syncdb

# Running

    # Run the server on http://localhost:8000
    $ python manage.py runserver

Optionally, get localtunnel to make the server accessible from the
internet:

    $ gem install localtunnel
    $ localtunnel -k ~/.ssh/id_rsa.pub 8000
