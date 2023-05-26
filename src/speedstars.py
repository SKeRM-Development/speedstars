import uuid
import requests
import data
import time
import copy

# No built in proxy handler, was created using a rotating proxy
proxies = {
    "http": "",
    "https": ""
}

def create_account(name: str) -> dict:
    """Creates an account and returns the display name and ticket in a dict"""
    data.ACCOUNT_DATA["CustomId"] = str(uuid.uuid4())

    while True:
        try:
            response = requests.post(data.BASE_URL + "/Client/LoginWithCustomID", json=data.ACCOUNT_DATA, headers=data.HEADERS, timeout=5, proxies=proxies)
            if response.json()["code"] != 200:
                continue
            break
        except requests.exceptions.RequestException as e:
            print("Request exception:", e)

    ticket = response.json()["data"]["SessionTicket"]

    data.NAME_DATA["DisplayName"] = name
    data.HEADERS["X-Authorization"] = ticket

    while True:
        try:
            response = requests.post(data.BASE_URL + "/Client/UpdateUserTitleDisplayName", json=data.NAME_DATA, headers=data.HEADERS, timeout=5, proxies=proxies)
            if response.json()["code"] != 200:
                continue
            return (name, ticket)
        except requests.exceptions.RequestException as e:
            print("Request exception:", e)

    return response.json()

def update_user_data(event: str, account: tuple, time: int) -> dict:
    """Updates player stats and returns the response from the API"""
    data.LEADERBOARD_DATA["Statistics"][0]["StatisticName"] = event
    data.LEADERBOARD_DATA["Statistics"][0]["Value"] = -time

    data.HEADERS["X-Authorization"] = account[1]

    while True:
        try:
            response = requests.post(data.BASE_URL + "/Client/UpdatePlayerStatistics", json=data.LEADERBOARD_DATA, headers=data.HEADERS, timeout=5, proxies=proxies)
            if response.json()["code"] != 200:
                continue
            break
        except requests.exceptions.RequestException as e:
            print("Request exception:", e)

    return response.json()

def update_player_stats(event: str, account: tuple, date: str, time: str) -> dict:
    """Updates player stats and returns the response from the API"""
    RACER_DATA = copy.deepcopy(data.RACER_DATA)

    RACER_DATA["Data"][f"RacerName_{event}"] = account[0]
    RACER_DATA["Data"][f"RacerData_{event}"] = f"CustomRacer_66BB3E65-5:{account[0]}:73:{time}"
    RACER_DATA["Data"]["Date_UserTotalScore"] = date
    RACER_DATA["Data"][f"Date_{event}"] = date

    while True:
        try:
            response = requests.post(data.BASE_URL + "/Client/UpdateUserData", headers=data.HEADERS, json=RACER_DATA, timeout=5, proxies=proxies)
            if response.json()["code"] != 200:
                continue
            break
        except requests.exceptions.RequestException as e:
            print("Request exception:", e)

    return response.json()

if __name__ == "__main__":
    try:
        account = create_account("test")
        print(account)
        while True:
            print(update_user_data("100m", account, 1000))
            print(update_player_stats("100m", account, "test", "1.000"))
            time.sleep(10)
    except requests.exceptions.RequestException as e:
        print("Request exception during account creation:", e)
