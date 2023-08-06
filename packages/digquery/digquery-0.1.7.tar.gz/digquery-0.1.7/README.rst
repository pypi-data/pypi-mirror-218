
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

Output of above command will be look like:

.. code-block:: bash

	digquery google.com
	====================================
	dig query for domain: google.com, type: TXT
	====================================
	google.com.             3600    IN      TXT     "docusign=05958488-4752-4ef2-95eb-aa7ba8a3bd0e"
	google.com.             3600    IN      TXT     "google-site-verification=wD8N7i1JTNTkezJ49swvWW48f8_9xveREV4oB-0Hf5o"
	google.com.             3600    IN      TXT     "MS=E4A68B9AB2BB9670BCE15412F62916164C0B20BB"
	google.com.             3600    IN      TXT     "google-site-verification=TV9-DBe4R80X4v0M4U_bd_J9cpOJM0nikft0jAgjmsQ"
	google.com.             3600    IN      TXT     "facebook-domain-verification=22rm551cu4k0ab0bxsw536tlds4h95"
	google.com.             3600    IN      TXT     "globalsign-smime-dv=CDYX+XFHUw2wml6/Gb8+59BsH31KzUr6c1l2BPvqKX8="
	google.com.             3600    IN      TXT     "webexdomainverification.8YX6G=6e6922db-e3e6-4a36-904e-a805c28087fa"
	google.com.             3600    IN      TXT     "v=spf1 include:_spf.google.com ~all"
	google.com.             3600    IN      TXT     "onetrust-domain-verification=de01ed21f2fa4d8781cbc3ffb89cf4ef"
	google.com.             3600    IN      TXT     "atlassian-domain-verification=5YjTmWmjI92ewqkx2oXmBaD60Td9zWon9r6eakvHX6B77zzkFQto8PQ9QsKnbf4I"
	google.com.             3600    IN      TXT     "docusign=1b0a6754-49b1-4db5-8540-d2c12664b289"
	google.com.             3600    IN      TXT     "apple-domain-verification=30afIBcvSuDV2PLX"
	
	====================================
	dig query for domain: google.com, type: A
	====================================
	google.com.             142     IN      A       142.250.193.238
	
	====================================
	dig query for domain: google.com, type: MX
	====================================
	google.com.             300     IN      MX      10 smtp.google.com.
	
	====================================
	dig query for domain: google.com, type: NS
	====================================
	google.com.             13296   IN      NS      ns4.google.com.
	google.com.             13296   IN      NS      ns1.google.com.
	google.com.             13296   IN      NS      ns3.google.com.
	google.com.             13296   IN      NS      ns2.google.com.


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


