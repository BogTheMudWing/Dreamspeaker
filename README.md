# Dreamspeaker
A deep learning Discord TTS bot that clones voices.

![https://i.ytimg.com/vi_webp/NdyOZWh9vNo/maxresdefault.webp](https://youtu.be/NdyOZWh9vNo)

This project actually started off as a joke. Me and my friends like to use a TTS bot so that if someone can’t speak, they can still take part in conversation. I find that it’s easy for people to ignore mute users because you have to actively monitor the chat. When using a TTS bot, people can better participate in conversation because you can actually be heard.

The only problem is that it becomes more difficult to figure out who is speaking, especially when multiple people are using TTS. Hearing a distinct and recognizable voice allows you to subconsciously link the voice to a person at any time in the sentence.

All of the actual AI processing is from a project called [coqui](https://github.com/coqui-ai/TTS). It’s a super capable toolkit and all credit for the voice processing goes to them. To actually make it clone a voice, it needs a reference recording. Any recording will do, but I’ve found it works best when reading the FitnessGram Pacer Test introduction. Then, test with some different phrases and if the bot struggles with a sentence, add to the recording your own reading of the sentence. Rinse and repeat until it can properly speak sentences. The bot automatically uses the correct reference based on the command sender. That way, only you can use your voice.

## Installation

This installation is intended for Ubuntu 18.04 / 20.04 / 22.04. I hope to add Windows 10/11 and MacOS automatic installation in the future.

### 1. Create a Discord bot
1. Go to https://discord.com/developers/applications and create a new application. Give it any name, description, or icon.
2. Go to the **Bot** tab and create a bot. Give it a name.
3. Scroll down and look for MESSAGE CONTENT INTENT under _Privileged Gateway Intents_. Enable the toggle.
4. Under the **OAuth2** tab, go to **URL Generator**. Check the _bot_ box. In the second table, check the _Read Messages/View Channels_, _Connect_, _Speak_, _Send Messages_, and _Attach Files_ boxes.
5. Copy the URL and open it. Invite the bot to your server. Go back to the **Bot** tab and find the _Bot Token_. Reset and copy it. We'll need it later.

### 2. Install
Clone this repository or download it as a ZIP and extract to a convenient location.

Run the  `install.sh` script. If double-clicking it does not work, enable execution in the properties or use `bash path/to/install.sh` in a terminal.

Paste the bot token into the prompt, then wait while installation occurs. After installation, you will be asked if you want to run the bot. Whether you do or not, you will need to accept coqui's EULA and download the XTTS v1.1 model when you run the bot for the first time. Simply type `y` and press enter at the prompts.

### 3. Setup
You're done with installation! Now you just need to add reference audio files. See below for more information.

## Commands

### `!tts <message>`

Use TTS. This command must be used while in a VC. The user must have their own reference audio file in the `reference` folder with the name `[usermame].wav`, replacing `[username]` with the username of the user (not their server nickname).

### `!voice <voice> <message>`

Generate a file from a voice. Voices are stored in the `voices` folder. I've included the `dramatic` voice, which comes from a public-domain LibreVox audiobook. The reader's name is Martin Martin Geeson.

### `!leave`

Ask the bot to leave the voice channel.
