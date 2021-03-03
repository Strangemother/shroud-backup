# shroud-backup

A mass backup util for forever store - hot and cold.

+ Track a file or directory of files
    + from CLI, Right Click (windows explorer), or API.
+ cold-store: Wasabi
+ Hot-store: backblaze


# cold store

Forever store content for one-time offsite backups

+ Massive long-term store


# hot store

share and fast download of assets

+ Site to Site share, hot care,
+ Friend share.


# background care

Files _unchanged_ in hot may push to cold after X months.


# Auto tracking

Files may be auto-tracked, allowing the persistent monitoring of a drive or many
files.

1. An auto tracked file may be _fully_ uploaded to hot or cold store.
2. A auto tracked file may be _history_ tracked through an auto git.

## File detection

A user may opt to _watch_ for any file within a sub directory - or a single drive.
If the file is _tracked_, it's digested. If it's new (and not ignored), it's logged
for the user to verify.


## history

history tracked files will not _cold-store_ but may automatically hot-store.
However, large _chunking_ through weekly changes into HOT can persist into COLD
as a partial. The git tree will handle rebuilds upon download.

---

# Interface

## Local

+ A local CEF UI, with a background app running on a multiprocess thread.
+ Commiting to a local or remote location


## Remote

For account centralisation, and payments


## Getting Started

The first app entry serves a welcome screen and an intro page. The user may continue with login (or not) and configure the app to track files and DIRS.

Upon the background thread, the drive scans for drives.

