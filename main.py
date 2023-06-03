import time
import threading
from src import speedstars

bots = []
races = ["60m", "100m", "200m", "400m", "110mH", "400mH"]

def create_bots():
    for i in range(10):
        time.sleep(2.5)
        account = speedstars.create_account("beingisdead on tt")
        bots.append(account)

def create_account():
    return speedstars.create_account("beingisdead on tt")

def bot_thread(bot):
    while True:
        for race in races:
            print(speedstars.update_user_data(race, bot, 0o0001))
            print(speedstars.update_player_stats(race, bot, "4/20/1587", "0.00000"))
            time.sleep(5)

def bot_main():
    create_bots()

    threads = []
    for bot in bots:
        thread = threading.Thread(target=bot_thread, args=(bot,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

def main():
    account = create_account()
    while True:
        for race in races:
            print(speedstars.update_user_data(race, account, 0o0001))
            print(speedstars.update_player_stats(race, account, "4/20/1587", "0.00000"))
            time.sleep(3)
main()
