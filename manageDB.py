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


class UseDB:
    """Manage access to the OFS database.
    Provide functions to add data in the db and query those data"""
    def __init__(self):
        self.cnx = mc.connect(**config.db_access_testing)
        print("\n Connexion initialisée.")

    def cancel_insertion(self):
        self.cnx.rollback()
        return print("Requête annulée.")

    def validate_insertion(self):
        self.cnx.commit()
        return print("Requête appliquée (commit).")

    def end_connexion(self):
        self.cnx.close()
        return print("\n Connexion terminée.")

    @staticmethod
    def close_cursor(cursor):
        """Close cursor."""
        cursor.close()
        return print("Curseur fermé.")

    def create_cursor(self, **cursor_type):
        """Create a cursor and pass the request to the db."""
        cursor = self.cnx.cursor(**cursor_type)  # TODO: TE
        print("Curseur créé.")
        return cursor

    def close_all(self, cursor):
        cursor.close()
        self.cnx.close()

    @staticmethod
    def execute_search(statement, data, **cursor_type):
        """Handle request command by creating the cursor and executing it.
        Require a tuple with the statement to perform, a list of data to process, an iterable cursor_type of parameters
        to create the cursor upon."""

        cursor = UseDB.create_cursor(**cursor_type)
        cursor.execute(statement, data)
        return cursor

    def execute_insertion(self, statement, data):
        """Handle request command by creating the cursor and executing it.
        Require tuple with the statement to perform, a list of data to process, iterable cursor_type of parameters
        to create the cursor upon."""

        cursor = UseDB.create_cursor()

        for item in data:
            try:
                cursor.execute(statement, item)
            except mc.Error as e:
                print("\n Suite à cette erreur: {}, \n l'item suivant n'a pas été ajouté à la table voulu. "
                      "\n {}".format(e, item))
                continue
            else:
                print("\n {}, a été ajouté à la table voulu.".format(item))

        self.cnx.commit()
        UseDB.close_all(cursor)


class Request(UseDB):
    """Manage cursor creation and closing. """

    def __init__(self):
        super.__init__()
        self.cursor_type = {'dictionary': False, 'buffered': False}

    def add_products(self, data):
        """Allow inserting items in selected table.
        Need table, data formated for selected table"""
        add_products = ("INSERT INTO products "
                        "(category_id, product_name, url, image_url, nutrition_grade_fr, ingredients_text, allergens, "
                        "stores, purchase_places) "
                        "VALUES (%(category_id)s, %(product_name)s, %(url)s, %(image_url)s, %(nutrition_grade_fr)s, "
                        "%(ingredients_text_fr)s, %(allergens)s, %(stores)s, %(purchase_places)s)")

        Request.execute_insertion(self, add_products, data)

    def add_categories(self, data):
        add_category = ("INSERT INTO categories "
                        "(categ_name) "
                        "VALUES (%s)")

        Request.execute_insertion(self, add_category, data)
        Request.close_all()

    def add_substitute(self):
        pass

    def find_items(self):
        """Allow search for data in specific table"""

        pass

    def find_category_id(self, category):
        """Get the id associated with a specific category in the Categories table.
        Require a category name. Return an id integer"""

        categ_name = category
        find_category_id = ("SELECT id FROM categories "
                            "WHERE categ_name = %s")

        self.cursor_type['buffered'] = True

        results = Request.execute_search(find_category_id, categ_name, **self.cursor_type)  # cursor object

        id_number = list(
            results.fetchone()).pop()  # get only the integer value of cursor_id tuple (transformed into a list)
        print("\n Pour la catégorie {}, l'id est {}.".format(categ_name, id_number))

        Request.close_all(results)
        return id_number

