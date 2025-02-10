import re

class Game:
    """
    Represents a game of chess between two players
    """
    def __init__(self, pgn_file=None):
        """
        Initializes a game of chess
        :param pgn_file: PGN file containing an already played chess game
        """
        self._data = {'checkmate':False, 'is_final': False, 'moves': [], 'pgn_text':None}

    @property
    def black(self):
        return self._data['Black']

    @black.setter
    def black(self, value):
        self._data['Black'] = value

    @property
    def black_elo(self):
        return int(self._data['BlackElo'])

    @black_elo.setter
    def black_elo(self, value):
        self._data['BlackElo'] = value

    @property
    def black_rating_diff(self):
        return self._data['BlackRatingDiff']

    @black_rating_diff.setter
    def black_rating_diff(self, value):
        self._data['BlackRatingDiff'] = value

    @property
    def black_title(self):
        if 'BlackTitle' in self._data:
            return self._data['BlackTitle']

        return None

    @black_title.setter
    def black_title(self, value):
        self._data['BlackTitle'] = value


    @property
    def checkmate(self):
        return self._data['checkmate']

    @checkmate.setter
    def checkmate(self, value):
        self._data['checkmate'] = value

    @property
    def is_final(self) -> bool:
        """
        Has the game result been finalized
        :return:
        """
        return self._data['is_final']

    @is_final.setter
    def is_final(self, val):
        """
        Set the is_final value
        :param val: Boolean value
        :raise ValueError: When val is not a boolean
        """
        if not isinstance(val, bool):
            raise ValueError('is_final must be a boolean')

        self._data['is_final'] = val

    @property
    def date(self):
        return self._data['date']

    @date.setter
    def date(self, value):
        self._data['date'] = value

    @property
    def eco(self):
        return self._data['ECO']

    @eco.setter
    def eco(self, value):
        self._data['ECO'] = value

    @property
    def event(self):
        """
        Game event
        :return:
        """
        return self._data['Event']

    @event.setter
    def event(self, value):
        """

        :return:
        """
        self._data['Event'] = value

    @property
    def game_id(self):
        return self._data['game_id']

    @game_id.setter
    def game_id(self, value):
        self._data['game_id'] = value

    @property
    def moves(self) -> list:
        """

        :return:
        """
        return self._data['moves']

    @moves.setter
    def moves(self, val):
        """

        :param val:
        :return:
        """
        self._data['moves'] = val

    @property
    def opening(self):
        return self._data['Opening']

    @opening.setter
    def opening(self, value):
        self._data['Opening'] = value

    @property
    def pgn_text(self):
        return self._data['pgn_text']

    @pgn_text.setter
    def pgn_text(self, value):
        self._data['pgn_text'] = value

    @property
    def result(self):
        return self._data['Result']

    @result.setter
    def result(self, value):
        self._data['Result'] = value

    @property
    def round(self):
        return self._data['Round']

    @round.setter
    def round(self, value):
        self._data['Round'] = value

    @property
    def site(self):
        return self._data['Site']

    @site.setter
    def site(self, value):
        """
        Game site (url for online chess, Physical Location for realworld pgn)
        :param value:
        :return:
        """
        self._data['Site'] = value

    @property
    def termination(self):
        return self._data['Termination']

    @termination.setter
    def termination(self, value):
        self._data['Termination'] = value

    @property
    def time_control(self):
        return self._data['TimeControl']

    @time_control.setter
    def time_control(self, value):
        self._data['TimeControl'] = value

    @property
    def utc_date(self):
        """
        White Player Name
        """
        return self._data['UTCDate']

    @utc_date.setter
    def utc_date(self, value):
        """

        :return:
        """
        self._data['UTCDate'] = value

    @property
    def utc_time(self):
        """
        White Player Name
        """
        return self._data['UTCTime']

    @utc_time.setter
    def utc_time(self, value):
        """

        :return:
        """
        self._data['UTCTime'] = value


    @property
    def white(self):
        """
        White Player Name
        """
        return self._data['White']

    @white.setter
    def white(self, value):
        """

        :return:
        """
        self._data['White'] = value

    @property
    def white_elo(self):
        """
        White Player Name
        """
        return int(self._data['WhiteElo'])

    @white_elo.setter
    def white_elo(self, value):
        """

        :return:
        """
        self._data['WhiteElo'] = value

    @property
    def white_rating_diff(self):
        """
        White Player Name
        """
        return self._data['WhiteRatingDiff']

    @white_rating_diff.setter
    def white_rating_diff(self, value):
        """

        :return:
        """
        self._data['WhiteRatingDiff'] = value

    @property
    def white_title(self):
        if 'WhiteTitle' in self._data:
            return self._data['WhiteTitle']

        return None

    @white_title.setter
    def white_title(self, value):
        self._data['WhiteTitle'] = value

    def from_pgn(self, pgn_text):
        """

        :param pgn_text:
        :return:
        """
        # Set the pgn_text property
        self.pgn_text = pgn_text

        # Parse, the pgn
        for line in pgn_text.split('\n'):
            # Tag Line
            if line.startswith('['):
                tag, value = line.split(' ',1)
                tag = tag.replace('[','')
                value = value.replace(']','').replace('"','')
                self._data[tag] = value

            # Split all the moves
            if line.startswith('1.'):
                # Create the moves array
                pat = re.compile(" \d+\.+ ")
                pos = 0
                moves = []
                while m := pat.search(line, pos):
                    moves.append(line[pos:m.start()])
                    pos = m.start() + 1
                moves.append(line[pos:])

                # Add all the moves we found
                self._data['moves'] = moves

        # Pull the game_id from the site value
        self.game_id = self.site.replace('https://lichess.org/','')

        # Did the game end with a checkmate?
        if len(self._data['moves']) > 0:
            move_number, move_text, comment_result = self._data['moves'][-1].split(' ',2)
            if move_text.find('#') != -1:
                self.checkmate = True

        # Game over?
        self.is_final = True