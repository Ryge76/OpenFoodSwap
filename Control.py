import argparse

import manageDB
import prepareData
import requestAPI


def populate_db():
    # create connexion to application's database
    db = manageDB.UseDB()

    # create query handler
    action = manageDB.Command()

    # Requesting OFF API for  different food categories
    data_set = requestAPI.FoodAPI()

    categories = ['fruits', 'legumes-et-derives', 'produits-laitiers', 'viandes', 'poissons', 'boissons',
                  'aliments-et-boissons-a-base-de-vegetaux', 'petit-dejeuners', 'snacks']

    for category in categories:
        data_set.call_for(category, qt='100')

        # prepare data before populating the database
        parser = prepareData.Parser(data_set)
        cleaned_data = parser.prepare_data()

        # add category in database 'categories' table and get it's id
        action.add_categories(db, category)
        category_id = action.find_category_id(db, category)

        # add category id number to each product of the cleaned data set before insertion in app's database
        for product in cleaned_data:
            product.update(category_id=category_id)
            action.add_products(db, product)


def create_options():
    # fn de gestion d'argument pour choix CLI ou GUI
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--GUI", "-G", help="Launch the program with GUI", action="store_true")
    args = parser.parse_args()

    if args.GUI:
        # lancer interface graphique
        pass

    # lancer CLI


def main():
    create_options()


if __name__ == '__main__':
    main()





