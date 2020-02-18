import sys

import manageDB


class LineInterface:
    def __init__(self):
        self.db = manageDB.UseDB()
        self.action = manageDB.Command()
        self.main_options = {
            '1': self.search_product,
            '2': self.explore_category,
            '4': self.quit
        }
        self.search_options = {
            '1': self.get_info,
            '2': self.back_to_menu
        }

        self.substitute_options = {
            '1': self.find_substitute,
            '2': self.back_to_menu
        }

        self.record_options = {
            '1': self.record_substitute,
            '2': self.back_to_menu
        }

        self.categ_options = {}
        self.source_product_id = ''
        self.categ_choice = ''
        self.categories = ['fruits', 'legumes-et-derives', 'produits-laitiers', 'viandes', 'poissons',
                           'boissons', 'aliments-et-boissons-a-base-de-vegetaux', 'petit-dejeuners', 'snacks']

    @staticmethod
    def quit():
        print("\n A bientôt !")
        sys.exit(0)

    @staticmethod
    def display_menu():
        print("""
        --------------------------------
                Menu Principal
        --------------------------------
                
        Voici les actions possibles

        1- Rechercher des informations sur un aliment en particulier
        2- Explorer une catégorie d'aliment
        3- Consulter l'historique de vos substitutions
        4- Quitter l'application """)

    @staticmethod
    def display_search_submenu():
        print("""
        Vous pouvez:
            1- obtenir plus d'infos sur un produit en particulier
            2- revenir au menu principal 
        """)

    @staticmethod
    def display_substitute_submenu():
        print("""
        Vous pouvez:
            1- trouver un substitut
            2- revenir au menu principal 
        """)

    @staticmethod
    def display_record_submenu():
        print("""
        Vous pouvez:
            1- enregistrer un subtitut pour le retrouver plus tard (menu principal -> historique)
            2- revenir au menu principal 
        """)

    def display_categ_submenu(self):
        print("""
        Voici les options possibles: """)

        # create texte of options based on what is in self.categories
        options = list(enumerate(self.categories, start=1))
        for c in options:
            print("""
            {0[0]}- {0[1]}""".format(c))

        # add a last choice
        print("""
            {a}- {b}""".format(a=(len(self.categories)+1), b='revenir au menu principal'))

    def choice(self, possibilities):

        # special case for categories
        if possibilities == self.categ_options:

            for i in range(1, (len(self.categories)+1)):   # try to populate options dictionary
                key = str(i)
                self.categ_options.get(key, self.show_category)
            last_key = str(len(self.categories)+1)
            self.categ_options.get(last_key, self.back_to_menu)

            possibilities = self.categ_options  # FIXME

        print(self.categ_options)

        possible_keys = list(possibilities.keys())
        choice = ''
        while choice not in possibilities:
            choice = input("\n Que voulez vous faire ? choix possibles {}:  ".format(possible_keys))

        act = possibilities.get(choice)
        act()

    def welcome(self):
        print("""
        -----------------------------
        Bienvenue dans OpenFoodSWAP !
        ----------------------------- 
        Cette application vous permet d'avoir des infos sur ce que vous
        consommez, et de trouver éventuellement des équivalents plus sains ! ;-)
        """)
        self.run()

    def back_to_menu(self):
        """Go back to main run() loop"""
        pass

    def search_product(self):
        search = input("\n Tapez les premières lettres ou le nom complet de l'aliment que vous recherchez:  ")
        results = self.action.search_any_product(self.db, search)

        if results is None:
            print("\n Echec de la commande de recherche.")
            self.search_product()

        elif results.rowcount == 0:
            print("Aucun résultat pour {}".format(search))

        else:
            print("\n Voici les résultats de votre recherche sur '{}': \n ".format(search))
            for row in results:
                print("""
                * {product_name}
                    nutriscore: {nutrition_grade_fr} 
                    identifiant: {id} 
                    catégorie: {categorie}
                    \n""".format(**row))

        self.display_search_submenu()
        self.choice(self.search_options)

    def get_info(self):
        search = input("\n Tapez l'identifiant de l'aliment pour lequel vous souhaitez plus d'information:  ")
        results = self.action.find_item_description(self.db, search)

        if results is None:
            print("\n Echec de la commande de recherche.")
            self.search_product()  # FIXME Loop Branch out. Prevent function from being generic

        print("Voici les détails pour ce produit en particulier: \n ")

        for row in results:
            print("""
            {product_name} - identifiant: {id}
            Nutriscore: {nutrition_grade_fr}
            Composition: {ingredients_text}
            Allergènes: {allergens}
            Lieux de vente: {stores}
            
            Plus d'infos: {url}""".format(**row))

        self.display_substitute_submenu()
        self.choice(self.substitute_options)

    def find_substitute(self):
        search = input("Tapez l'identifiant du produit pour lequel vous voulez un substitut: ")

        self.source_product_id = search

        source_info = self.action.find_item_description(self.db, search)

        if source_info is None:
            print("\n Echec de la commande de recherche")

        for row in source_info:
            category_id = row['category_id']
            product_score = row['nutrition_grade_fr']

        results = self.action.search_substitute(self.db, product_score, category_id)

        print("\n Les subtituts possibles sont: \n")

        for row in results:
            print("""
            * {product_name} - nutriscore: {nutrition_grade_fr} - identifiant: {id}\n""".format(**row))

        self.display_record_submenu()
        self.choice(self.record_options)

    def record_substitute(self):
        id_source = self.source_product_id

        id_sub = input("Quel est l'identifiant du substitut que vous voulez conserver ?: ")

        data = [id_source, id_sub]
        self.action.add_substitute(self.db, data)

    def explore_category(self):
        self.display_categ_submenu()
        self.choice(self.categ_options)

    def show_category(self):
        pass

    def run(self):
        while True:
            self.display_menu()
            self.choice(self.main_options)
            # choice = ''
            # while choice not in self.options.keys():
            #     choice = input("\n Que voulez vous faire ? (choisissez entre 1 et 4): ")
            #
            # act = self.options.get(choice)
            # act()


if __name__ == '__main__':
    LineInterface().welcome()



