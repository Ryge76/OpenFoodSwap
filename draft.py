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
cursor = cnx.cursor()

# populate categories table
# categories = ['fruits', 'legumes', 'produits laitiers', 'viandes', 'poissons', 'boissons', 'cereales', 'petit dej',
#               'snacks']
#
# add_category = ("INSERT INTO categories "
#                 "VALUES (%s, %s)")
#
# # delete_categories = ("DELETE FROM categories")
# # cursor.execute(delete_categories)
#
# # for category in categories:
# #     cursor.execute(add_category, (None, category))
# #
# # cnx.commit()


# find id for requested category
find_category_id = ("SELECT id FROM categories "
                    "WHERE categ_name = %s")

categ_search = ['snacks']

cursor_id = cnx.cursor(buffered=True)
cursor_id.execute(find_category_id, categ_search)
id_number = list(cursor_id.fetchone()).pop()  # get only the integer value of cursor_id
print("\n Pour la catégorie {}, l'id est {}.".format(categ_search, id_number))

# ad category_id to every products in the dataset
for product in data_set:
    product.update({'category_id': id_number})

# print(data_set)

# populate products table
add_products = ("INSERT INTO products "
                "(category_id, product_name, url, image_url, nutrition_grade_fr, ingredients_text, allergens, "
                "stores, purchase_places) "
                "VALUES (%(category_id)s, %(product_name)s, %(url)s, %(image_url)s, %(nutrition_grade_fr)s, "
                "%(ingredients_text_fr)s, %(allergens)s, %(stores)s, %(purchase_places)s)")


for product in data_set:
    # cursor.execute(add_products, product)
    try:
        cursor.execute(add_products, product)
        print("{} a été ajouté à la table des produits.".format(product['product_name']))
    except mysql.connector.Error as e:
        print("{} n'a pas été ajouté à la table des produits suite à cette erreur: \n {}.".format(product['product_name']), e)

cnx.commit()



