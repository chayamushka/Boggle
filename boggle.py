import time
from tkinter import *

from game import *

THREE_MIN_IN_SEC = 180
ONE_SEC_IN_MILI = 1000


def to_mins(time1):
    """
    this method converts time to sting format
    :param time1: type int representing the number of seconds
    :return: type str representing the time in the format MIN:SEC
    """
    return time.strftime('%M:%S', time.gmtime(time1))


class GameGraphics:
    def __init__(self):

        self.__high_scores = {}
        self.__game = Game()
        self.__screen = Tk()
        self.__current_path = []

        # ---------- picture initiating -----------#
        play_image = PhotoImage(file="play2.PNG", height=234, width=274)
        background_img = PhotoImage(file="re.PNG")

        # ---------- __screen initiating -----------#
        self.__start_screen = Label(self.__screen, image=background_img)
        self.__game_frame = Canvas(self.__screen, width=700, height=750)
        self.__game_frame.create_image(350, 375, image=background_img)
        # ---------- buttons initiating -----------#
        self.__start_button = Button(self.__start_screen, command=self.start_game_play, image=play_image,
                                     compound="center", activebackground="tan", bg="tan", highlightthickness=0, padx=0,
                                     pady=0, borderwidth=0, relief=FLAT)
        self.__quit_button = Button(self.__start_screen, text="quit", command=quit,
                                    bg="red4", fg="white")
        self.__submit_but = Button(self.__game_frame, text="submit", command=self.submit)
        self.__letter_buttons = []

        # ---------- clock initiating -----------#
        self.__clock_text = self.__game_frame.create_text(550, 350, text="", font=("Candy", 30), fill="white")
        self.__remaining = 0

        # ---------- player name initiating -----------#
        self.__player_name = StringVar()
        self.__player_name_textbox = Entry(self.__start_screen, bg="tan", textvariable=self.__player_name,
                                           foreground='grey22')
        self.__player_name_textbox.bind('<Button-1>', self.player_name_inp)

        # ---------- random crap initiating -----------#
        self.__score_text = self.__game_frame.create_text(550, 340, text="", font=("Candy", 30), fill="white")
        self.cur_word = Label(self.__game_frame, text="", width=21, anchor=W)
        self.board_frame = Frame(self.__game_frame, width=500, height=500, bg="black")
        self.__words_frame = Listbox(self.__game_frame, relief=FLAT, height=10, bg='light sea green')
        self.__words_frame.insert(END, "your words:")

        # ---------- initiating -----------#
        self.create_start_screen()
        self.__screen.mainloop()

    # -------------------------------------------------- button functions ------------------------------------------ #

    def player_name_inp(self, event):
        """
        this method deals with the username input
        :param event: the event that set us
        :return: None
        """
        if self.__player_name_textbox.get() == 'Please Enter your Name:':
            event.widget.delete(0, END)

    def start_game_play(self):
        """
        this method starts a new game.
        :return: None
        """
        self.__start_screen.pack_forget()
        self.create_board()

    def submit(self):
        word = self.__game.one_turn(self.__current_path)
        if word:
            self.__words_frame.insert(END, word)
        # reset all buttons and current word
        self.reset_buttons(Letters.reset)

    # --------------------------------------------- outside callers ------------------------------------------------- #

    def remove_last_step(self):
        """
        this method removes the previous step from the current path
        :return: None
        """
        if self.__current_path:
            self.__current_path.pop()

    def add_to_cur_path(self, cor):
        """
        this method adds a cord to the path.
        :param cor: type tuple of the form (x,y), representing the coord we want to add
        :return: None
        """
        self.__current_path.append(cor)

    def is_valid_step(self, cor):
        """
        this method checks of the usser can click the given coord.
        :param cor: type tuple of the form (x,y), representing the coord we want to add
        :return: type bool, True for good path False for bad.
        """
        if len(self.__current_path) == 0:
            return True
        last_step = self.__current_path[-1]

        def dist(x, y):
            return abs(x - y) <= 1

        if dist(last_step[0], cor[0]) and dist(last_step[1], cor[1]) and cor not in self.__current_path[:-1]:
            return True
        return False

    # ------------------------------------------- main functions -----------------------------------------------#

    def create_start_screen(self):
        """
        this method creates the start menu
        :return: None
        """
        self.__screen.title("boggle")
        self.__player_name.set('Please Enter your Name:')
        self.__player_name_textbox.place(relx=0.385, rely=0.8)
        self.__start_screen.pack()

        self.__start_button.place(relx=0.3, rely=0.446)
        self.__quit_button.place(relx=0.47, rely=0.85)

    def create_board(self):
        """
        this method creates the game __screen and inits all starting values
        :return: None
        """
        self.__game_frame.pack()
        self.cur_word.place(relx=0.22, rely=0.35)
        self.board_frame.place(relx=0.1, rely=0.41)
        for i, line in enumerate(self.__game.board.get_board()):
            for l, letter in enumerate(line):
                self.__letter_buttons.append(Letters(letter, [i, l], self))

        self.__words_frame.place(relx=0.7, rely=0.5)
        self.__submit_but.place(relx=0.1, rely=0.34)
        self.count_down(THREE_MIN_IN_SEC)

    def count_down(self, time_left=None):
        """
        this method counts the __remaining time and ends the game once the time is over
        :param time_left: the number of seconds __remaining until game over
        :return: None
        """
        if time_left is not None:
            self.__remaining = time_left

        if self.__remaining <= 0:
            self.__game_frame.delete(self.__clock_text)
            self.__game_frame.delete(self.__score_text)
            self.game_over()

        else:
            self.__game_frame.delete(self.__score_text)
            self.__score_text = self.__game_frame.create_text(550, 340, text=f"Score : {self.__game.get_score()}",
                                                              font=("Candy", 30), fill="white")
            self.__game_frame.delete(self.__clock_text)
            self.__clock_text = self.__game_frame.create_text(550, 300, text=to_mins(self.__remaining),
                                                              font=("Candy", 30),
                                                              fill="white")
            self.__remaining -= 1

            # next second
            self.__screen.after(ONE_SEC_IN_MILI, self.count_down)

    def game_over(self):
        """
        this method removes the game __screen and changes if to starting __screen,
        and resets all starting values
        :return: None
        """

        # update the players high score.
        if self.__player_name.get() == 'Please Enter your Name:' or not self.__player_name.get():
            self.__player_name.set('player')
        if self.__player_name.get() in self.__high_scores.keys():
            self.__high_scores[self.__player_name.get()] = max(self.__game.get_score(),
                                                               self.__high_scores[self.__player_name.get()])
        else:
            self.__high_scores[self.__player_name.get()] = self.__game.get_score()

        self.__game_frame.pack_forget()

        # if there are any words on the frame remove them
        if self.__words_frame.get(1):
            self.__words_frame.delete(1, END)

        self.reset_buttons(Letters.destroy)
        self.__letter_buttons = []

        self.__remaining = 0
        self.__player_name.set("Please Enter your Name:")
        self.__game = Game()
        self.high_scores().place(relx=0.05, rely=0.45)
        self.__start_screen.pack()

    def high_scores(self):
        """
        this method updates the leader board
        :return: the leader board
        """
        leader_board = Listbox(self.__start_screen, height=6, bg="tan")
        leader_board.insert(0, 'High scores: ')
        sorted_scores = sorted(self.__high_scores, key=lambda x: self.__high_scores[x], reverse=True)
        for name in sorted_scores[:5]:
            leader_board.insert(END, f"{name} : {self.__high_scores[name]}")
        return leader_board

    def reset_buttons(self, func):
        """
        this function resets the buttons according to the parameter function
        :param func:
        :return:
        """
        for let in self.__letter_buttons:
            func(let)
        self.cur_word['text'] = ''
        self.__current_path = []


class Letters():

    def __init__(self, letter, cor, game):
        self.letter = letter
        self.clicked = False
        self.button = Button(game.board_frame, text=letter, borderwidth=10, padx=15, pady=15,
                             command=self.letter_pressed,
                             activebackground="red4", bg="LightPink4")
        self.__cord = tuple(cor)
        self.button.grid(row=cor[0], column=cor[1], sticky='ew')
        self.game = game

    def reset(self):
        """
        this method resets the current button to unclicked.
        :return: None
        """
        self.clicked = False
        self.button['bg'] = 'LightPink4'

    def destroy(self):
        self.button.destroy()

    def letter_pressed(self):
        """
        this method does the click operation and sets the colors of the button accordingly
        :return: None
        """
        if self.game.is_valid_step(self.__cord):
            if self.clicked:
                self.reset()
                self.game.remove_last_step()
                self.game.cur_word["text"] = self.game.cur_word["text"][:-1]
                return

            self.clicked = True
            self.button["bg"] = "light sea green"
            self.game.cur_word["text"] += self.letter
            self.game.add_to_cur_path(self.__cord)


if __name__ == '__main__':
    game2 = GameGraphics()
