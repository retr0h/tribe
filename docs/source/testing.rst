Testing
=======

Requirements:

* Ansible >= 1.6
* Vagrant >= 1.6
* Tox

Execute unit tests:

.. code-block:: bash

    $ vagrant up --no-provision
    $ vagrant provision
    $ tox

Execute integraton tests:

.. code-block:: bash

    $ PLAYBOOK=vagrant/tests/main.yml vagrant provision
