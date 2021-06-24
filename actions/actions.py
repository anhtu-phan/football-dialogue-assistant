# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, Restarted
from rasa_sdk.executor import CollectingDispatcher
from resources import get_info


# class ActionRestart(Action):
#
#     def name(self) -> Text:
#         return "action_restart"
#
#     def run(
#         self,
#         dispatcher: "CollectingDispatcher",
#         tracker: Tracker,
#         domain: "DomainDict",
#     ) -> List[Dict[Text, Any]]:
#         return [Restarted()]


class ActionProvideLeagueInfo(Action):

    def name(self) -> Text:
        return "action_provide_league_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        league_name = tracker.get_slot("league_name")
        try:
            if league_name is not None:
                print(f"ActionProvideLeagueInfo ---->>>>> league_name = {league_name}")
                result = get_info.get_league_info(league_name)
                if result is not None:
                    mess = ""
                    nb_matches = 0
                    for r in result:
                        mess += f"In {r['round']}:\n"
                        for fixture in r['fixtures']:
                            mess += f"{fixture['home']['name']} meet {fixture['away']['name']} on {fixture['time']};\n"
                            nb_matches += 1
                    mess = f"There are {nb_matches} matches coming up:\n" + mess
                else:
                    mess = "The season is over"
            else:
                mess = "Sorry! I cannot find information about this league"
        except Exception as e:
            print(e)
            mess = "Sorry! I cannot find information about this league"
        dispatcher.utter_message(mess)
        return [SlotSet("global_league_name", league_name), SlotSet("league_name", None)]


class ActionStatisticLeague(Action):
    def name(self) -> Text:
        return "action_statistic_league"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        statistic_type = tracker.get_slot("statistic_type")
        league_name = tracker.get_slot("league_name")
        query_round = tracker.get_slot("query_round")
        query_number = tracker.get_slot("query_number")
        # TODO query api
        print(f"ActionStatisticLeague ---->>>>> statistic_type = {statistic_type} league_name = {league_name} "
              f"query_round = {query_round} query_number = {query_number}")
        dispatcher.utter_message("MC, MU, Liver, Chelsea")
        return [SlotSet("league_name", None)]


class ActionTopPlayer(Action):
    def name(self) -> Text:
        return "action_top_player"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            league_name = tracker.get_slot("league_name")
            if league_name is None:
                league_name = tracker.get_slot("global_league_name")
            season = tracker.get_slot("season")
            i_query_number = tracker.get_slot("query_number")
            try:
                query_number = int(i_query_number)
            except:
                query_number = 1
            print(f"ActionTopPlayer ---->>>>> league_name = {league_name}({tracker.get_slot('league_name')}) season = {season} query_number = {query_number}({i_query_number})")
            result = get_info.get_top_score(league_name, season, query_number)
            if query_number == 1:
                mess = f"The top player is {result[0]['name']} of {result[0]['team']} with {result[0]['goals']} goals"
            else:
                mess = f"The following is {query_number} top player:\n"
                for i in range(len(result)):
                    mess += f"{i+1}: {result[i]['name']} of {result[i]['team']} with {result[i]['goals']} goals.\n"
        except Exception as e:
            print(e)
            mess = "Sorry I cannot find this information"
        dispatcher.utter_message(mess)
        return [SlotSet("league_name", None), SlotSet("query_number", None)]


class ActionPlayerInfo(Action):
    def name(self) -> Text:
        return "action_player_info"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        print("========== ActionPlayerInfo ==========")
        try:
            player_name = tracker.get_slot("PERSON")
            league_name = tracker.get_slot("league_name")
            season = tracker.get_slot("season")
            nb_league = 1
            if league_name is None:
                nb_league = 0
                # print(f"Slot {tracker.slots}")
                league_name = tracker.get_slot("global_league_name")

            # TODO query_type is None just show info about player
            query_type = tracker.get_slot("query_type")

            print(f"ActionPlayerInfo ---->>>>> player_name = {player_name} "
                  f"league_name = {league_name}({tracker.get_slot('league_name')}) query_type={query_type} nb_league = {nb_league}")
            result = get_info.get_player_statistic(player_name, [league_name], season, nb_league, query_type)
            # print(f"ActionPlayerInfo ---->>>>> results = {result}")
            # result = None
            mess = ""
            for league in result:
                mess += f"At {league['league']}: "
                for key, value in league[query_type].items():
                    if value is not None:
                        mess += f"{key} is {value}; "
                mess += "\n"
        except Exception as e:
            print(e)
            mess = "Sorry I cannot find information about this player"
        dispatcher.utter_message(mess)
        return [SlotSet("league_name", None), SlotSet("PERSON", None), SlotSet("query_type", None)]


class ActionFixtures(Action):
    def name(self) -> Text:
        return "action_fixtures"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            club_name = tracker.get_slot("club_name")
            league_name = tracker.get_slot("league_name")
            print(f"ActionFixtures ---->>>>> club_name = {club_name} league_name = {league_name}")
            result = get_info.get_fixtures_by_team(club_name, league_name=league_name)
            if len(result['result']) > 0:
                mess = f"{result['team_name']} will\n"
                for res in result['result']:
                    if res["type"] == "home":
                        mess += f"meet {res['team']} at {res['round']} of {res['league']} in {res['time']} at home;\n"
                    else:
                        mess += f"visit {res['team']} at {res['round']} of {res['league']} in {res['time']};\n"
            else:
                mess = f"Sorry I cannot find information about next matches of {result['team_name']}"
        except Exception as e:
            print(e)
            mess = "Sorry I cannot find information"
        dispatcher.utter_message(mess)
        return [SlotSet("club_name", None), SlotSet("league_name", None)]


class ActionLineUp(Action):
    def name(self) -> Text:
        return "action_line_up"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        first_club = tracker.get_slot("first_club")
        second_club = tracker.get_slot("second_club")
        print(f"ActionLineUp ---->>>>> {first_club} vs {second_club}")
        dispatcher.utter_message("Coming soon")
        return []


class ActionClubInfo(Action):
    def name(self) -> Text:
        return "action_club_info"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        club_name = tracker.get_slot("club_name")
        query_type = tracker.get_slot("query_type")
        print(f"ActionClubInfo ---->>>>> {club_name} vs {query_type}")
        dispatcher.utter_message("Coming soon")
        return []
