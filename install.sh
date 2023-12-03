#! /bin/bash

# Prompt for bot token
if zenity --entry --hide-text --text="Please paste your bot token below" --title="Dreamspeaker Installation"
then

    # Edit file
    sed -i "s/YOUR_DISCORD_BOT_TOKEN/$?/" Dreamspeaker.py | zenity --progress --pulsate --auto-close --auto-kill --text="Saving bot token..." --title="Dreamspeaker Installation"

    pip install TTS | zenity --progress --pulsate --auto-close --auto-kill --text="Installing Python dependencies..." --title="Dreamspeaker Installation"
    git clone https://github.com/coqui-ai/TTS | zenity --progress --pulsate --auto-close --auto-kill --text="Cloning repository..." --title="Dreamspeaker Installation"
    pip install -e ./TTS/ | zenity --progress --pulsate --auto-close --auto-kill --text="Installing repository with Python..." --title="Dreamspeaker Installation"
    make system-deps | zenity --progress --pulsate --auto-close --auto-kill --text="Making TTS..." --title="Dreamspeaker Installation"
    make install | zenity --progress --pulsate --auto-close --auto-kill --text="Installing TTS..." --title="Dreamspeaker Installation"
    rm ./install
    if zenity --question --text="Installation complete sucessfully. Do you want to run the bot now to complete installation?" --title="Dreamspeaker Installation"
    then
        x-terminal-emulator -e python3 ttsbot.py
    fi
fi