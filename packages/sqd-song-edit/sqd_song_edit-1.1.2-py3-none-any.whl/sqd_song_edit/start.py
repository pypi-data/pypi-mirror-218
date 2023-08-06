import os
import time
import eyed3
import argparse
from sqdconvert.utils import convert
from sqdconvert.config import get_config

from . import color

__all__ = [
    "main"
]

def main(args: argparse.ArgumentParser) -> None:
    try:
        saved = None

        if args.interactive:
            args.file = input(f"{color.bright_blue}Song file to edit: {color.bright_white}").strip()

            if args.file.startswith('"') and args.file.endswith('"'):
                args.file = args.file.split('"', 1)[1].rsplit('"', 1)[0]
            elif args.file.startswith("'") and args.file.endswith("'"):
                args.file = args.file.split("'", 1)[1].rsplit("'", 1)[0]

        inp = os.path.normpath(args.file)
        if os.path.exists(inp):
            if not os.path.isfile(inp):
                print(f"💥 {color.red}Input at the specified location is not a file: {color.bright_yellow}'{inp}'{color.reset}")
                exit()
        else:
            print(f"💥 {color.red}File not found: {color.bright_yellow}'{inp}'{color.reset}")
            exit()
        
        filepath = inp
        if not inp.endswith(".mp3"):
            filepath = filepath.rsplit(".", 1)[0]+".mp3"
            print(f"⚠️ {color.yellow}Any audio file other than `.mp3` is not supported at the moment. This program will try to auto-convert the provided file.{color.reset}")
            config = get_config()
            print("It is recommended you specify the ffmpeg path in the sqdconvert config if not done already.")
            print(f"⚠️ {color.yellow}Using {color.red}{config.ffmpeg_path}{color.yellow} as the ffmpeg path.{color.reset}")
            status = convert(config.ffmpeg_path, inp, filepath, verbose=args.verbose)
            if status != 0:
                print(f"💥 {color.red}Failed to convert the audio file.{color.reset}")
                exit()

        eyed3.log.setLevel("VERBOSE" if args.verbose else "ERROR")
        song = eyed3.load(filepath)
        saved = False
        
        write = False
        if not song.tag or args.remove_metadata:
            write = True
            song.initTag()

        def get_tag(tag):
            if write:
                return "[]"
            else:
                return f"[{'' if tag is None else tag}]"

        print(f"{color.bright_green}Anything in square brackets {color.bright_yellow}([]){color.bright_green} is a default value.{color.reset}")
        print(f"{color.bright_green}If you don't type anything and press enter, the default value will automatically be selected.{color.reset}")
        print(f"{color.bright_green}If you type {color.bright_yellow}`.rm`{color.bright_green} in any of the following, the value in it will be removed.{color.reset}")

        artist = input(f"{color.bright_blue}Artist Name {color.bright_yellow}{get_tag(song.tag.artist)}{color.bright_blue}: {color.bright_white}").strip()
        print(end=color.reset)
        if artist != "":
            if artist == ".rm":
                song.tag.artist = None
            else:
                song.tag.artist = artist

        title = input(f"{color.bright_blue}Song Title {color.bright_yellow}{get_tag(song.tag.title)}{color.bright_blue}: {color.bright_white}").strip()
        print(end=color.reset)
        if title != "":
            if title == ".rm":
                song.tag.title = None
            else:
                song.tag.title = title

        album = input(f"{color.bright_blue}Album {color.bright_yellow}{get_tag(song.tag.album)}{color.bright_blue}: {color.bright_white}").strip()
        print(end=color.reset)
        if album != "":
            if album == ".rm":
                song.tag.album = None
            else:
                song.tag.album = album
        
        genre = input(f"{color.bright_blue}Genre {color.bright_yellow}{get_tag(song.tag.genre)}{color.bright_blue}: {color.bright_white}").strip()
        print(end=color.reset)
        if genre != "":
            if genre == ".rm":
                song.tag.genre = None
            else:
                song.tag.genre = genre
        
        cover_art = input(f"{color.bright_blue}Cover Art Location {color.bright_yellow}[Don't change]{color.bright_blue}: {color.bright_white}").strip()
        print(end=color.reset)
        if cover_art != "":
            if genre == ".rm":
                song.tag.genre = False
            else:
                if cover_art.startswith('"') and cover_art.endswith('"'):
                    cover_art = cover_art.split('"', 1)[1].rsplit('"', 1)[0]
                elif cover_art.startswith("'") and cover_art.endswith("'"):
                    cover_art = cover_art.split("'", 1)[1].rsplit("'", 1)[0]

                cover_art = os.path.normpath(cover_art)
                if os.path.exists(cover_art):
                    if not os.path.isfile(cover_art):
                        print(f"{color.red}Input at the specified location is not a file: {color.bright_yellow}'{cover_art}'{color.reset}")
                        print(f"{color.red}Removing Cover Art...{color.reset}")
                        cover_art = False
                else:
                    print(f"{color.red}File not found: {color.bright_yellow}'{inp}'{color.reset}")
                    print(f"{color.red}Removing Cover Art...{color.reset}")
                    cover_art = False

                if cover_art:
                    if not cover_art.endswith(".png") and \
                       not cover_art.endswith(".jpg") and not cover_art.endswith(".jpeg"):
                        print(f"{color.red}Cover art must only be a PNG or JPG/JPEG.{color.reset}")
                        print(f"{color.red}Skipping Cover Art...{color.reset}")
                        cover_art = None
                    else:
                        if cover_art.endswith(".png"):
                            cover_art_mime = "image/png"
                        else:
                            cover_art_mime = "image/jpeg"
        else:
            cover_art = None
        
        if cover_art is False:
            # if cover art is to be removed
            try: song.tag.images.remove("")
            except: pass
        elif cover_art is None:
            # if cover art is to be skipped
            pass
        else:
            # if cover art is to be added
            with open(cover_art, "rb") as cover_art_file:
                song.tag.images.set(3, cover_art_file.read(), cover_art_mime)
        
        print()
        print(f"{color.bright_green}Saving your audio file...{color.reset}")
        while True:
            try:
                song.tag.save(version=eyed3.id3.ID3_V2_3) # save audio file
            except PermissionError:
                print(f"💥 {color.red}Could not save the audio file! Make sure to close any music app that could be accessing this file.{color.reset}")
                print(f"{color.bright_blue}Retrying in 3 seconds...{color.reset} {color.green}Ctrl + C to stop.{color.reset}")
                time.sleep(3)
            else:
                break
        saved = True
        print(f"👌 {color.bright_green}Successfully updated your audio file.{color.reset}")

    except KeyboardInterrupt:
        if saved is False:
            print(f"\n{color.reset}{color.red}exiting without saving...{color.reset}")
        else:
            print(f"\n{color.reset}{color.red}exiting...{color.reset}")