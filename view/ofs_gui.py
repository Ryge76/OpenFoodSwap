import tkinter as t

import OpenFoodsSwap.manageDB as manageDB


class Ofs(t.Tk):
    """OpenFood Swap GUI. """
    def __init__(self):
        self.db = DbAction()
        super().__init__()
        self.title("OpenFood SWAP")

        self.frames = {
            '1': self.welcome_screen,
            '2': self.main_menu_screen,
        }
        self.on_screen = []

        self.load_menu()

        self.start()  # initiate first view
        pass

    def load_menu(self):
        pass

    def show_next(self, frame='2'):
        """Destroy displayed view and show next view."""

        # destroy displayed view
        self.on_screen[0].destroy()
        self.on_screen.pop()

        next_frame = self.frames.get(frame)
        self.display_frame(next_frame)

    def displayed_frame(self, frame):
        """Store name of the view displayed."""
        self.on_screen.append(frame)

    @staticmethod
    def display_frame(frame):
        frame()

    def start(self):
        self.display_frame(self.welcome_screen)

    def run(self):
        self.mainloop()
        self.start()

    def create_menu(self):
        """Create the menu bar for the application."""
        menubar = t.Menu(self)

        menu_action = t.Menu(menubar, tearoff=0)
        menu_action.add_command(label="Rechercher un produit",
                                command=self.search_screen)
        menu_action.add_command(label="Explorer une catégorie",
                                command=self.category_screen)
        menu_action.add_command(label="Voir les substitutions précédentes",
                                command=self.history_screen)
        menu_action.add_command(label="Quitter", command=self.destroy)
        menubar.add_cascade(label="Actions", menu=menu_action)

        self.config(menu=menubar)

    def welcome_screen(self):
        """Create welcome frame. """

        welcome_frame = t.Frame(width=1024, height=768, background='yellow')
        welcome_frame.pack()

        self.displayed_frame(welcome_frame)

        welcome = t.Label(welcome_frame, text="""
        Bienvenue dans OpenFood SWAP !""", fg='blue')
        welcome.pack(side='top', fill=t.BOTH)

        sub_welcome = t.Label(welcome_frame, text="""
        Cette application vous permet d'avoir des infos sur ce que vous 
        consommez, et de trouver éventuellement 
        des équivalents plus sains ! ;-)
        """)
        sub_welcome.pack()

        start_button = t.Button(welcome_frame, text="Cliquez pour commencer !",
                                fg='green', command=self.show_next)
        start_button.pack(side="bottom", fill=t.BOTH)

    def main_menu_screen(self):
        """Create main menu option screen"""

        self.create_menu()

        option_menu = t.Frame(width=1024, height=768, background='blue')
        option_menu.pack(fill=t.BOTH)

        self.displayed_frame(option_menu)

        # create menu option with radio button.
        choice = t.IntVar()
        choice_menu_1 = t.Radiobutton(
            option_menu,
            text="Rechercher des informations sur un aliment en particulier",
            variable=choice, value=1)
        choice_menu_1.pack(fill=t.BOTH)

        choice_menu_2 = t.Radiobutton(option_menu,
                                      text="Explorer une catégorie d'aliments",
                                      variable=choice, value=2)
        choice_menu_2.pack(fill=t.BOTH)

        choice_menu_3 = t.Radiobutton(
            option_menu, text="Consulter l'historique de vos substitutions",
            variable=choice, value=3)
        choice_menu_3.pack(fill=t.BOTH)

        choice_menu_4 = t.Radiobutton(
            option_menu, text="Quitter l'application",
            variable=choice, value=4)
        choice_menu_4.pack(fill=t.BOTH)

    def search_screen(self):
        pass

    def category_screen(self):
        pass

    def history_screen(self):
        pass

    def quit(self):
        pass


