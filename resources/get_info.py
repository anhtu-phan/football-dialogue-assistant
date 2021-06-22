import requests
import os
import json
from datetime import datetime

# print(os.environ.get('X_RAPIDAPI_KEY'))

headers = {
    'x-rapidapi-key': os.environ.get('X_RAPIDAPI_KEY'),
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}


def search_league(league_name):
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    querystring = {"search": league_name.lower().split(" ")[0]}
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        response = response.json()
        if response is not None and len(response['response']) > 0:
            return response['response'][0]['league']
    return {"id": None}


def get_current_season(league_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    query_string = {"id": league_id}
    response = requests.request("GET", url, headers=headers, params=query_string)
    current_season = None
    if response.status_code == 200:
        response = response.json()
        # print(response)
        for league in response['response']:
            for season in league['seasons']:
                if season['current']:
                    current_season = season['year']
                    break
    return current_season


def search_player(player_name, league_id=None, team_id=None):
    url = "https://api-football-v1.p.rapidapi.com/v3/players"
    player_names = player_name.lower().split(" ")
    for player_name in player_names:
        querystring = {"search": player_name}
        if league_id is not None:
            querystring['league'] = league_id
        if team_id is not None:
            querystring['team'] = team_id

        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            response = response.json()
            if response is not None and len(response['response']) > 0:
                return response['response'][0]['player']
    return {"id": None}


def get_league_info(league_name):
    league_id = search_league(league_name)['id']
    if league_id is not None:
        current_season = get_current_season(league_id)
        if current_season is not None:
            res = get_fixtures(league_id, current_season)
            return res
    return None


def get_fixtures(league_id, season, current=True):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds"
    querystring = {"league": str(league_id), "season": str(season), "current": str(current).lower()}
    response = requests.request("GET", url, headers=headers, params=querystring)
    current_rounds = []
    results = []
    if response.status_code == 200:
        response = response.json()
        if response is not None:
            current_rounds = response['response']
    for r in current_rounds:
        res = get_fixtures_by_round(league_id, season, r)
        results.append(res)
    return results


def get_fixtures_by_round(league_id, season, round_name):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    querystring = {"league": league_id, "season": season, "round": round_name}
    response = requests.request("GET", url, headers=headers, params=querystring)
    result = {
        "round": round_name,
        "fixtures": []
    }
    if response.status_code == 200:
        response = response.json()
        # print(response)
        for f in response['response']:
            fixture = {}
            fixture['time'] = datetime.fromtimestamp(f['fixture']['timestamp']).strftime("%b %d %I:%M%p")
            fixture['timezone'] = f['fixture']['timezone']
            fixture['home'] = {"id": f['teams']['home']['id'], "name": f['teams']['home']['name']}
            fixture['away'] = {"id": f['teams']['away']['id'], "name": f['teams']['away']['name']}
            result['fixtures'].append(fixture)
        # print(result)

    return result


def get_top_score(league_name, season=None, number_players=1):
    url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
    league_id = search_league(league_name)['id']
    result = []
    if league_id is not None:
        if season is None:
            season = get_current_season(league_id)
        querystring = {"league": league_id, "season": season}
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            response = response.json()
            if response is not None:
                for i in range(0, min(number_players, len(response['response']))):
                    info_i = response['response'][i]
                    info = {
                        "name": info_i['player']['firstname'] + " " + info_i['player']['lastname'],
                        "team": info_i['statistics'][0]['team']['name'],
                        "goals": info_i['statistics'][0]['goals']['total']
                    }
                    result.append(info)
    return result


def get_player_statistic(player_name, league_names, season=None, nb_league=0, query_type="goals"):
    url = "https://api-football-v1.p.rapidapi.com/v3/players"
    league_id = search_league(league_names[0])['id']
    if league_id is None:
        return None
    player_id = search_player(player_name, league_id)['id']
    if player_id is None:
        return None
    querystring = {"id": player_id}
    if season is None:
        season = get_current_season(league_id)
    querystring['season'] = season
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code != 200:
        return None
    response = response.json()
    result = []
    if nb_league == 0:
        for stat in response['response'][0]['statistics']:
            if int(stat['league']['season']) == int(season):
                result.append({
                    "league": stat['league']['name'],
                    query_type: stat[query_type]
                })
    else:
        for i in range(nb_league):
            league = search_league(league_names[i])
            for stat in response['response'][0]['statistics']:
                if stat['league']['id'] == league['id'] and int(stat['league']['season']) == int(season):
                    result.append({
                        "league": league['name'],
                        query_type: stat[query_type]
                    })
    return result


if __name__ == '__main__':
    league_id = search_league("euro")
    r = get_player_statistic("werner", ["euro"], nb_league=0)
    print(r)
