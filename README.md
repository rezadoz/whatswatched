# whatswatched
A command-line tool to track and play media files in a directory using `mpv`. It maintains a JSON-based watch history (in the form of a hidden json within the directory of the media), allowing you to resume from where you left off.

## This is for

People that want to keep track of what episode they're on in a media directory without leaving their command line... that also use `mpv`.

## Table of Contents

* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)

  * [Marking a Specific File as Current](#marking-a-specific-file-as-current)
  * [Verbose Output](#verbose-output)
  * [Help](#help)
* [How It Works](#how-it-works)
* [Data Format](#data-format)

## Features

* Scans a directory for media files with extensions: `.mp4`, `.mkv`, `.avi`, `.mov`.
* Tracks watched status and timestamps in `.whatswatched.json`.
* Allows manual setting of the current episode.
* Plays media files using `mpv`.
* Prompts to mark media as watched after playback.
* Automatically advances to the next unwatched file.

## Requirements

* Python 3.6 or higher.
* `mpv` media player 

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



## Usage

Run the script from the command line:

```bash
./whatswatched.py [options]
```

If you are doing this in a media directory for the first time, this will create the JSON file to index the videos in the directory. Then you will have to manually set the first episode with the `--current` option.

```bash
./whatswatched.py --current /path/to/Episode1.mkv
```

After doing that you can run the script without options to prompt if you want to play the current episode in that directory.

**TIP:** You can press `shift+q` to exit and save your resume posistion for when you reopen it with `mpv`. This is great if you're partially through the media file and want to resume it later. `whatswatched` is blind to this, which is why it asks you if you finished watching the media file when you exit `mpv`. If you give an affirmative input it mark the next file as the current episode and ask you to play it.

### Options

* `-c`, `--current FILENAME`
  Set a specific file as the current episode. You will have to do this with the first episode in the beginning.

* `-d`, `--dir DIRECTORY`
  Specify the working directory (defaults to the current directory).

* `-v`, `--verbose`
  Enable verbose output.

* `-h`, `--help`
  Show help message and exit.

### Marking a Specific File as Current

To set a particular file as the current episode:

```bash
./whatswatched.py -c "Episode1.mkv"
```



### Verbose Output

To enable verbose output for debugging or informational purposes. This is useless tbh and as of now just prints a confirmation message when using the `--current` option.

```bash
./media_tracker.py -v
```



### Help

To view the help message with all available options (so what you're doing now):

```bash
./media_tracker.py -h
```



## How It Works

1. **Initialization**:

   * Scans the specified directory for media files with supported extensions.
   * Creates or updates `.whatswatched.json` to track media files and their watch status.

2. **Setting Current Episode**:

   * Use the `--current` option to manually set the current episode. You'll have to do this in the beginning with the first episode.

3. **Playback Loop**:

   * If a current episode is already set, prompts the user to play it.
   * After playback, prompts to mark the episode as watched. If yes, it will update the next episode as the new current episode and prompt the user to play it.

4. **Data Persistence**:

   * Updates `.whatswatched.json` with the latest watch status and timestamps.

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
