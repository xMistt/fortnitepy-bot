import fortnitepy, json, sys, datetime
from crayons import red, green, cyan

def time():
    return datetime.datetime.now().strftime('%H:%M:%S')

def botLogin():
    with open('config.json', "r") as f:
        data = json.load(f)

    while True:
        a = input(green(f"[PartyBot] [{time()}] Enter your bot's email: "))
        b = input(green(f"[PartyBot] [{time()}] Enter your bot's password: "))
            
        client = fortnitepy.Client(
            email=a,
            password=b
        )

        @client.event
        async def event_ready():
            print(green(f"\n[PartyBot] [{time()}] Success!\n[PartyBot] [{time()}] Email: {a}\n[PartyBot] [{time()}] Password: {b}"))
            data["email"] = a
            data["password"] = b
            with open('config.json', 'w') as json_file:
                json.dump(data, json_file, indent = 4, sort_keys=True)
            print(red(f"[PartyBot] [{time()}] Please restart your bot..."))
            sys.exit()

        print(cyan(f"[PartyBot] [{time()}] Checking\n[PartyBot] [{time()}] Note: This may take awhile"))
        client.run()
