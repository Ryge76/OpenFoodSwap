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

products = r_json['products']
items = r_param['fields']
