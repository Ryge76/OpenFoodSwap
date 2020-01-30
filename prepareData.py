
class Parser:
    """Contains the logic to parse data received from the API.
    Require a FoodAPI object."""

    MANDATORY_KEYS = ['product_name', 'url', 'nutrition_grade_fr', 'ingredients_text_fr', 'stores',
                      'purchase_places']

    def __init__(self, data):
        self.criteria = data.param['fields'].split(',')  # getting list of criteria
        self.products_list = data.json['products']  # getting list of product
        self.final_result = []

    @staticmethod
    def check_value(dic, *args, value=''):
        """Check if the mandatory keys in a product, has a defined value.
        Return True if the specified value is found"""
        key_ring = list(args) + Parser.MANDATORY_KEYS
        for key in key_ring:
            if dic[key] == value:
                print("La valeur de la clé '{}' est manquante sur le produit '{}'".format(key, dic['product_name']))
                return True

    @staticmethod
    def find_invalid_value(p_list):
        """Find product with no values for mandatory keys.
        Return list of indexes of products with incorrect values."""
        to_delete = []  # list of indexes of incorrect products

        for product in p_list:
            control = Parser.check_value(product)
            if control:
                index = p_list.index(product)
                to_delete.append(index)

        print("Index des produits à supprimer: \n {} \n".format(to_delete))
        return to_delete

    def prepare_data(self):
        """Implements the parsing logic with successive calls to internal methods"""
        print("Le jeu initial de données contient {} produits. \n".format(len(self.products_list)))

        incorrect_idx = Parser.find_incorrect_product(self, self.products_list)  # step 1: identifying index of incomplete products
        complete_products_only = Parser.delete_incorrect(self, incorrect_idx)  # step 2: remove unwanted products
        incorrect_idx = Parser.find_invalid_value(complete_products_only)  # step 3: identifying index of products with invalid values
        self.final_result = Parser.delete_incorrect(self, incorrect_idx)  # step 4 = step 2

        print("Le jeu final de données contient {} produits. \n".format(len(self.final_result)))

        return self.final_result

    def find_incorrect_product(self, p_list):
        """Look for products in a list of products that haven't got the correct number of criteria.
        Return a list of indexes."""
        to_delete = []  # list of indexes of incorrect products

        for i in range(len(p_list)):  # iterating the product list
            if len(p_list[i]) < len(self.criteria):
                print("Produit(s) non conforme(s): \n {} \n".format(p_list[i]))
                to_delete.append(i)

        print("Index des produits à supprimer: \n {} \n".format(to_delete))
        return to_delete

    def delete_incorrect(self, index_list):
        """Suppress products from the products list based on the index list.
        Return a list of products."""
        index_list.sort(reverse=True)  # sort index in desc order for proper use with str.pop() method
        for i in index_list:
            self.products_list.pop(i)
        print("Les produits ont correctement été supprimés. \n")
        return self.products_list


def main():
    # creating a FoodAPI object required to use Parser
    from requestAPI import FoodAPI
    data_set = FoodAPI()
    data_set.call_for('snack', qt='50')

    # parsing data
    parser = Parser(data_set)
    cleaned_data = parser.prepare_data()
    print(cleaned_data)


if __name__ == '__main__':
    main()




