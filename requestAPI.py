import requests


class FoodAPI:
    def __init__(self):
        """defining base url and parameters for using OpenFoodFacts API"""
        self.url = 'https://fr.openfoodfacts.org./cgi/search.pl'
        self.param = {'action': 'process', 'tagtype_0': 'categories', 'tag_contains_0': 'contains', 'tag_0': '',
                        'sort_by': 'unique_scans_n', 'page_size': '', 'json': 'true', 'fields':
                            'product_name,image_url,nutrition_grade_fr,purchase_places,stores,url,ingredients_text_fr,allergens'}
        self.json = {}

    def call_for(self, categ, qt='10'):
        """API call for a specific category"""
        self.param['tag_0'] = categ
        self.param['page_size'] = qt

        try:  # TODO: look for better handling of ConnectionError (requests.exceptions.ConnectionError)
            r = requests.get(self.url, params=self.param)
            assert r.ok  # check status 200 for the request
        except AssertionError:
            print('Echec de de la requête, avec code status HTTP {}'.format(r.status_code))

        else:
            print('Requête correctement effectuée vers \n {}'.format(r.url))
            self.json = r.json()


def main(categ, qt='10'):
    API = FoodAPI()
    API.call_for(categ, qt)
    print(API.json)


if __name__ == '__main__':
    main('snack')









