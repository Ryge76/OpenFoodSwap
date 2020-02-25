import mysql.connector as mc
import OpenFoodsSwap.config as config


class UseDB:
    """Manage access to the OFS database.
    Provide functions to add data in the db and query those data"""
    def __init__(self):
        self.cnx = mc.connect(**config.db_access_testing)
        # print("\n Connexion initialisée.")

    def end_connexion(self):
        self.cnx.close()
        return print("\n Connexion terminée.")

    @staticmethod
    def close_cursor(cursor):
        """Close cursor."""
        cursor.close()
        # return print("Curseur fermé.")

    def create_cursor(self, **cursor_type):
        """Create a cursor and pass the request to the db."""
        cursor = self.cnx.cursor(**cursor_type)  # TODO: TE
        # print("\n Curseur créé.")
        return cursor

    def close_all(self, cursor=None):
        if cursor:
            cursor.close()
        self.cnx.close()

    def execute_search(self, statement, *data, **cursor_type):
        """Handle request command by creating the cursor and executing it.
        Require a tuple with the statement to perform, a list of data to
         process, an iterable cursor_type of parameters
        to create the cursor upon."""

        cursor = self.create_cursor(**cursor_type)
        try:
            cursor.execute(statement, *data)
        except mc.Error as e:
            print(" \n Votre recherche n'a pu aboutir suite à cette erreur: "
                  "\n{}".format(e))
            return
        else:
            return cursor

    def execute_insertion(self, statement, data, **cursor_type):
        """Handle request command by creating the cursor and executing it.
        Require tuple with the statement to perform, a list of data to process,
         iterable cursor_type of parameters
        to create the cursor upon."""

        cursor = self.create_cursor(**cursor_type)

        try:
            cursor.execute(statement, data)
        except mc.Error as e:
            print("\n Suite à cette erreur: {}, \n "
                  "l'item suivant n'a pas été ajouté à la table voulu. "
                  "\n {}".format(e, data))

        else:
            # print("\n {}, a été ajouté à la table voulu.".format(data))
            self.cnx.commit()

        self.close_cursor(cursor)


