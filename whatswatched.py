import os
import sys
import json
import argparse
import subprocess
import shlex
from datetime import datetime

ASCII_ART = r"""
 _      ___      __
| | /| / / | /| / /
| |/ |/ /| |/ |/ /~~~whatswatched
|__/|__/ |__/|__/
"""

DEFAULT_JSON = ".whatswatched.json"
DEFAULT_PLAYER = "mpv"

EXTS = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm')


def get_media_files(directory):
    return sorted([f for f in os.listdir(directory) if f.lower().endswith(EXTS)])


def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {"files": {}, "current_episode": None}


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_index(directory, json_path, data):
    media_files = get_media_files(directory)
    for f in media_files:
        if f not in data['files']:
            data['files'][f] = {
                "path": os.path.abspath(os.path.join(directory, f)),
                "watched": False,
                "watched_date": None
            }
    data['files'] = {k: v for k, v in data['files'].items() if k in media_files}
    return data


def prompt_yes_no(message):
    resp = input(message + "\nY/n? ").strip().lower()
    if resp in ('', 'y', 'yes'):
        return True
    print("OK bye")
    sys.exit(0)


def play_file(cmd, path):
    subprocess.run(cmd + [path])


def get_next_unwatched(files):
    for k, v in files.items():
        if not v["watched"]:
            return k
    return None


def mark_watched(data, file):
    now = datetime.now().isoformat()
    data["files"][file]["watched"] = True
    data["files"][file]["watched_date"] = now
    files_list = list(data['files'].keys())
    i = files_list.index(file)
    if i + 1 < len(files_list):
        data['current_episode'] = files_list[i + 1]
    else:
        data['current_episode'] = None


def handle_stats(data, directory):
    watched = [k for k, v in data['files'].items() if v['watched']]
    unwatched = [k for k, v in data['files'].items() if not v['watched']]
    total = len(data['files'])
    watched_count = len(watched)
    percent = int((watched_count / total) * 100) if total else 0
    print("watched: " + ", ".join(f'\"{f}\"' for f in watched))
    print("---")
    print("unwatched: " + ", ".join(f'\"{f}\"' for f in unwatched))
    print("---")
    print(f'"{os.path.basename(directory)}": {watched_count}/{total} episodes watched ({percent}% complete)')
    print(f'current episode: "{data["current_episode"]}")


def main():
    parser = argparse.ArgumentParser(description="whatswatched media indexer and player", add_help=False)
    parser.add_argument("-c", "--current", nargs=1)
    parser.add_argument("-n", "--null-current", action="store_true")
    parser.add_argument("-u", "--unwatched", nargs="*")
    parser.add_argument("-w", "--watched", nargs="*")
    parser.add_argument("-d", "--dir", default=os.getcwd())
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-p", "--player", nargs=argparse.REMAINDER)
    parser.add_argument("-o", "--open", nargs=1)
    parser.add_argument("-s", "--stats", action="store_true")
    args = parser.parse_args()

    directory = os.path.abspath(args.dir)
    json_path = os.path.join(directory, DEFAULT_JSON)
    data = load_json(json_path)
    data = update_index(directory, json_path, data)

    if args.help:
        print("Usage: whatswatched [options]\nOptions:\n")
        print("  -c, --current <file>       Set specified file as current_episode")
        print("  -n, --null-current         Set current_episode to null")
        print("  -u, --unwatched [...]      Mark all/specified files as unwatched")
        print("  -w, --watched [...]        Mark all/specified files as watched")
        print("  -d, --dir <directory>      Use specified working directory")
        print("  -h, --help                 Show this help message")
        print("  -p, --player <command>     Use alternate media player")
        print("  -o, --open <file>          Open specific file and enter playback logic")
        print("  -s, --stats                Print watched/unwatched stats")
        print("\nMore info at https://github.com/rezadoz/whatswatched")
        return

    if args.current:
        file = args.current[0]
        if file in data['files']:
            data['current_episode'] = file
            save_json(json_path, data)
            print(f'Current episode set to: {file}')
        else:
            print(f'File "{file}" not found in index.')
        return

    if args.null_current:
        data['current_episode'] = None
        save_json(json_path, data)
        print("Current episode set to null.")
        return

    if args.unwatched is not None:
        targets = args.unwatched or data['files'].keys()
        for f in targets:
            if f in data['files']:
                data['files'][f]['watched'] = False
                data['files'][f]['watched_date'] = None
        save_json(json_path, data)
        print("Marked as unwatched.")
        return

    if args.watched is not None:
        now = datetime.now().isoformat()
        targets = args.watched or data['files'].keys()
        for f in targets:
            if f in data['files']:
                data['files'][f]['watched'] = True
                data['files'][f]['watched_date'] = now
        save_json(json_path, data)
        print("Marked as watched.")
        return

    if args.stats:
        handle_stats(data, directory)
        return

    player_cmd = shlex.split(args.player[0]) if args.player else [DEFAULT_PLAYER]

    if not args.open:
        print(ASCII_ART)

    file_to_play = None
    if args.open:
        file_to_play = args.open[0]
    elif data["current_episode"]:
        file_to_play = data["current_episode"]
        prompt_yes_no(f"play current episode? {file_to_play}")
    else:
        file_to_play = get_next_unwatched(data['files'])
        if file_to_play:
            prompt_yes_no(f"no current episode, play first unwatched file in directory? {file_to_play}")
        else:
            print("No unwatched files found.")
            return

    while file_to_play:
        play_file(player_cmd, data['files'][file_to_play]['path'])
        if prompt_yes_no("mark media as watched?"):
            mark_watched(data, file_to_play)
            save_json(json_path, data)
            file_to_play = data['current_episode']
            if file_to_play:
                prompt_yes_no(f"play next file? {file_to_play}")
            else:
                print("No more episodes.")
                return
        else:
            return


if __name__ == "__main__":
    main()
