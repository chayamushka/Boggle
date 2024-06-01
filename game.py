from boggle_board_randomizer import randomize_board


class Board:
    def __init__(self):
        self.__board = randomize_board()
        self.__len = len(self.__board)

    # for debug
    def __str__(self):
        """
        This function is called when a board object is to be printed. for debugging purposes
        :return: A string of the current status of the board
        """
        whatever = ''
        for row in self.__board:
            whatever+= '  '.join(letter for letter in row)+"\n"
        return whatever

    def get_board(self):
        """
        thus func gets the board
        :return: a Board object
        """
        return self.__board[:]

    def get_content(self, cor):
        """
        gets the content of the bornd at some coord.
        :param cor: type tuple of the form (x,y) the coord we want to check
        :return: type str of the letter in the given coord
        """
        if type(cor) is not tuple:
            raise ValueError("pls insert a tuple")
        if len(cor) != 2:
            raise ValueError("pls insert a tuple with 2 arguments")
        if type(cor[0]) is not int or type(cor[1]) is not int:
            raise ValueError(f"pls insert only numbers {cor}")
        if cor[0] not in range(self.__len) or cor[1] not in range(self.__len):
            raise ValueError("pls insert numbers in the range! tnx")
        return self.__board[cor[0]][cor[1]]

    def get_path_string(self, cords):
        """
        this method gets the string corresponding to a given path.
        :param cords: type list of tuple holding the coords in the given path.
        :return: type str representing the path on the board given by cords.
        """
        if type(cords) is not list:
            raise ValueError("pls insert a list!!")
        if not len(cords):
            return ""
        word = "".join(list(map(self.get_content, cords))) # joins the content of every cord
        return word

    def get_all_cords(self):
        """
        this method gets all the legal coords on the board.
        :return: type list of tuple of the coords on the board.
        """
        return [(x, y) for x in range(self.__len) for y in range(self.__len)]

    def shuffle_board(self):  # feature
        """
        This method gets a new random board.
        :return: type list of list representing the letter on the board.
        """
        self.__board = randomize_board()
        return self.__board


def get_words_from_file(filepath=r"boggle_dict.txt"):
    """
    this method gets the dictionary for the game.
    :param filepath: type string representing the file directory of the dict
    :return: type set of strings of all the legal words.
    """
    with open(filepath) as data_file:
        dictionary_words = set(line.rstrip() for line in data_file)
        return dictionary_words


class Game:
    def __init__(self):
        self.__score = 0
        self.__used_words = set()
        self.__dictionary = get_words_from_file()
        self.board = Board()

    def get_score(self):
        """
        this method gets the score
        :return: an int
        """
        return self.__score

    def get_used_words(self):
        """
        this method gets used_words
        :return: a set of strings
        """
        return self.__used_words.copy()

    def __add_score(self, word):
        """
        this method updates the current score.
        :param word: the new word that we are adding point for
        :return: None
        """
        self.__score += len(word)**2
        return self.__score

    def one_turn(self, path):
        """
        this method runs one single turn, it gets a path and checks if the user gets any points.
        :param path: type list of tuple representing the path on the board by coords.
        :return: type sting of the word if the word rewards point otherwise None.
        """
        word = self.board.get_path_string(path)
        if word in self.__dictionary and word not in self.__used_words:
            self.__add_score(word)
            self.__used_words.add(word)
            return word
