import json

import pathlib
import sqlite3

from datetime import date, timedelta
from calendar import monthrange

data_dir = pathlib.Path(__file__).parent.parent / "data"

from libs.aws.lambda_utils import lambda_handler, BaseEvent


class Event(BaseEvent):
    path: str


@lambda_handler(model=Event)
def handle(event: Event, context):

    print(f"🔵 Connect to database")
    db = sqlite3.connect(data_dir / "database.sqlite")

    if event.path == "retrieve_sessions_starting_after":
        # ------------------------------------------------------------
        # Q3.0 : Retrieve sessions starting after a given date

        def retrieve_sessions_starting_after(date: date):
            cursor = db.cursor()
            cursor.execute("SELECT * FROM session WHERE starting_date >= ?", (date,))
            output = cursor.fetchall()
            cursor.close()
            return output

        sessions = retrieve_sessions_starting_after(date(2025, 5, 1))
        print(f"🔵 {len(sessions)} sessions were found")

    if event.path == "retrieve_sales_from_team":
        # ------------------------------------------------------------
        # Q3.1 : Sales from each team

        def retrieve_sales_from_team(team: str):
            cursor = db.cursor()
            cursor.execute(
                """""",
                (team,),
            )
            output = cursor.fetchall()
            cursor.close()
            return output

        data = {team: retrieve_sales_from_team(team) for team in ["support", "sales"]}
        for team, data in data.items():
            print(f"👉 Sales from {team}")
            for status, count, amount in data:
                print(f"\t{status} : {count} sessions, {amount}€")

    elif event.path == "retrieve_sales_progression":
        # ------------------------------------------------------------
        # Q3.2 : Sales progression over the month
        def retrieve_sales_progression(username: str, year: int, month: int) -> str:
            output = []
            cursor = db.cursor()
            cursor.close()
            return json.dumps(output, indent=4)

        sales_from_support = retrieve_sales_progression(
            "martin.mougenot@walter-learning.com", 2025, 4
        )
        print(sales_from_support)
    return {}
