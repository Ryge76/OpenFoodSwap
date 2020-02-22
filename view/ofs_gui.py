import tkinter as t


class Ofs(t.Tk):
    """OpenFood Swap GUI. """
    def __init__(self):
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

    def welcome_screen(self):
        """Create welcome screen. """

        welcome_frame = t.Frame(width=1024, height=768, background='yellow')
        welcome_frame.pack()

        self.displayed_frame(welcome_frame)

        welcome = t.Label(welcome_frame, text="""
        Bienvenue dans OpenFood SWAP !""", fg='blue')
        welcome.pack(side='top', fill=t.BOTH)

        sub_welcome = t.Label(welcome_frame, text="""Cette application vous permet d'avoir des infos sur ce que vous consommez,
        et de trouver éventuellement des équivalents plus sains ! ;-)
        """)
        sub_welcome.pack()

        start_button = t.Button(welcome_frame, text="Cliquez pour commencer !", fg='green', command=self.show_next)
        start_button.pack(side="bottom", fill=t.BOTH)

    def main_menu_screen(self):
        """Create main menu option screen"""

        option_menu = t.Frame(width=1024, height=768, background='blue')
        option_menu.pack(fill=t.BOTH)

        self.displayed_frame(option_menu)

        # create menu option with radio button.
        choice = t.IntVar()
        choice_menu_1 = t.Radiobutton(option_menu, text="Rechercher des informations sur un aliment en particulier",
                                      variable=choice, value=1)
        choice_menu_1.pack(fill=t.BOTH)

        choice_menu_2 = t.Radiobutton(option_menu, text="Explorer une catégorie d'aliments",
                                      variable=choice, value=2)
        choice_menu_2.pack(fill=t.BOTH)

        choice_menu_3 = t.Radiobutton(option_menu, text="Consulter l'historique de vos substitutions",
                                      variable=choice, value=3)
        choice_menu_3.pack(fill=t.BOTH)

        choice_menu_4 = t.Radiobutton(option_menu, text="Quitter l'application",
                                      variable=choice, value=4)
        choice_menu_4.pack(fill=t.BOTH)


if __name__ == '__main__':
    w = Ofs()
    w.run()
