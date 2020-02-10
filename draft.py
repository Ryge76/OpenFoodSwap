import requests
import mysql.connector as mc
import config


def find_missing_keys(p_list):
    """Look for products in a list of products that haven't got the correct number of criteria. """
    to_delete = []  # list of indexes of incorrect products
    criteria = r_param['fields'].split(',')
    for i in range(len(p_list)):  # iterating the product list
        if len(p_list[i]) < len(criteria):
            print("Produit(s) non conforme(s): \n {}".format(p_list[i]))
            to_delete.append(i)
    print("Index des produits à supprimer: \n {}".format(to_delete))
    return to_delete


def check_value(dic, *args, value=''):
    """Check if the mandatory keys in a product, has a defined value.
    Return True if the specified value is found"""
    mandatory_keys = ['product_name', 'url', 'nutrition_grade_fr', 'ingredients_text_fr', 'stores',
                      'purchase_places']
    for key in mandatory_keys:
        if dic[key] == value:
            print("La valeur de la clé '{}' est manquante sur le produit '{}'".format(key, dic['product_name']))
            return True


def find_invalid_value(p_list):
    """Find product with no values for mandatory keys.
    Require a list of product in argument.
    Return list of indexes of products with incorrect values."""
    to_delete = []  # list of indexes of incorrect products

    for product in p_list:
        control = check_value(product)
        if control:
            index = p_list.index(product)
            to_delete.append(index)

    print("Index des produits à supprimer: \n {} \n".format(to_delete))
    return to_delete


def delete_incorrect(p_list, idx_list):
    idx_list.sort(reverse=True)  # sorting index in desc order
    for index in idx_list:
        p_list.pop(index)
    return p_list


# requesting OFF API
url = 'https://fr.openfoodfacts.org./cgi/search.pl'
r_param = {'action': 'process', 'tagtype_0': 'categories', 'tag_contains_0': 'contains', 'tag_0': 'snack',
           'sort_by': 'unique_scans_n', 'page_size': '60', 'json': 'true', 'fields':
               'product_name,image_url,nutrition_grade_fr,purchase_places,stores,url,ingredients_text_fr,allergens'}

r = requests.get(url, params=r_param)
print('Requête correctement effectuée. \n {}'.format(r.url))
r_json = r.json()
print(r_json)
products_list = r_json['products']
print("Nombre de produits initial: {}".format(len(products_list)))  # test


# cleaning the data set
missing_keys = find_missing_keys(products_list)  # find incorrect indexes
cleaned = delete_incorrect(products_list, missing_keys)
missing_values = find_invalid_value(cleaned)
cleaned_final = delete_incorrect(cleaned, missing_values)  # get the final list of product

print("La liste finale comporte {} produits. \n {}".format(len(cleaned_final), cleaned_final))

data_set = cleaned_final.copy()


# initiating the OFS DB
cnx = mc.connect(**config.db_access_testing)


# populate categories table
# categories = [(None, 'fruits'), (None, 'legumes'), (None, 'produits laitiers'), (None, 'viandes'),
#               (None, 'poissons'), (None, 'boissons'), (None, 'cereales'), (None, 'petit dej'),
#               (None, 'snacks')]
categories = ['fruits', 'legumes', 'produits laitiers', 'viandes', 'poissons', 'boissons', 'cereales', 'petit dej',
              'snacks']

add_category = ("INSERT INTO categories "
                "(categ_name) "
                "VALUES (%s)")

cursor = cnx.cursor()
data = []
for category in categories:
    data.append(category)
    try:
        cursor.execute(add_category, data)
    except mc.errors.IntegrityError as e:
        print("\n Categorie {} déjà existante. \n {}".format(category, e))
        continue
    else:
        print(" \n Insertion de la catégorie {}: OK. ".format(category))
    finally:
        data.pop()

cnx.commit()
cursor.close()


# find id for requested category
find_category_id = ("SELECT id FROM categories "
                    "WHERE categ_name = %s")

categ_search = ['snacks']

