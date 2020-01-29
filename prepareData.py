import requests

url = 'https://fr.openfoodfacts.org./cgi/search.pl'
r_param = {'action': 'process', 'tagtype_0': 'categories', 'tag_contains_0': 'contains', 'tag_0': 'snack',
           'sort_by': 'unique_scans_n', 'page_size': '10', 'json': 'true', 'fields':
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
print(products_list)

criteria = r_param['fields'].split(',')  # getting a list of criteria from the 'fields' parameter
print("{a} critères retenus par produit. \n {b}. \n".format(a=len(criteria), b=criteria))

# todelete = []
# for i in range(len(products_list)):
#     if '' in products_list[i].values():
#         print("Le produit '{}', contient une ou plusieurs données manquantes".format(products_list[i]['product_name']))
#         todelete.append(i)
#         print("Il est enlevé de la liste pour cette raison. \n {}".format(products_list.pop(i)))
products_dict = {products_list}

for product in products_dict:
    if '' in product.values():
        print("Le produit '{}', contient une ou plusieurs données manquantes".format(product['product_name']))
        del product



print("Nombre de produits final: {}".format(len(products_list)))
print("Index des produits à supprimer: {}".format(todelete))
print(products_list)

# # reject any product without defined criteria
# for i in range(len(products_list)):
#     if len(products_list[i]) < len(criteria):
#         print("Produit(s) non conforme(s): \n {}".format(products_list[i]))
#         del products_list[i]
# print("Nombre de produits final: {}".format(len(products_list)))
# print(products_list)

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

# reject any product without mandatory keys
# mandatory_keys = ['product_name', 'url', 'nutrition_grade_fr', 'ingredients_text_fr', 'stores', 'purchase_places']
