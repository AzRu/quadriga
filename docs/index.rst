Quadriga
--------

Welcome to the documentation for **quadriga**, Python client for Canadian
cryptocurrency exchange platform QuadrigaCX_. It wraps the exchange's
`REST API v2`_ using the `requests`_ library.

.. _QuadrigaCX: https://www.quadrigacx.com
.. _REST API v2: https://www.quadrigacx.com/api_info
.. _requests: https://github.com/requests/requests

Requirements
============

- Python 2.7, 3.4, 3.5 or 3.6
- QuadrigaCX API secret, API key and client ID (the number used for your login)

Installation
============

To install a stable version from PyPi_:

.. code-block:: bash

    ~$ pip install quadriga

To install the latest version directly from GitHub_:

.. code-block:: bash

    ~$ pip install -e git+git@github.com:joowani/quadriga.git@master#egg=quadriga

You may need to use ``sudo`` depending on your environment.

.. _PyPi: https://pypi.python.org/pypi/quadriga
.. _GitHub: https://github.com/joowani/quadriga


Contents
========

.. toctree::
    :maxdepth: 1

    overview
    specs
    errors
    public
    logging
    session
    contributing


Disclaimer
==========

The author(s) of this project is in no way affiliated with QuadrigaCX, and
shall not accept any liability, obligation or responsibility whatsoever for
any cost, loss or damage arising from the use of this client. Please use at
your own risk.