cursor_id = cnx.cursor(buffered=True)
cursor_id.execute(find_category_id, categ_search)
id_number = list(cursor_id.fetchone()).pop()  # get only the integer value of cursor_id
print("\n Pour la catégorie {}, l'id est {}.".format(categ_search, id_number))
cursor_id.close()

# ad category_id to every products in the dataset
for product in data_set:
    product.update({'category_id': id_number})


# populate products table
add_products = ("INSERT INTO products "
                "(category_id, product_name, url, image_url, nutrition_grade_fr, ingredients_text, allergens, "
                "stores, purchase_places) "
                "VALUES (%(category_id)s, %(product_name)s, %(url)s, %(image_url)s, %(nutrition_grade_fr)s, "
                "%(ingredients_text_fr)s, %(allergens)s, %(stores)s, %(purchase_places)s)")

cursor = cnx.cursor()
for product in data_set:
    try:
        cursor.execute(add_products, product)
    except mc.Error as e:
        print("\n {} n'a pas été ajouté à la table des produits suite à cette erreur: \n {}.".format(product['product_name'], e))
        continue
    else:
        print("\n {} a été ajouté à la table des produits.".format(product['product_name']))

cnx.commit()
cursor.close()


# search for a complete category type
search_criterion = list()
search_criterion.append(id_number)
search_category = ("SELECT id, product_name FROM products "
                   "WHERE category_id = %s "
                   "ORDER BY product_name")

cursor_category = cnx.cursor(dictionary=True, buffered=True)
cursor_category.execute(search_category, search_criterion)  # /!\ faire en sorte qu'il y est une liste en param !!!!

print("Voici les résultats de la requête de recherche pour cette categorie: \n ")
for row in cursor_category:
    print("* {product_name} --> choix: {id} \n".format(**row))

cursor_category.close()

# search details of a specific product
search_product = ("SELECT product_name, nutrition_grade_fr, ingredients_text, allergens, stores, "
                  "purchase_places, url, image_url, id, category_id "
                  "FROM products WHERE id = %s")

product_id = [39]
cursor_product = cnx.cursor(dictionary=True, buffered=True)
cursor_product.execute(search_product, product_id)

print("Voici les détails pour ce produit en particulier: \n ")
for row in cursor_product:
    print("* {product_name} - identifiant: {id} \n"
          "Nutriscore: {nutrition_grade_fr} \n"
          "Composition: {ingredients_text} \n"
          "Allergènes: {allergens} \n"
          "Lieux de vente: {stores} \n"
          "Plus d'infos: {url}".format(**row))

cursor_product.close()


# search for any product
search_all_products = ("SELECT product_name, products.id, categ_name AS categorie "
                       "FROM products INNER JOIN categories "
                       "ON products.category_id = categories.id "
                       "WHERE product_name LIKE %s "
                       "ORDER BY product_name")
name = ['Bis%']
cursor_product = cnx.cursor(dictionary=True, buffered=True)
cursor_product.execute(search_all_products, name)

print("Voici les résultats de votre recherche: \n ")
for row in cursor_product:
    print("* {product_name} - identifiant: {id} - catégorie: {categorie}\n".format(**row))

cursor_product.close()

# search for better graded product as a substitute
# TODO: comment insérer la catégorie de produit et le nutriscore ?
# TODO: comment sauvegarder le produit à substituer ?
search_substitute = ("SELECT product_name, nutrition_grade_fr, id "
                     "FROM products "
                     "WHERE  category_id = %(categ)s AND nutrition_grade_fr < %(score)s "
                     "ORDER BY nutrition_grade_fr, product_name")

replace_me = {'categ': 9, 'score': 'd'}

cursor_product = cnx.cursor(dictionary=True, buffered=True)
cursor_product.execute(search_substitute, replace_me)

print("Les subtituts possibles sont: \n ")
for row in cursor_product:
    print("* {product_name} - nutriscore: {nutrition_grade_fr} - identifiant: {id}\n".format(**row))

cursor_product.close()


