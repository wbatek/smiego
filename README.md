# smiego

Smiego is a Discord bot that performs two main tasks:

1. It automatically kicks specified users from voice channels at regular intervals.
2. It joins voice channels to play a random audio file when a specific user is present, then leaves the channel after playing.

# Features
Automatic User Kicking: The bot monitors voice channels and kicks users listed in a users_to_kick.txt file at regular intervals.
Audio Playback: The bot joins a voice channel when a specific user (e.g., wbatek) is present, plays a random audio file from the recordings directory, and then disconnects.
