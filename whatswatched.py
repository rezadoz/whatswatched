#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

ASCII_ART = r"""
           __          __                      __       __             __
 _      __/ /_  ____ _/ /_______      ______ _/ /______/ /_  ___  ____/ /
| | /| / / __ \/ __ `/ __/ ___/ | /| / / __ `/ __/ ___/ __ \/ _ \/ __  /
| |/ |/ / / / / /_/ / /_(__  )| |/ |/ / /_/ / /_/ /__/ / / /  __/ /_/ /
|__/|__/_/ /_/\__,_/\__/____/ |__/|__/\__,_/\__/\___/_/ /_/\___/\__,_/
"""

WATCH_FILE = ".whatswatched.json"
SUPPORTED_EXTS = {".mp4", ".mkv", ".avi", ".mov"}

def load_watch_data(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {"files": {}, "current_episode": None}

def save_watch_data(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def get_media_files(directory):
    return sorted([f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in SUPPORTED_EXTS])

def ask(prompt):
    print(f"{prompt}\nY/n? ", end='')
    answer = input().strip().lower()
    return answer in {"", "y", "yes"}

def play_file(path):
    subprocess.run(["mpv", path])

def main():
    parser = argparse.ArgumentParser(description="Track and play media progress in a directory.", add_help=False)
    parser.add_argument("-c", "--current", metavar="FILENAME", help="Mark a specific file as the current episode")
    parser.add_argument("-d", "--dir", default=os.getcwd(), help="Set the working directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    args = parser.parse_args()

    print(ASCII_ART)

    directory = os.path.abspath(args.dir)
    watch_path = os.path.join(directory, WATCH_FILE)

    data = load_watch_data(watch_path)
    media_files = get_media_files(directory)

    updated = False
    for f in media_files:
        if f not in data["files"]:
            data["files"][f] = {
                "path": os.path.join(directory, f),
                "watched": False,
                "watched_date": None
            }
            updated = True
    if updated and args.verbose:
        print("[INFO] Media file list updated.")

    if args.current:
        if args.current not in data["files"]:
            print(f"[ERROR] {args.current} not found in media files.")
            sys.exit(1)
        data["current_episode"] = args.current
        if args.verbose:
            print(f"[INFO] Set current episode to {args.current}")
        save_watch_data(watch_path, data)
        sys.exit(0)

    save_watch_data(watch_path, data)

    while data["current_episode"]:
        current = data["current_episode"]
        entry = data["files"].get(current)
        if not entry:
            print(f"[ERROR] Current episode '{current}' not found in media list.")
            break

        if ask(f"play current episode? {current}"):
            play_file(entry["path"])

            if ask("mark media as watched?"):
                entry["watched"] = True
                entry["watched_date"] = datetime.now().isoformat(timespec='seconds')

                keys = sorted(data["files"].keys())
                try:
                    idx = keys.index(current)
                    for next_file in keys[idx + 1:]:
                        if not data["files"][next_file]["watched"]:
                            data["current_episode"] = next_file
                            break
                    else:
                        data["current_episode"] = None
                except ValueError:
                    data["current_episode"] = None

                save_watch_data(watch_path, data)
                if data["current_episode"]:
                    continue
                else:
                    print("OK bye")
                    break
            else:
                print("OK bye")
                break
        else:
            print("OK bye")
            break

if __name__ == "__main__":
    main()
