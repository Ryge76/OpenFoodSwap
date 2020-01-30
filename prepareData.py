import requests

url = 'https://fr.openfoodfacts.org./cgi/search.pl'
r_param = {'action': 'process', 'tagtype_0': 'categories', 'tag_contains_0': 'contains', 'tag_0': 'snack',
           'sort_by': 'unique_scans_n', 'page_size': '30', 'json': 'true', 'fields':
               'product_name,image_url,nutrition_grade_fr,purchase_places,stores,url,ingredients_text_fr,allergens'}

try:
    r = requests.get(url, params=r_param)
    assert r.ok
except AssertionError:
    print('Echec de de la requête, avec code status HTTP {}'.format(r.status_code))

else:
    print('Requête correctement effectuée. \n {}'.format(r.url))
    r_json = r.json()

products_list = r_json['products']
products_list.append(dict({'product_name': 'test', 'nutrition_grade_fr': ''}))  # faux produit pour test

print("Nombre de produits initial: {}".format(len(products_list)))  # test
# print(products_list)


class Parser:
    """Contains the logic to parse data received from the API.
    Require a FoodAPI object."""
    def __init__(self, data):
        self.criteria =


# reject any product without defined criteria
def find_incorrect(p_list):
    """Look for products that haven't got the correct number of criteria. """
    criteria = r_param['fields'].split(',')  # list of criteria
    to_delete = []  # list of indexes of incorrect products
    for i in range(len(p_list)):
        if len(p_list[i]) < len(criteria):
            print("Produit(s) non conforme(s): \n {}".format(p_list[i]))
            to_delete.append(i)
    to_delete.sort(reverse=True)
    print("Index des produits à supprimer: \n {}".format(to_delete))
    return to_delete


incorrect = find_incorrect(products_list)

for index in incorrect:
    products_list.pop(index)

print("La liste finale comporte {} produits. \n {}".format(len(products_list), products_list))

search = [product for product in products_list if product['product_name'] == 'Benco original']
print("Résultat de la recherche du produit 'Benco Original': {}".format(search))
'''
TODO: vérifier que la liste criteria fonctionne et qu'on peut éliminer les produits incomplets
TODO: faire une séquence cohérente pour traiter les données. Quelle classe ? Quelles méthodes ? Quel enchainement ?
Peut être créer une classe ParseData, puis faire des appels de méthodes dessus.
'''

print("Nombre de produits final: {}".format(len(products_list)))
print(products_list)

# # eliminating all products with blank value
# for product in products_list:
#     if '' in product.values():
#         print("Le produit '{}', contient une ou plusieurs données manquantes".format(product['product_name']))
#         print(product)
#         products_list.remove(product)


# reject any product without mandatory keys
def check_keys(dic):
    """Check if the mandatory keys in a product, has a defined value."""
    mandatory_keys = ['product_name', 'url', 'nutrition_grade_fr', 'ingredients_text_fr', 'stores', 'purchase_places']
    for key in mandatory_keys:
        if dic[key] == '':
            print("La valeur de la clé '{}' est manquante sur le produit '{}'".format(key, dic['product_name']))
            return True


for product in products_list:
    control = check_keys(product)
    if control:
        products_list.remove(product)

print("Nombre de produits final: {}".format(len(products_list)))

print(products_list)

# # checking if test product and another were eliminated
# erased_values = ['test', 'Fourrés Chocolat noir BIO']
# final = [product.values() for product in products_list]
#
# for v in erased_values:
#     if v in final:
#         print("oho...")
#     else:
#         print("Perfect !")



# # reject any product without a specific value for every specific criterion
# incorrect_items = []
# for i in range(len(products_list)):
#     temp = products_list[i].values()
#     if '' in temp:
#         print("Ce produit a été retiré: \n {}".format(products_list[i]))
#         incorrect_items.append(i)
#
# for item in incorrect_items:
#     del products_list[item]  # ne peux pas supprimer successivement sur les index car ceux ci changent !
#
# print("Nombre de produits final: {}".format(len(products_list)))
# print(products_list)