class Command:
    """Manage cursor creation and closing. """

    def __init__(self):
        self.cursor_type = {'dictionary': False, 'buffered': False}

    @staticmethod
    def add_products(db, data):
        """Allow inserting items in selected table.
        Need table, data formated for selected table"""
        add_products = (
            "INSERT INTO products "
            "(category_id, product_name, url, image_url, nutrition_grade_fr,"
            " ingredients_text, allergens, stores, purchase_places) "
            "VALUES (%(category_id)s, %(product_name)s, %(url)s,"
            " %(image_url)s, %(nutrition_grade_fr)s, "
            "%(ingredients_text_fr)s, %(allergens)s, %(stores)s,"
            " %(purchase_places)s)")

        db.execute_insertion(add_products, data)

    @staticmethod
    def add_categories(db, data):
        """Add a new category in 'categories' table.
        Require data to be a list type"""
        add_category = ("INSERT INTO categories "
                        "(categ_name) "
                        "VALUES (%s)")

        if isinstance(data, str):
            value = [data]
            db.execute_insertion(add_category, value)

        else:
            for item in data:
                if isinstance(item, (dict, list)):
                    db.execute_insertion(add_category, item)

                else:
                    value = [item]
                    db.execute_insertion(add_category, value)

    @staticmethod
    def add_substitute(db, data):
        """Add a product and its substitute to substitutes table.
        Require database connexion object and id keys of both product."""
        add_substitute = ("INSERT INTO substitutes "
                          "(initial_product, substitute, subs_date) "
                          "VALUES (%s, %s, now())")

        db.execute_insertion(add_substitute, data)

    def find_item_description(self, db, product_id):
        """Allow search for data in specific table"""
        search_product = ("SELECT product_name, nutrition_grade_fr,"
                          " ingredients_text, allergens, stores, "
                          "purchase_places, url, image_url, id, category_id "
                          "FROM products WHERE id = %s")

        self.cursor_type.update(dictionary=True, buffered=True)

        product_id = [product_id]

        results = db.execute_search(search_product, product_id,
                                    **self.cursor_type)

        return results

    def find_category_id(self, db, category):
        """Get the id associated with a specific category in the
        Categories table.
        Require a category name (string).
        Return an id integer"""

        categ_name = [category]
        find_category_id = ("SELECT id FROM categories "
                            "WHERE categ_name = %s")

        self.cursor_type.update(dictionary=False, buffered=True)

        results = db.execute_search(find_category_id, categ_name,
                                    **self.cursor_type)

        if results is None:
            print("La categorie {} n'existe pas".format(category))
            return None
        else:
            # get only the integer value of cursor_id tuple
            id_number = results.fetchone()[0]
            print("\n Pour la catégorie {}, l'id est {}.".format(categ_name,
                                                                 id_number))

        db.close_cursor(results)

        return id_number

    def search_any_product(self, db, name):
        search_all_products = (
            "SELECT product_name, products.id, nutrition_grade_fr,"
            " categ_name AS categorie "
            "FROM products INNER JOIN categories "
            "ON products.category_id = categories.id "
            "WHERE product_name LIKE %s "
            "ORDER BY product_name")

        look_for = [name + '%']
        self.cursor_type.update(dictionary=True, buffered=True)

        results = db.execute_search(search_all_products, look_for,
                                    **self.cursor_type)

        return results

    def search_substitute(self, db, product_score, category_id):
        search_substitute = ("SELECT product_name, categories.categ_name,"
                             " nutrition_grade_fr, products.id "
                             "FROM products "
                             "INNER JOIN categories "
                             "ON products.category_id = categories.id "
                             "WHERE category_id = %(categ)s AND "
                             "nutrition_grade_fr < %(score)s "
                             "ORDER BY nutrition_grade_fr, product_name")

        replace_me = {'score': product_score, 'categ': category_id}
        self.cursor_type.update(dictionary=True, buffered=True)

        results = db.execute_search(search_substitute, replace_me,
                                    **self.cursor_type)

        return results

    def find_by_category(self, db, category):
        """Get products by category"""
        find_category = ("SELECT product_name, products.id,"
                         " nutrition_grade_fr, categ_name AS categorie "
                         "FROM products INNER JOIN categories "
                         "ON products.category_id = categories.id "
                         "WHERE categ_name = %s "
                         "ORDER BY product_name")

        look_for = [category]

        self.cursor_type.update(dictionary=True, buffered=True)
        results = db.execute_search(find_category, look_for,
                                    **self.cursor_type)

        return results

    def show_all_substitutes(self, db):
        """Show all substitutions from substitutes table"""
        show_substitutes = ("SELECT products.product_name as 'source',"
                            " products.nutrition_grade_fr, products.id, "
                            "p.product_name as 'substitut', "
                            "p.nutrition_grade_fr as 'nutriscore', "
                            "p.id as 'id_sub', subs_date "
                            "FROM substitutes INNER JOIN products "
                            "ON initial_product = products.id "
                            "INNER JOIN products AS p ON substitute = p.id "
                            "ORDER BY subs_date")

        self.cursor_type.update(dictionary=True, buffered=True)
        results = db.execute_search(show_substitutes, **self.cursor_type)

        return results


def sample():
    product = [
        {'allergens': 'en:gluten,en:milk,en:soybeans',
         'product_name': 'Prince: Goût Chocolat au Blé Complet',
         'stores': 'Carrefour Market,Magasins U,Auchan,Intermarché,Carrefour,'
                   'Casino,Leclerc,Cora,Bi1',
         'url': 'https://fr.openfoodfacts.org/',
         'image_url': 'https://static.openfoodfacts.org/images/',
         'nutrition_grade_fr': 'd',
         'purchase_places': 'F-77480 Mousseaux-les-Bray,FRANCE',
         'ingredients_text_fr': "Céréale , sucre, sel, lait écrémé en poudre,"
                                " lactose et protéines de lait, arômes."}]

    categories = ['snacks', 'legumes']

    # initiate connexion to the database
    db = UseDB()
    c = Command()
    c.add_categories(db, categories)
    categ = c.find_category_id(db, 'snacks')
    product[0].update(category_id=categ)
    c.add_products(db, product)
    sub = [1, 20]
    c.add_substitute(db, sub)

    c.find_item_description(db, [5])

    c.search_any_product(db, 'Nutella')

    db.close_all()


if __name__ == '__main__':
    sample()
