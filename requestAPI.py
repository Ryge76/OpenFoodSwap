import requests


class FoodAPI:
    def __init__(self):
        """defining the base url and parameters for using OpenFoodFacts API"""
        self.url = 'https://fr.openfoodfacts.org./cgi/search.pl'
        self.param = {'action': 'process', 'tagtype_0': 'categories', 'tag_contains_0': 'contains', 'tag_0': '',
                        'sort_by': 'unique_scans_n', 'page_size': '', 'json': 'true', 'fields':
                            'product_name,image_url,nutrition_grade_fr,purchase_places,stores,url,ingredients_text_fr,allergens'}
        self.json = {}

    def call_for(self, categ, qt='10'):
        """API call for a specific category. Require a 'categ' param (which corresponds to the category of food
        that is queried and) a 'qt' param (qt for quantity of products for the queried category)."""
        self.param['tag_0'] = categ
        self.param['page_size'] = qt

        try:
            r = requests.get(self.url, params=self.param)
        except ConnectionError:
            raise ConnectionError("Echec de de la requête: problème de connexion on dirait...")

        assert r.ok, "Echec de de la requête, avec code status HTTP {}".format(r.status_code)  # check status 200 for the request
        print("Requête correctement effectuée vers: \n {} \n".format(r.url))

        self.json = r.json()


def main(categ, qt='10'):
    api = FoodAPI()
    api.call_for(categ, qt)
    print("Voici le json récupéré: \n {}".format(api.json))


if __name__ == '__main__':
    main('snack')
