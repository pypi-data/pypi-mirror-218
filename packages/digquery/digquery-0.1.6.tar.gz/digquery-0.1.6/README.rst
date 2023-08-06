
==============
digquery
==============

A Python package for querying DNS information using the `dig` command.

Installation
------------

Install the package using pip:

.. code-block:: bash

    pip install digquery

Usage
-----

To use the `digquery` command, run it from the command line followed by the domain name:

.. code-block:: bash

    digquery example.com 
    pydig example.com 
    mydig example.com

This will execute separate `dig` commands for each query type (`A` , `TXT` , `MX`, `NS`) and display the results in clear and crisp format.

Contributing
------------

Contributions are welcome! Here are some ways you can contribute:

- Report bugs or suggest improvements by creating a new issue on the `digquery` GitHub repository.
  https://github.com/techdjay/digquery
- Fork the repository, make changes, and submit a pull request.

License
-------

This project is licensed under the MIT License. See the `LICENSE` file for more information.

Authors
-------

- Jay <techdjay@gmail.com>


