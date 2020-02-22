import tkinter as t
import time
import manageDB


class ViewControl(t.Frame):
    def __init__(self, main_frame, **kwargs):

        self.main_frame = main_frame

        super().__init__(main_frame, **kwargs)

        self.actual_frame = []
        self.frames = {
            '1': Welcome,
            '2': MainMenu
        }

        self.start()

    def show_next(self, frame='2'):
        """Destroy displayed view and show next view."""

        # destroy displayed view
        self.actual_frame[0].destroy()
        self.actual_frame.pop()

        show = self.frames.get(frame)
        show(self.main_frame)

    def displayed_frame(self, frame):
        """Store name of the view displayed."""
        self.actual_frame.append(frame)

    def display_frame(self, frame):
        actual = frame(self.main_frame)
        self.displayed_frame(actual)

    def start(self):
        self.display_frame(Welcome)




class OfsGui(t.Frame):
    """Manage application's wiews """
    def __init__(self, window, **kwargs):
        self.main_window = window

        super().__init__(self.main_window, width=1080, height=768, background='blue', **kwargs)
        # self.pack(fill=t.BOTH)

        self.actual_frame = []
        self.frames = {
            '1': Welcome,
            '2': MainMenu
        }

        self.start()

    def show_next(self, frame='2'):
        """Destroy displayed view and show next view."""

        # destroy displayed view
        self.actual_frame[0].destroy()
        self.actual_frame.pop()

        next_frame = self.frames.get(frame)
        self.display_frame(next_frame)

    def displayed_frame(self, frame):
        """Store name of the view displayed."""
        self.actual_frame.append(frame)

    def display_frame(self, frame):
        actual = frame(self.main_window)
        self.displayed_frame(actual)

    def start(self):
        self.display_frame(Welcome)
        # ViewControl(self.main_window)

    def quit(self):
        self.destroy()


class Welcome(t.Frame):
    """Welcome frame. """
    def __init__(self, main_frame):
        super().__init__(main_frame, width=1024, height=768, background='yellow')
        self.pack(fill=t.BOTH)
        self.display()

    def display(self):
        """Create welcome screen. """
        # self.displayed_frame(self)

        welcome = t.Label(self, text="""
        Bienvenue dans OpenFood SWAP !""", fg='blue')
        welcome.pack(side='top', fill=t.BOTH)

        sub_welcome = t.Label(self, text="""Cette application vous permet d'avoir des infos sur ce que vous consommez,
        et de trouver éventuellement des équivalents plus sains ! ;-)
        """)
        sub_welcome.pack()

        start_button = t.Button(self, text="Cliquez pour commencer !", fg='green', command=OfsGui.show_next)
        start_button.pack(side="bottom")


class MainMenu(t.Frame):
    """Main app menu """

    def __init__(self, main_frame):
        super().__init__(main_frame, width=1024, height=768, background='green')
        self.pack(fill=t.BOTH)
        self.display()

    def display(self):

        """Create main menu screen"""
        title = t.Label(self, text="Menu principal", fg='green')
        title.pack(fill=t.X)

        sub_title = t.Label(self, text="Choisissez ce que vous voulez faire: ")
        sub_title.pack(fill=t.X)

        # create menu option with radio button.
        choice = t.IntVar()
        choice_menu_1 = t.Radiobutton(self, text="Rechercher des informations sur un aliment en particulier",
                                      variable=choice, value=1)
        choice_menu_1.pack()

        choice_menu_2 = t.Radiobutton(self, text="Explorer une catégorie d'aliments",
                                      variable=choice, value=2)
        choice_menu_2.pack()

        choice_menu_3 = t.Radiobutton(self, text="Consulter l'historique de vos substitutions",
                                      variable=choice, value=3)
        choice_menu_3.pack()

        choice_menu_4 = t.Radiobutton(self, text="Quitter l'application",
                                      variable=choice, value=4)
        choice_menu_4.pack()

        # action based upon choice
        decision = choice.get()

        # if decision is None:
        #     return
        # else:
        #     action = self.main_options.get(decision)
        #     action()
    # def show_next(self):
    #     self.acutal_frame[0].destroy()
    #     show = self.frames['2']
    #     show()

    def quit(self):
        self.destroy()



# class MainMenu(t.Frame):
#     """Main menu screen"""
#
#     def __init__(self, main_frame, **kwargs):
#         super().__init__(main_frame, width=1024, height=768, **kwargs)
#         self.main_frame = main_frame
#         self.pack(fill=t.BOTH)
#         self.mainloop()
#
#         self.main_options = {
#             '1': self.search_product,
#             '2': self.explore_category,
#             '3': self.show_history,
#             '4': self.quit
#         }
#
#     def main_menu(self):
#         """Create main menu screen"""
#         title = t.Label(self, text="Menu principal", fg='green')
#         title.pack(fill=t.X)
#
#         sub_title = t.Label(self, text="Choisissez ce que vous voulez faire: ")
#         sub_title.pack(fill=t.X)
#
#         # create menu option with radio button.
#         choice = t.IntVar()
#         choice_menu_1 = t.Radiobutton(self, text="Rechercher des informations sur un aliment en particulier",
#                                       variable=choice, value=1)
#         choice_menu_1.pack()
#
#         choice_menu_2 = t.Radiobutton(self, text="Explorer une catégorie d'aliments",
#                                       variable=choice, value=2)
#         choice_menu_2.pack()
#
#         choice_menu_3 = t.Radiobutton(self, text="Consulter l'historique de vos substitutions",
#                                       variable=choice, value=3)
#         choice_menu_3.pack()
#
#         choice_menu_4 = t.Radiobutton(self, text="Quitter l'application",
#                                       variable=choice, value=4)
#         choice_menu_4.pack()
#
#         # action based upon choice
#         decision = choice.get()
#
#         # if decision is None:
#         #     return
#         # else:
#         #     action = self.main_options.get(decision)
#         #     action()
#
#     def search_product(self):
#         pass
#
#     def explore_category(self):
#         pass
#
#     def show_history(self):
#         pass
#
#     def run(self):
#         self.main_menu()


def main():
    window = t.Tk()
    OfsGui(window)
    window.mainloop()


if __name__ == '__main__':
    main()

main()



