# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionProvideLeagueInfo(Action):

    def name(self) -> Text:
        return "action_provide_league_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO query league info
        league_name = tracker.get_slot("league_name")
        print(f"ActionProvideLeagueInfo ---->>>>> league_name = {league_name}")
        dispatcher.utter_message(
            "The season is over. "
            "The The champion team is MC, top 4 are: MC, MU, Liver, Chelsea. "
            "The teams that are relegated are Fullham, West Brom, Sheffield.")
        return []


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
        return []


class ActionTopPlayer(Action):
    def name(self) -> Text:
        return "action_top_player"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        league_name = tracker.get_slot("league_name")
        print(f"ActionTopPlayer ---->>>>> league_name = {league_name}")
        dispatcher.utter_message("The top-player is Harry Kane with 23 goals")
        return []


class ActionPlayerInfo(Action):
    def name(self) -> Text:
        return "action_player_info"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        player_name = tracker.get_slot("player_name")
        league_name = tracker.get_slot("league_name")
        query_type = tracker.get_slot("query_type")
        print(f"ActionPlayerInfo ---->>>>> player_name = {player_name} "
              f"league_name = {league_name} query_type={query_type}")
        dispatcher.utter_message("He scored 5 goals in the Premier League, 3 goals in the Champion League")
        return []


class ActionFixtures(Action):
    def name(self) -> Text:
        return "action_fixtures"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        club_name = tracker.get_slot("club_name")
        print(f"ActionFixtures ---->>>>> club_name = {club_name}")
        dispatcher.utter_message(f"{club_name} will meet Villarreal on Aug 11, 21:00 at UEFA Super Cup")
        return []


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
