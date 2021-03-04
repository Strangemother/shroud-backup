# shroud-backup

A mass backup util for forever store - hot and cold.

+ Track a file or directory of files
    + from CLI, Right Click (windows explorer), or API.
+ cold-store: Wasabi
+ Hot-store: backblaze


## Getting Started

The utility runs in three parts

1. The backend _shroud_ content
2. The _coms_ websocket connection
3. The _desktop_ frontend


# Install

Each unit is broken into libs and components. Each lib may be installed in the
development environment.

    # disks
    src/libs/disks/> python setup.py develop
    # coms server
    src/libs/serv/> python setup.py develop


## Dev Run

Run the backend to track data

    shroud-backup\src\backend\shroud>run.bat

Run the coms service

    shroud-backup\src\libs\serv\serv>run_hypercorn.bat

Run the UI for the desktop:

    shroud-backup\src\desktop>run.bat
