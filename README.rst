=========
BIMA BACK
=========

Example deploying a `djang-bima-back <https://github.com/AjuntamentdeBarcelona/django-bima-back>`_
based project.

Installation and run
--------------------

#. Clone project from the Git repository.

#. Setup Node.js environment ::

    cd bima_back
    npm install

#. Setup Python virtualenv ::

    mkvirtualenv "bima_back" -p python3
    pip install -r requirements/local.txt

#. Create local configuration ::

    cd src
    cp app.ini.template app.ini

#. Review and edit ``app.in```, specially ``WS_BASE_URL``, it should point to `djang-bima-core <https://github.com/AjuntamentdeBarcelona/django-bima-core>`_

#. Check test ::

    pytest

#. Run local server ::

    python manage.py runserver

#. Run rq queue ::

    python manage.py rqworker back

Contributing
------------

See `<CONTRIBUTING.rst>`_.
