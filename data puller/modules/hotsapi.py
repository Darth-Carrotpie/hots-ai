import requests
import json


class hotsapi:
    def __init__(self):
        self.status_code = 503
        return

    def return_json(self, r):
        self.status_code = r.status_code
        if r.status_code == 200:
            return r.json()
        else:
            return None

    def get_replay_list(self, start_date=None, end_date=None, game_map=None, game_type=None, player=None, min_id=None):
        payload = {'start_date': start_date, 'end_date': end_date, 'game_map': game_map,
                   'game_type': game_type, 'player': player, 'min_id': min_id}

        # response = requests.post('https://hotsapi.net/api/v1/replays/', data=payload)
        # print(response.request.body)
        # print(response.request.headers)

        r = requests.get("https://hotsapi.net/api/v1/replays", params=payload)
        print(r.url)
        print(r.request.body)
        print(r.request.headers)
        print(r.status_code)
        return r

    def get_paged_replay_list(self, page=None, start_date=None, end_date=None, game_map=None, game_type=None, player=None, min_id=None):
        payload = {'page': page, 'start_date': start_date, 'end_date': end_date,
                   'game_map': game_map, 'game_type': game_type, 'player': player, 'min_id': min_id, 'existing': True, 'with_players': False}
        r = requests.get(
            "https://hotsapi.net/api/v1/replays/paged", params=payload)
        return self.return_json(r)

    def get_replay(self, id):
        r = requests.get("https://hotsapi.net/api/v1/replays/" + str(id))
        return self.return_json(r)

    def get_replays_parsed(self, id):
        r = requests.get(
            "https://hotsapi.net/api/v1/replays/parsed?min_parsed_id="+str(id)+"&with_players=true")
        # print(r.status_code)
        return self.return_json(r)

    def upload_replay(self, file):
        file = {"file": open(file, "rb")}
        r = requests.post("https://hotsapi.net/api/v1/replays/", files=file)
        return self.return_json(r)

    def get_hero_list(self):
        r = requests.get("https://hotsapi.net/api/v1/heroes/translations")
        return self.return_json(r)

    def get_map_list(self):
        r = requests.get("https://hotsapi.net/api/v1/maps/translations")
        return self.return_json(r)
