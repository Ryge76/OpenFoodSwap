import mysql.connector as mc
import config

"""
Etpaes:
1. initialiser la connection avec la DB
2. Remplir la BD
3. Faire des requêtes select pour chercher un produit
3. Faire des requêtes select pour trouver un équivalent
4. Enregistrer le substitut dans la BD

5. 
"""


class DBAccess:
    """Manage access to the OFS database.
    Provide functions to add data in the db and query those data"""
    def __init__(self):
        self.cnx = mc.connect(**config.db_access_testing)

