# Dreamspeaker

A deep learning Discord TTS bot that clones voices.

*Click the video thumbnail below to watch the YouTube video.*

[![YouTube Video](https://i.ytimg.com/vi_webp/NdyOZWh9vNo/maxresdefault.webp)](https://youtu.be/NdyOZWh9vNo)

## About

This project actually started off as a joke. Me and my friends like to use a TTS bot so that if someone can’t speak, they can still take part in conversation. I find that it’s easy for people to ignore mute users because you have to actively monitor the chat. When using a TTS bot, people can better participate in conversation because you can actually be heard.

The only problem is that it becomes more difficult to figure out who is speaking, especially when multiple people are using TTS. Hearing a distinct and recognizable voice allows you to subconsciously link the voice to a person at any time in the sentence.

All of the actual AI processing is from a project called [coqui](https://github.com/coqui-ai/TTS). It’s a super capable toolkit and all credit for the voice processing goes to them. To actually make it clone a voice, it needs a reference recording. Any recording will do, and you only really need between five and twenty seconds of audio. The bot automatically uses the correct reference based on the command sender. That way, only you can use your voice.

## Installation

> [!WARNING]
>
> This project uses Coqui XTTS v2, which allows only non-commercial use of the model and its outputs. **Using this bot for commercial purposes is not permitted.**
>
> You can read the full Coqui Public Model License 1.0.0 at <https://coqui.ai/cpml>.

### 1. Create a Discord bot

1. Go to https://discord.com/developers/applications and create a new application. Give it any name, description, or icon.
2. Go to the **Bot** tab.
3. Scroll down and look for MESSAGE CONTENT INTENT under _Privileged Gateway Intents_. Enable the toggle.
4. Under the **OAuth2** tab, go to **OAuth2 URL Generator**. Check the _bot_ box. In the second table, check the _Read Messages/View Channels_, _Connect_, _Speak_, _Send Messages_, and _Attach Files_ boxes.
5. Copy the URL and open it. Invite the bot to your server. Repeat for any servers you want to add the bot to.
6. Go back to the **Bot** tab and find the _Token_. Reset and copy it into a temporary text file. We'll need it later.

### 2. Install

Clone this repository or download it as a ZIP and extract to a convenient location.

```bash
git clone https://github.com/BogTheMudWing/Dreamspaker.git
cd Dreamspeaker
```

Create and activate a virtual environment. Python 3.10 is recommended, but you may be able to use others.

```bash
python3.10 -m venv ./venv
source ./venv/bin/activate
```

Install ffmpeg. This will differ depending on your operating system, so search for instructions.

Install requirements. It may take a while. It took 15 minutes for me.

```bash
# The tmp directory is temporarily changed here because I ran into issues where my default /tmp is not large enough, and you may run into the same issue.
TMPDIR=/var/tmp pip install -r requirements.txt
git clone https://github.com/coqui-ai/TTS
pip install -e ./TTS/
```

Add your bot token to .env. Replace `YOUR_BOT_TOKEN_HERE` with your bot token.

```bash
echo BOT_TOKEN=YOUR_BOT_TOKEN_HERE >> .env
```

Start the bot to initialize the model.

```bash
python Dreamspeaker.py
```

At the prompt, input `y` to accept the terms of the non-commercial CPML, then wait for the model to download.

At this point, you can start using it or stop it with Ctrl + C.

## Operation

Each time you want to start the bot, run this command:

```bash
./venv/bin/python Dreamspeaker.py
```

When you want to shut down the bot, press `Ctrl + C`. It may take a while to shut down completely, but it is not dangerous to repeat `Ctrl + C` to ask it to stop. You can delete `compose.yml` if you want to, but it is useful to have for future maintenance.

## Commands

### `!ref`

Add a reference for yourself. When you use this command, upload an audio file as an attachment of your voice (or whatever voice you want your TTS to sound like). The file will be automatically converted to WAV and saved. If you already had a reference, it will be overwritten. 

### `!tts <message>`

Use TTS. This command must be used while in a VC. The user must have their own reference audio file in the `reference` folder with the name `[usermame].wav`, replacing `[username]` with the username of the user (not their server nickname). This can be set by them using the `!ref` command above.

### `!voice <voice> <message>`

Generate a file from a voice. Voices are stored in the `voices` folder. I've included the `dramatic` voice, which comes from a public-domain LibreVox audiobook. The reader's name is Martin Martin Geeson.

### `!leave`

Ask the bot to leave the voice channel.

## Uninstallation

Delete the Dreamspeaker folder.

## Thanks to

- Coqui for the TTS engine and model.
- Discord for their developer API.
- discord.py for the Discord Python library.
- GitHub for hosting my code.

---

[![Bog The MudWing](https://blog.macver.org/content/images/2025/07/Stamp-Colored-Small-Shadow.png)](https://blog.macver.org/about-me)
