from time import sleep
import json
from datetime import datetime
from collections import OrderedDict
import requests

base_url = 'http://127.0.0.1:8000'
token = ''


class MarioSession(requests.Session):
    def __init__(self, base_url, token, api_version):
        super().__init__()
        self.base_url = base_url
        self.token = token
        self.api_version = api_version
        if self.token is not None:
            self.headers.update({'Authorization': f'Token {self.token}'})

    def request(self, method, url, raise_for_status=False, max_retries=1, **kwargs):
        url = f'{self.base_url}/api/v{self.api_version}/{url}/'

        for attempt in range(max_retries):
            try:
                result = super().request(method, url, **kwargs)
            except requests.ConnectionError:
                print(f"Got connection error let's try again (attempt {attempt}).")
                sleep(1)
            else:
                break
        else:
            raise requests.ConnectionError(f"Made {max_retries} attempts and still connection error")

        if raise_for_status:
            try:
                result.raise_for_status()
                result.json()
            except requests.HTTPError:
                try:
                    print(result.json())
                except json.JSONDecodeError:
                    # print(result.content)
                    pass
                raise
            except json.JSONDecodeError:
                print(result.content)
                raise

        return result


mario = MarioSession(base_url=base_url, token=token, api_version=1)

generations = OrderedDict()

with open('generations.txt') as generations_file:
    for line in generations_file:
        game_num, data = eval(line)
        generations[game_num] = data

results = {}

with open('results.txt') as results_file:
    for line in results_file:
        data = eval(line)
        if len(data) == 6:
            ian_watched = data[5]
            data = data[:5]
        else:
            ian_watched = False

        result_num, score, players, handicaps, timestamp = data
        results[result_num] = {
            'score': score, 'players': players,
            'handicaps': handicaps, 'timestamp': timestamp,
            'ian_watched': ian_watched
        }

creation_timestamp = 1401796435

initial_persons = mario.get('persons', raise_for_status=True).json()['results']
all_persons = {person['name']: person['id'] for person in initial_persons}


def check_player_exists(player_name):
    if player_name not in all_persons:
        response = mario.post('persons', json={'name': player_name})
        person_id = response.json()['id']
        all_persons[player_name] = person_id
    return player_name


def get_player(generation, index):
    tyres = generation['tyres'][index].replace('Tire', 'Tyre')
    return {
        'character': generation['characters'][index],
        'tyres': tyres,
        'glider': generation['gliders'][index],
        'vehicle': generation['vehicles'][index],
        'red_team': generation['team colours'][index] == 'red',
        'seat_position': index,
        'person': check_player_exists(generation['players'][index]),
    }


for num, generation in generations.items():
    print(num)
    if num < 466:
        continue

    result = results.get(num)

    if result:
        for person in result['handicaps']:
            check_player_exists(person[0])
            # Historically we never had creation timestamps so let's guess they are all 20 minutes before submission
            creation_timestamp = result['timestamp'] - 20 * 60
        else:
            # If game was never submitted fuck it. let's at least have timestamps in the right order
            creation_timestamp += 60

    if num == -1:
        response = {'id': 75}
    else:
        data = {
            'creation_timestamp': datetime.fromtimestamp(creation_timestamp).isoformat(),
            'players': [
                get_player(generation, index) for index in range(4)
            ],
            'forced_team_selection': generation['team selection'] != 'random',
        }

        response = mario.post('games', json=data, raise_for_status=True, max_retries=5).json()

    if result:
        game_id = response['id']
        data = {
            'red_score': result['score'],
            'ian_watched': result['ian_watched'],
            'submission_timestamp': datetime.fromtimestamp(result['timestamp']).isoformat()
        }
        response = mario.patch(f'games/{game_id}', json=data, raise_for_status=True, max_retries=5)

        print('check')
        handicaps_expected = dict(result['handicaps'])
        for key in handicaps_expected:
            handicaps_expected[key] = float(handicaps_expected[key])

        handicaps_seen = mario.get('persons', raise_for_status=True, max_retries=5).json()['results']
        handicaps_seen = {person['name']: float(person['handicap']) for person in handicaps_seen}
        if not handicaps_expected == handicaps_seen:
            print(handicaps_expected)
            print(handicaps_seen)
            for player, score in handicaps_expected.items():
                print(player, score, handicaps_seen[player])
            raise Exception('handicaps dont match')
