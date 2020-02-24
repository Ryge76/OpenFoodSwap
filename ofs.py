import argparse

import manageDB
import prepareData
import requestAPI
import view.ofs_gui as vg
import view.cli as vc


def populate_db():
    """Populate local database with products."""
    # create connexion to application's database
    db = manageDB.UseDB()

    # create query handler
    action = manageDB.Command()

    # Requesting OFF API for  different food categories
    data_set = requestAPI.FoodAPI()

    categories = ['fruits', 'legumes-et-derives', 'produits-laitiers',
                  'viandes', 'poissons', 'boissons',
                  'aliments-et-boissons-a-base-de-vegetaux', 'petit-dejeuners',
                  'snacks']

    for category in categories:
        data_set.call_for(category, qt='100')

        # prepare data before populating the database
        parser = prepareData.Parser(data_set)
        cleaned_data = parser.prepare_data()

        # add category in database 'categories' table and get it's id
        action.add_categories(db, category)
        category_id = action.find_category_id(db, category)

        # add category id number to each product of the cleaned data set \
        # before insertion in app's database
        for product in cleaned_data:
            product.update(category_id=category_id)
            action.add_products(db, product)


def install():
    """Manage first installation."""
    populate_db()
    with open("./ready.txt", 'w') as f:
        f.write("Install done !")


def user_choice():
    """Allow user to choose between CLI and GUI."""
    options = {
        '1': vc.main,
        '2': vg.main
    }

    choices = list(options.keys())

    choice = ''
    while choice not in choices:
        choice = input("""
                Voulez-vous lancer le programme:
                1. en ligne de commande
                2. en interface graphique

                Votre choix (parmi {}) : """.format(choices))

    action = options.get(choice)
    action()


def create_options():
    """Create argument to run script in CLI, GUI or install mode"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--GUI", "-G",
                        help="Launch the program with GUI",
                        action="store_true")
    parser.add_argument("-i", "--install", help="Remplissage initial de la"
                                                "base de données.",
                        action="store_true")
    args = parser.parse_args()

    return args


def main():
    args = create_options()

    if args.install:
        print("Je fais l'installation")
        # install()
        # user_choice()

    elif args.GUI:
        # lancer interface graphique
        print("Je lance l'interface graphique !")
        vg.main()

    else:
        print("Je lance l'interface en ligne de commande")
        vc.main()


if __name__ == '__main__':
    main()
