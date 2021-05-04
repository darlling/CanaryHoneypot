Honeypot
==========

Getting Started
--------------

To get started create a virtual environment to play in:

.. code-block:: sh

   $ virtualenv env
   $ . env/bin/activate

Inside the virtualenv, install Honeypot following the instructions in the `README <https://github.com/thinkst/opencanary>`_.

Honeypot ships with a default config, which we'll copy and edit to get started. The config is a single `JSON <https://en.wikipedia.org/wiki/JSON>`_ dictionary.

.. code-block:: sh

   $ honeypotd --copyconfig
   $ $EDITOR ~/.honeypot.conf

In the config file we'll change **device.node_id** which must be unique for
each instance of honeypotd, and we'll configure **logger** to log
alerts to a file.

.. code-block:: json

   {
       "device.node_id": "Your-very-own-unique-name",
       [...]
        "logger": {
	    "class" : "PyLogger",
	    "kwargs" : {
	        "handlers": {
	            "file": {
		        "class": "logging.FileHandler",
		        "filename": "/var/tmp/honeypot.log"
			}
	         }
	    }
       }
      [...]
   }


With that in place, we can run the daemon, and test that it logs a failed FTP login attempt to the log file.

.. code-block:: sh

   $ honeypotd --start
   [...]
   $ ftp localhost
   [...]
   $ cat /var/tmp/honeypot.log
   [...]
   {"dst_host": "127.0.0.1", "dst_port": 21, "local_time": "2021-04-26 13:38:21.281259", "logdata": {"PASSWORD": "default", "USERNAME": "admin"}, "logtype": 2000, "node_id": "honeypot-1", "src_host": "127.0.0.1", "src_port": 49635}
   

Troubleshooting
---------------

The tool JQ can be used to check that the config file is well-formed JSON.

.. code-block:: sh

   $ jq . ~/.honeypot.conf

Run honeypotd in the foreground to see more error messages.

.. code-block:: sh

   $ honeypotd --dev

You may also easily restart the service using,

.. code-block:: sh

   $ honeypotd --restart

