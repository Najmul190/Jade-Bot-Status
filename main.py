import os
import pypresence
import sys
import ctypes
import pystray
import requests
import io

from PIL import Image
from time import sleep


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if not is_admin():
    print("Please run this script as administrator.")

    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )

    exit(0)


def setupStartup(method="startup_folder"):
    """Sets up the Python script to start on startup using the specified method."""

    if method == "startup_folder":
        startup_folder = os.path.expanduser(
            "~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
        )
        try:
            os.symlink(
                sys.executable,
                os.path.join(startup_folder, f"{os.path.basename(sys.executable)}.lnk"),
            )
        except OSError as e:
            print(f"Error creating startup file: {e}")


def clearConsole():
    """Clears the console."""
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


def quitApp():
    icon.stop()
    global breakLoop

    breakLoop = True

    exit(0)


def connectDiscord():
    for pipe in range(9):
        global RPC
        RPC = pypresence.Presence("1184926978382516285", pipe=pipe)

        try:
            RPC.connect()
            print("Successfully connected to Discord.")

            break
        except pypresence.exceptions.InvalidPipe:
            pass


appdata_path = os.path.expanduser("~/AppData/Roaming")
file_path = os.path.join(appdata_path, "referral.txt")

clearConsole()

icon = requests.get(
    "https://cdn.discordapp.com/attachments/918997350238797855/1188893079982313583/jadebot.ico?ex=659c2df6&is=6589b8f6&hm=0c396ba697c89da2938b057f2a873d051e2565e9b947778a2f2e7aa089d84539&"
)

icon = pystray.Icon(
    "Jade Bot",
    Image.open(io.BytesIO(icon.content)),
    menu=pystray.Menu(pystray.MenuItem("Quit", quitApp)),
)


print(
    """
       _           _      ____        _   
      | |         | |    |  _ \      | |  
      | | __ _  __| | ___| |_) | ___ | |_ 
  _   | |/ _` |/ _` |/ _ \  _ < / _ \| __|
 | |__| | (_| | (_| |  __/ |_) | (_) | |_ 
  \____/ \__,_|\__,_|\___|____/ \___/ \__|
                                        
"""
)

if not os.path.exists(file_path):
    print(
        "Enter your referral link (e.g: https://whop.com/marketplace/jadebot/?a=najmul190) or press Enter: "
    )
    referral = input()

    if referral == "":
        referral = "None"
    elif (
        not referral.startswith("https://whop.com/marketplace/jadebot/")
        and referral != ""
    ):
        input("Invalid referral link.")
        exit(1)

    try:
        with open(file_path, "w") as f:
            f.write(f"{referral}||FALSE")
            referral = "https://whop.com/marketplace/jadebot/"
    except OSError as e:
        print(f"Error creating file, using default referral.")
        referral = "https://whop.com/marketplace/jadebot/"
else:
    with open(file_path, "r") as f:
        referral = f.readline().split("||")[0]
        if referral == "None":
            referral = "https://whop.com/marketplace/jadebot/"
        elif not referral.startswith("https://whop.com/marketplace/jadebot/"):
            input("Invalid referral link.")
            exit(1)

with open(file_path, "r") as f:
    startup = f.readline().split("||")[1]

if startup != "TRUE":
    print("Do you want to start this script on startup of your system? [y/n]")
    if input().lower() == "y":
        setupStartup()
    else:
        pass

    with open(file_path, "w") as f:
        f.write(f"{referral}||TRUE")

try:
    connectDiscord()
except FileNotFoundError:
    print("Discord not found, is it running? (Retrying in 15s)")
    sleep(15)
    connectDiscord()

while True:
    try:
        RPC.update(
            state="#1 Discount & Free Food Server in UK",
            large_image=(
                "https://media1.tenor.com/m/GqmhjeGS67sAAAAd/bossman-jade-bot.gif"
            ),
            large_text="Join Jade Bot today!",
            small_image=(
                "https://emoji.discadia.com/emojis/72e1d6a1-49b7-4e25-894a-b2318ec34010.GIF"
            ),
            small_text="We have thousands of vouches!",
            buttons=[
                {"label": "Discord", "url": "https://discord.gg/jadebot"},
                {
                    "label": "Sign Up",
                    "url": referral,
                },
            ],
        )

    except:
        print("Failed to connect to Discord, is it running? (Retrying in 15s)")
        sleep(15)
        connectDiscord()

    try:
        sleep(5)

        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.user32.ShowWindow(hwnd, 0)

        icon.run()

        if breakLoop:
            break

        sleep(15)

    except KeyboardInterrupt:
        print("Exiting...")
        icon.stop()
        exit(0)
