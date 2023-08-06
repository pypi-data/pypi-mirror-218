import os
import luddite
import argparse

from . import (
    __title__ as title,
    __full_title__ as full_title,
    __description__ as description,
    __copyright__ as copyright,
    __version__ as version
)
from . import color
from .start import main as start

if os.name == "nt":
    # windows
    from pyreadline3 import Readline
    readline = Readline()
else:
    # macOS/linux
    import readline

def main():
    parser = argparse.ArgumentParser(
        prog = title,
        description = description,
        epilog = f"Example: {title} -f audio_file.mp3"
    )

    parser.add_argument("-f", "--file",
                        help="audio file to edit")
    parser.add_argument("-i", "--interactive",
                        action="store_true", help="start an interactive conversion")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="print more output")
    parser.add_argument("-V", "--version",
                        action="version", version=full_title+" "+version)
    parser.add_argument("-l", "--license",
                        action="version", version=copyright+" - MIT License. For more information see: https://opensource.org/license/mit/",
                        help="show program's license and exit")
    parser.add_argument("-r", "--remove-metadata",
                        action="store_true", help="remove every song metadata and then show the options")
    parser.add_argument("-U", "--update",
                        action="store_true", help="show update program command and exit")

    args = parser.parse_args()

    if args.update:
        try:
            new_version = luddite.get_version_pypi(full_title)
        except:
            new_version = None

        print(f"Installed version: {version}")
        print(f"PyPi version: {new_version}")
        print()

        if new_version and version != new_version:
            print(f"{color.bright_blue}{version} {color.bright_green}>> {color.bright_blue}{new_version}{color.reset}")
        
        print(f"{color.bright_white}Use {color.bright_red}pip install -U {full_title}{color.bright_white} to update!{color.reset}")
        exit()

    if not args.interactive and not args.file:
        parser.error("Specify either a file or pass `-i` for an interactive session.")

    start(args)

    try:
        new_version = luddite.get_version_pypi(full_title)
    except:
        new_version = None
    
    if new_version and version != new_version:
        print()
        print(f"{color.bright_green}New version for {color.bright_yellow}{full_title}{color.bright_green} is available.{color.reset}")
        print(f"{color.bright_blue}{version} {color.bright_green}>> {color.bright_blue}{new_version}{color.reset}")
        print(f"{color.bright_white}Use {color.bright_red}pip install -U {full_title}{color.bright_white} to update!{color.reset}")

if __name__ == "__main__":
    main()