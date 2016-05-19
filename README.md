Test project - one page app 
---------------------
Tim Messick 

Demonstration of basics of Django/Python/Javascript/AJAX/3rd party API integration

Notes
------

To Run:
1) Make sure you have virtualenv available

2) git init && git remote add origin https://github.com/awlzac/smt.git && git pull origin master
This will acquire the project from my github account.

3) source smtsetup.sh
This is a convenience script for the expected setup process, virtualenv, pip installs, ensuring python3, initial migrate, etc.


From there, run testcases with: ./manage.py test
or run the server with e.g.: ./manage.py runserver 0.0.0.0:8000

In the browser, click on the map to add an address to the list, or "Clear Addresses" to clear the list, the back end db, and the Google Fusion table.

