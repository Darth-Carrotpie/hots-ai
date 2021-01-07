# need to remaket his to take in flattened pandas df instead of raw json
import pandas as pd


class hDataForm:
    def __init__(self, _form_name):
        self.form_name = _form_name
        self.form_inits = {'list_form': self.list_form_init,
                           'flat_form': self.flat_form_init, 'obj_form': self.obj_form_init}
        self.form_inputs = {'list_form': self.list_form_input,
                            'flat_form': self.flat_form_input, 'obj_form': self.obj_form_input}
        self.form_inputs_pd = {'list_form': self.list_form_input_pd,
                               'flat_form': self.flat_form_input_pd, 'obj_form': self.obj_form_input_pd}
        self.column_names = []
        self.object_for_df = {}
        self.form_inits[self.form_name]()
        return

    def input_match(self, match):
        if isinstance(match, pd.Series):
            self.form_inputs_pd[self.form_name](match)
        else:
            self.form_inputs[self.form_name](match)

    def get_output(self):
        return self.column_names, self.object_for_df

    def list_form_init(self):
        self.column_names = ['date', 'map', 'game_type',
                             'winner_team', 'loser_team', 'outcome']
        self.object_for_df = {'date': [], 'map': [], 'game_type': [
        ], 'winner_team': [], 'loser_team': [], 'outcome': []}

    def list_form_input_pd(self, match):
        pass

    def list_form_input(self, match):
        heroesA = []
        heroesB = []
        for player_index in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if match["players"][player_index]['winner']:
                heroesA.append(
                    match["players"][player_index]['hero'].replace('ú', 'u'))
            else:
                heroesB.append(
                    match["players"][player_index]['hero'].replace('ú', 'u'))
        self.object_for_df['date'].append(match["game_date"])
        self.object_for_df['map'].append(match["game_map"])
        self.object_for_df['game_type'].append(match["game_type"])
        self.object_for_df['winner_team'].append(heroesA)
        self.object_for_df['loser_team'].append(heroesB)
        self.object_for_df['outcome'].append(1)

    def obj_form_init(self):
        self.column_names = ['date', 'map', 'game_type',
                             'winner_team', 'loser_team', 'outcome']
        self.object_for_df = {'date': [], 'map': [], 'game_type': [
        ], 'winner_team': [], 'loser_team': [], 'outcome': []}

    def obj_form_input_pd(self, match):
        pass

    def obj_form_input(self, match):
        heroesA = []
        heroesB = []
        for player_index in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if match["players"][player_index]['winner']:
                heroesA.append({"hero": match["players"][player_index]['hero'].replace('ú', 'u'),
                                "level": match["players"][player_index]['hero_level']})
            else:
                heroesB.append({"hero": match["players"][player_index]['hero'].replace('ú', 'u'),
                                "level": match["players"][player_index]['hero_level']})
        self.object_for_df['date'].append(match["game_date"])
        self.object_for_df['map'].append(match["game_map"])
        self.object_for_df['game_type'].append(match["game_type"])
        self.object_for_df['winner_team'].append(heroesA)
        self.object_for_df['loser_team'].append(heroesB)
        self.object_for_df['outcome'].append(1)

    def flat_form_init(self):
        self.column_names = ['date', 'game_map', 'game_type', 'winnerA', 'winnerB', 'winnerC',
                             'winnerD', 'winnerE', 'loserA', 'loserB', 'loserC', 'loserD', 'loserE', 'outcome']
        self.object_for_df = {'date': [], 'game_map': [], 'game_type': [], 'winnerA': [], 'winnerB': [], 'winnerC': [
        ], 'winnerD': [], 'winnerE': [], 'loserA': [], 'loserB': [], 'loserC': [], 'loserD': [], 'loserE': [], 'outcome': []}

    def flat_form_input(self, match):
        winners = ['winnerA', 'winnerB', 'winnerC', 'winnerD', 'winnerE']
        losers = ['loserA', 'loserB', 'loserC', 'loserD', 'loserE']
        heroesA = []
        heroesB = []

        for player_index in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            hero_name = match["players"][player_index]['hero'].replace(
                'ú', 'u')
            if match["players"][player_index]['winner']:
                heroesA.append(hero_name)
            else:
                heroesB.append(hero_name)
        self.object_for_df['date'].append(match["game_date"])
        self.object_for_df['game_map'].append(match["game_map"])
        self.object_for_df['game_type'].append(match["game_type"])
        for index in range(0, 5):
            self.object_for_df[winners[index]].append(heroesA[index])
        for index in range(0, 5):
            self.object_for_df[losers[index]].append(heroesB[index])
        self.object_for_df['outcome'].append(1)

    def flat_form_input_pd(self, match):
        winners = ['winnerA', 'winnerB', 'winnerC', 'winnerD', 'winnerE']
        losers = ['loserA', 'loserB', 'loserC', 'loserD', 'loserE']
        heroesA = []
        heroesB = []

        for player_index in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            hero_col = 'players.'+player_index+'.hero'
            winner_col = 'players.'+player_index+'.winner'
            hero_name = ''
            if type(match[hero_col]) is str:
                hero_name = match[hero_col].replace('ú', 'u')
            else:
                return
            if match[winner_col]:
                heroesA.append(hero_name)
            else:
                heroesB.append(hero_name)

        self.object_for_df['date'].append(match["date"])
        self.object_for_df['game_map'].append(match["game_map"])
        self.object_for_df['game_type'].append(match["game_type"])
        for index in range(0, 5):
            self.object_for_df[winners[index]].append(heroesA[index])
        for index in range(0, 5):
            self.object_for_df[losers[index]].append(heroesB[index])
        self.object_for_df['outcome'].append(1)
