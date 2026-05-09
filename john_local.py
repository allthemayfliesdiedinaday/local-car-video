import requests
import random
import re
import datetime
import subprocess
import textwrap

# you can get a giphy key from https://developers.giphy.com/
# replace the placeholder with the actual key ^^

GIPHY_KEY = "YOUR_KEY_HERE"

# fetches a random cat .gif/.mp4 from the giphy API, ensures cat gif isn't reused by tracking id in used-cats.txt
# also saves the original unedited .gif and .mp4 if you want those

def get_cat_video():
    used_cats = set()

    # loads used cat ids from used-cats.txt

    try:
        with open("used-cats.txt") as f:
            used_cats = {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        pass

    # this keeps asking the API for a cat until we haven't found an unused cat, keep in mind you have max 100 requests per hour
    # so you might want to limit how many times it asks

    while True:
        url = (
            f"https://api.giphy.com/v1/gifs/random?tag=cat&rating=g&api_key={GIPHY_KEY}"
        )
        data = requests.get(url).json()
        gif_id = data["data"]["id"]

        # if gif is found this breaks the loop

        if gif_id not in used_cats:
            break

    # gets info about the file from the API and does the downloading

    mp4 = data["data"]["images"]["original_mp4"]["mp4"]

    r = requests.get(mp4)
    with open("cat.mp4", "wb") as f:
        f.write(r.content)

    with open("used-cats.txt", "a") as f:
        f.write(gif_id + "\n")

    gif_url = data["data"]["images"]["original"]["url"]
    r_gif = requests.get(gif_url)
    with open("cat.gif", "wb") as f:
        f.write(r_gif.content)

# takes a random track from tracks.txt and downloads it
# some of these don't work because i fucked up the formatting :D

def get_random_track():
    with open("tracks.txt") as f:
        tracks = [line.strip() for line in f if line.strip()]

    if not tracks:
        raise Exception("tracks.txt is empty")

    track = random.choice(tracks)

    print("Downloading:", track)

    r = requests.get(track)
    r.raise_for_status()

    with open("music.mp3", "wb") as f:
        f.write(r.content)


def make_video():

    today = datetime.datetime.now()
    day = today.day
    filename = today.strftime("%d %B %Y") + ".mp4"

    # you could make a function to do this for both the gif and the mp4, or just render the generated mp4 as a gif ¯\_(ツ)_/¯
    if day in [1, 21, 31]:
        suffix = "st"
    elif day in [2, 22]:
        suffix = "nd"
    elif day in [3, 23]:
        suffix = "rd"
    else:
        suffix = "th"

    text = f"post this cat on the {day}{suffix} day of the month"

    wrapped = "\n".join(textwrap.wrap(text, width=20))

    banner_height = 200

    filter_chain = (
        f"pad=iw:ih+{banner_height}:0:{banner_height}:color=white,"
        f"drawtext=text='{wrapped}':"
        f"x=(w-text_w)/2:"
        f"y=({banner_height}-text_h)/2:"
        f"fontsize=48:"
        f"fontcolor=black:"
        f"line_spacing=10:"
        f"fontfile=./arial.ttf"  # change this to your preferred font
    )

    start_time = random.randint(0, 30)

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        "cat.mp4",
        "-ss",
        str(start_time),
        "-i",
        "music.mp3",
        "-vf",
        filter_chain,
        "-ar",
        "8000",
        "-shortest",
        filename,
    ]

    subprocess.run(cmd)

    print("Saved:", filename)


def make_thumbnail():

    today = datetime.datetime.now()
    day = today.day

    if day in [1, 21, 31]:
        suffix = "st"
    elif day in [2, 22]:
        suffix = "nd"
    elif day in [3, 23]:
        suffix = "rd"
    else:
        suffix = "th"

    text = f"post this cat on the {day}{suffix} day of the month"
    wrapped = "\n".join(textwrap.wrap(text, width=20))

    banner_height = 200

    filter_chain = (
        f"pad=iw:ih+{banner_height}:0:{banner_height}:color=white,"
        f"drawtext=text='{wrapped}':"
        f"x=(w-text_w)/2:"
        f"y=({banner_height}-text_h)/2:"
        f"fontsize=48:"
        f"fontcolor=black:"
        f"line_spacing=10:"
        f"fontfile=./arial.ttf"  # change this to your preferred font
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        "cat.gif",
        "-vf",
        filter_chain,
        "cat_banner.gif",
    ]

    subprocess.run(cmd)


def main():
    get_cat_video()
    get_random_track()
    make_video()
    make_thumbnail()

    today = datetime.datetime.now().strftime("%d %B %Y") + ".mp4"


main()
