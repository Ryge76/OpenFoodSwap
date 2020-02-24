import sys

import manageDB


class LineInterface:
    def __init__(self):
        self.db = manageDB.UseDB()
        self.action = manageDB.Command()
        self.main_options = {
            '1': self.search_product,
            '2': self.explore_category,
            '3': self.show_history,
            '4': self.quit
        }
        self.search_options = {
            '1': self.get_info,
            '2': self.find_substitute,
            '3': self.back_to_menu
        }

        self.substitute_options = {
            '1': self.find_substitute,
            '2': self.back_to_menu
        }

        self.record_options = {
            '1': self.record_substitute,
            '2': self.get_info,
            '3': self.back_to_menu
        }

        self.categ_options = {}
        self.source_product_id = ''
        self.categ_choice = ''
        self.categories = ['fruits', 'legumes-et-derives', 'produits-laitiers', 'viandes', 'poissons',
                           'boissons', 'aliments-et-boissons-a-base-de-vegetaux', 'petit-dejeuners', 'snacks']

    @staticmethod
    def quit():
        """Exit application."""
        print("\n A bientôt !")
        sys.exit(0)

    @staticmethod
    def check_type(var):
        """Control that the user input is an integer.
        Return False to stop the initial while loop."""
        try:
            int(var)
        except ValueError:
            print("\n Merci de ne saisir que des chiffres. Essayez à nouveau.")
            return True
        return False

    @staticmethod
    def display_menu():
        print("""
        --------------------------------
                Menu Principal
        --------------------------------
                
        Voici les actions possibles

        1- Rechercher des informations sur un aliment en particulier
        2- Explorer une catégorie d'aliments
        3- Consulter l'historique de vos substitutions
        4- Quitter l'application """)

    @staticmethod
    def display_search_submenu():
        print("""
        Vous pouvez:
            1- obtenir plus d'infos sur un produit en particulier
            2- chercher un substitut
            3- revenir au menu principal 
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
            2- obtenir plus d'infos sur un produit
            3- revenir au menu principal 
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
        """Get user to select an action in a specific range of options."""

        possible_keys = list(possibilities.keys())
        choice = ''
        while choice not in possibilities:
            choice = input("\n Que voulez vous faire ? choix possibles {}:  ".format(possible_keys))

        if possibilities == self.categ_options:
            self.categ_choice = choice

        act = possibilities.get(choice)
        act()

    def welcome(self):
        """Display welcome screen. Call for the main menu."""

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
        """Handle search on any product."""
        search = input("\n Tapez les premières lettres ou le nom complet de l'aliment que vous recherchez:  ")

        results = self.action.search_any_product(self.db, search)

        if results is None:
            print("\n Echec de la commande de recherche.")
            return

        elif results.rowcount == 0:
            print("\n Aucun résultat pour {}".format(search))
            return

        else:
            print("\n Voici les résultats de votre recherche sur '{}': \n ".format(search))
            for row in results:
                print("""
                * {product_name}
                    nutriscore: {nutrition_grade_fr} 
                    identifiant: {id} 
                    catégorie: {categorie} \n""".format(**row))

        self.display_search_submenu()
        self.choice(self.search_options)

    def get_info(self):
        """Handle information search on a product."""

        control = True
        while control:
            search = input("\n Tapez l'identifiant de l'aliment pour lequel vous souhaitez plus d'information:  ")

            # check validity of input. Integer expected.
            control = self.check_type(search)

        results = self.action.find_item_description(self.db, search)

        if results is None:
            print("\n Echec de la commande de recherche. Essayez à nouveau.")
            self.get_info()

        elif results.rowcount == 0:
            print("Mmmh, nous ne trouvons pas d'information sur le produit {}...".format(search))
            return

        print("\n Voici les détails pour ce produit en particulier: \n ")

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
        """Handle search for substitution.
        Use source_product_id attribute to store initial product id.
        Call record menu if successful."""

        control = True
        while control:
            search = input("Tapez l'identifiant du produit pour lequel vous voulez un substitut: ")

            # check validity of input. Integer expected.
            control = self.check_type(search)

        self.source_product_id = search

        # gather information needed about source product (category id and score)
        source_info = self.action.find_item_description(self.db, search)

        if source_info is None:
            print("Le produit {} ne semble pas exister. Ressayez à nouveau".format(search))
            self.find_substitute()

        elif source_info.rowcount == 0:
            print("Le produit {} ne semble pas exister. Ressayez à nouveau".format(search))
            self.find_substitute()

        for row in source_info:
            category_id = row['category_id']
            product_score = row['nutrition_grade_fr']

        # make the actual search for substitute product.
        results = self.action.search_substitute(self.db, product_score, category_id)

        if results is None:
            print("\n Echec de la commande de recherche")
            return

        elif results.rowcount == 0:
            print("\n Il n'y a pas d'alternatives mieux classées pour le produit {} à notre connaissance".format(search))
            return

        print("\n Les subtituts possibles, de la même catégorie et avec un meilleur nutriscore, sont: \n")

        for row in results:
            print("""
            * {product_name} - nutriscore: {nutrition_grade_fr} - identifiant: {id}\n""".format(**row))

        self.display_record_submenu()
        self.choice(self.record_options)

    def record_substitute(self):
        """Handle recording of substitution.
        Require source_product_id attribute."""
        id_source = self.source_product_id

        control = True
        while control:
            id_sub = input("Quel est l'identifiant du substitut que vous voulez conserver ?: ")

            # check validity of input. Integer expected.
            control = self.check_type(id_sub)

        data = [id_source, id_sub]
        self.action.add_substitute(self.db, data)

        print("""
            Préférence enregistrée avec succès ! 
        Vous pouvez la retrouver en consultant l'historique (menu principal -> consulter l'historique """)

    def explore_category(self):
        """Handle options menu for category search."""
        self.display_categ_submenu()

        # populate dictionary of categories options if empty
        if len(self.categ_options) != (len(self.categories)+1):
            for i in range(1, (len(self.categories)+1)):   # try to populate options dictionary
                key = str(i)
                self.categ_options.setdefault(key, self.show_category)

            last_key = str(len(self.categories)+1)
            self.categ_options.setdefault(last_key, self.back_to_menu)

        self.choice(self.categ_options)

    def show_category(self):
        """Show results of the queries for a specified category of products.
        Rely on categ_choice et categorie attributes to work.
        If the query is succesfull, call for function to show details on a specific product."""
        index = int(self.categ_choice)-1
        look_for = self.categories[index]

        results = self.action.find_by_category(self.db, look_for)

        if results is None:
            print("\n Echec de la commande de recherche.")
            return

        elif results.rowcount == 0:
            print("Aucun résultat pour {}".format(look_for))
            return

        else:
            print("\n Voici les résultats pour la catégorie '{}': \n ".format(look_for))
            for row in results:
                print("""* {product_name} -- Nutriscore: {nutrition_grade_fr}  -- Identifiant: {id} \n""".format(**row))

        self.display_search_submenu()
        self.choice(self.search_options)

    def show_history(self):
        """Show records of substitutions."""
        results = self.action.show_all_substitutes(self.db)

        if results is None:
            print("\n Echec de la commande de recherche.")
            return

        elif results.rowcount == 0:
            print("\n L'historique ne contient aucun enregistrement pour l'instant. \n")
            return

        else:
            print("\n Voici les substitutions déja enregistrées jusqu'ici: ")
            for row in results:
                print("""
        * SUBTITUTION du {subs_date}
                ALIMENT DE BASE   {source} -- Nutriscore: {nutrition_grade_fr}  -- Identifiant: {id}
                    >> SUBSTITUT   {substitut} -- Nutriscore: {nutriscore}  -- Identifiant: {id_sub}""".format(**row))

        # display search options
        self.display_search_submenu()
        self.choice(self.search_options)

    def run(self):
        """Initiate main loop and show the main menu."""
        while True:
            self.display_menu()
            self.choice(self.main_options)


def main():
    LineInterface().welcome()


if __name__ == '__main__':
    main()






