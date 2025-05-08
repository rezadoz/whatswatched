# whatswatched
A command-line tool to track and play media files in a directory using `mpv` (or whatever you want). It maintains a watch history (in the form of a hidden `.whatswatched.json` file in the same directory of the media), allowing you to track your progress, resume from where you left off, and slightly more!

## This is for

terminal-philes that want to keep track of what episode they're on in a media directory without leaving their command line

## Table of Contents

* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [How It Works](#how-it-works)
* [Data Format](#data-format)

## Features

* Scans a directory for media files with extensions: `.mp4`, `.mkv`, `.avi`, `.mov`. (line 19 of code)
* Tracks watched status and timestamps in `.whatswatched.json`.
* Allows manual setting of the current episode or watched flags.
* Plays media files using `mpv` by default, different command strings can be supplied with the `--player` option.
* Prompts to mark media as watched after playback (which advances the set current episode) and prompts the user to contine the current episode playback loop

## Requirement

* Python 3.6 or higher.
* `mpv` media player (or whatever media player you want that can be launched from command line such as `vlc`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/rezadoz/whatswatched.git
   ```



2. Navigate to the project directory:

   ```bash
   cd whatswatched
   ```



3. Ensure the script is executable:

   ```bash
   chmod +x whatswatched.py
   ```

4. (Optional) put it somewhere else, make an alias for your shell or symlink to use the script like a command

## Usage

Run the script from the command line:

```bash
./whatswatched.py [options]
```

If you are doing this in a media directory for the first time, this will create the JSON file to index the videos in the directory.

**TIP:** You can press `shift+q` to exit and save your resume posistion for when you reopen it with `mpv`. This is great if you're partially through the media file and want to resume it later. `whatswatched` is blind to this, which is why it asks you if you finished watching the media file when you exit `mpv`. If you give an affirmative input it mark the next file as the current episode and ask you to play it.

### Options

* `-c`, `--current FILENAME`
  Set a specific file as the current episode.

* `-n`, `--null-current`
  Set the current episode to none.

* `-o`, `--open FILENAME`
  Open a specific file, you may have order this before `--player`

* `-p`, `--player "COMMAND STRING"`
  Supply an alternative command string like "mpv --loop" or "vlc"

* `-d`, `--dir DIRECTORY`
  Specify the working directory (defaults to the current directory).

* `-w`, `--watched [FILENAME1 FILENAME2 ...]`
  Flag specific file(s) as watched. If no file(s) are supplied it will flag all of them.


* `-u`, `--unwatched [FILENAME1 FILENAME2 ...]`
  Flag specific file(s) as inwatched. If no file(s) are supplied it will flag all of them.

* `-s`, `--stats`
  Show some stats about the working media directory such as your progress.

* `-h`, `--help`
  Show help message and exit.

## How It Works

1. **Initialization**:

   * Scans the specified directory for media files with supported extensions.
   * Creates or updates `.whatswatched.json` to track media files and their watch status.

2. **Setting Current Episode**:

   * Use the `--current` option to manually set the current episode. You'll have to do this in the beginning with the first episode.

3. **Playback Loop**:

   * If a current episode is already set, prompts the user to play it.
   * After playback, prompts to mark the episode as watched. If yes, it will update the next episode as the new current episode and prompt the user continue the loop by playing the next episode.

4. **Data Persistence**:

   * Updates `.whatswatched.json` (located in the same directory of the media) with the latest watch status and timestamps.

## Data Format

The `.whatswatched.json` file maintains the following structure:

```json
{
  "files": {
    "Episode1.mkv": {
      "path": "/path/to/Episode1.mkv",
      "watched": true,
      "watched_date": "2025-05-07T22:15:30"
    },
    "Episode2.mkv": {
      "path": "/path/to/Episode2.mkv",
      "watched": false,
      "watched_date": null
    }
  },
  "current_episode": "Episode2.mkv"
}
```
