# OpenFoodSwap
Simple Foods swapping app based Open Foods Facts DB.

This application aime to provide you healthier substitutes for a selected
product. 

---------------
# **Functions**


User have two options:

1. Search the DB for some food he wants to find information about
2. Find a healthier equivalent to a product and save it
3. Look for his previous saved substitutes

This app should be usable via simple cli or GUI (work in progress).

# **Requirements**
1. Download and install [Python 3.7 or latest version](https://www.python.org/)
2. Download and install [Pipenv](https://pypi.org/project/pipenv/)
3. Download and install [MySql Community Edition](https://www.mysql.com/products/community/)

# **How to install**

1. Create a directory on your hard drive and then clone this repository 
(or download compressed file on your hard drive)
2. Run `pipenv install` in the directory of your application. 
This will install all required dependencies
3. Execute the database creation script `ofsdb_simple_creation.sql` 
(install folder)
4. Run `pipenv run python ofs.py [-i]`
(*-i* is only necessary for the first launch to populate the database with data)


Enjoy !