class DbAction:
    def __init__(self):
        self.db = manageDB.UseDB()
        self.action = manageDB.Command()

    def search_product(self):
        """Handle search on any product."""
        search = input("\n Tapez les premières lettres ou le nom complet de "
                       "l'aliment que vous recherchez:  ")

        results = self.action.search_any_product(self.db, search)

        if results is None:
            print("\n Echec de la commande de recherche.")
            return

        elif results.rowcount == 0:
            print("\n Aucun résultat pour {}".format(search))
            return

        else:
            print("\n Voici les résultats de votre recherche sur "
                  "'{}': \n ".format(search))
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
            search = input("\n Tapez l'identifiant de l'aliment pour lequel "
                           "vous souhaitez plus d'information:  ")

            # check validity of input. Integer expected.
            control = self.check_type(search)

        results = self.action.find_item_description(self.db, search)

        if results is None:
            print("\n Echec de la commande de recherche. Essayez à nouveau.")
            self.get_info()

        elif results.rowcount == 0:
            print("Mmmh, nous ne trouvons pas d'information sur le produit "
                  "{}...".format(search))
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
            search = input("Tapez l'identifiant du produit pour lequel vous"
                           " voulez un substitut: ")

            # check validity of input. Integer expected.
            control = self.check_type(search)

        self.source_product_id = search

        # gather information needed about source product (category id and score)
        source_info = self.action.find_item_description(self.db, search)

        if source_info is None:
            print("Le produit {} ne semble pas exister. Ressayez à "
                  "nouveau".format(search))
            self.find_substitute()

        elif source_info.rowcount == 0:
            print("Le produit {} ne semble pas exister. Ressayez à "
                  "nouveau".format(search))
            self.find_substitute()

        for row in source_info:
            category_id = row['category_id']
            product_score = row['nutrition_grade_fr']

        # make the actual search for substitute product.
        results = self.action.search_substitute(self.db, product_score,
                                                category_id)

        if results is None:
            print("\n Echec de la commande de recherche")
            return

        elif results.rowcount == 0:
            print("\n Il n'y a pas d'alternatives mieux classées pour "
                  "le produit {} dans notre base de données.".format(search))
            return

        print("\n Les subtituts possibles, de la même catégorie et avec un "
              "meilleur nutriscore, sont: \n")

        for row in results:
            print("""
            * {product_name} - nutriscore: {nutrition_grade_fr} - identifiant: 
            {id}\n""".format(**row))

        self.display_record_submenu()
        self.choice(self.record_options)

    def record_substitute(self):
        """Handle recording of substitution.
        Require source_product_id attribute."""
        id_source = self.source_product_id

        control = True
        while control:
            id_sub = input("Quel est l'identifiant du substitut que vous "
                           "voulez conserver ?: ")

            # check validity of input. Integer expected.
            control = self.check_type(id_sub)

        data = [id_source, id_sub]
        self.action.add_substitute(self.db, data)

        print("""
            Préférence enregistrée avec succès ! 
        Vous pouvez la retrouver en consultant l'historique (menu principal -> consulter l'historique) """)

    def explore_category(self):
        """Handle options menu for category search."""
        self.display_categ_submenu()

        # populate dictionary of categories options if empty
        if len(self.categ_options) != (len(self.categories) + 1):

            # try to populate options dictionary
            for i in range(1, (len(self.categories) + 1)):
                key = str(i)
                self.categ_options.setdefault(key, self.show_category)

            last_key = str(len(self.categories) + 1)
            self.categ_options.setdefault(last_key, self.back_to_menu)

        self.choice(self.categ_options)

    def show_category(self):
        """Show results of the queries for a specified category of products.
        Rely on categ_choice et categorie attributes to work.
        If the query is succesfull, call for function to show details on a
        specific product."""
        index = int(self.categ_choice) - 1
        look_for = self.categories[index]

        results = self.action.find_by_category(self.db, look_for)

        if results is None:
            print("\n Echec de la commande de recherche.")
            return

        elif results.rowcount == 0:
            print("Aucun résultat pour {}".format(look_for))
            return

        else:
            print("\n Voici les résultats pour la catégorie '{}': "
                  "\n ".format(look_for))
            for row in results:
                print("""* {product_name} -- Nutriscore: {nutrition_grade_fr} 
                 -- Identifiant: {id} \n""".format(**row))

        self.display_search_submenu()
        self.choice(self.search_options)

    def show_history(self):
        """Show records of substitutions."""
        results = self.action.show_all_substitutes(self.db)

        if results is None:
            print("\n Echec de la commande de recherche.")
            return

        elif results.rowcount == 0:
            print("\n L'historique ne contient aucun enregistrement pour "
                  "l'instant. \n")
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

def main():
    app = Ofs()
    app.run()


if __name__ == '__main__':
    main()
