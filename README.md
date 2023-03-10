# Discord Line Message Sync

ð [ç¹é«ä¸­æçREADME.md](#Discord-Line-è¨æ¯åæ­¥æ©å¨äºº) ð

## A bot that syncs messages between Discord and Line

This bot is made to sync all kinds of messages between Discord and Line, using four applications including Line bot,
Line Notify, Discord bot and Discord webhook.

imgs/gifs

Below is a list of supported message types:

| Line -----to----> Discord   | Support |
|:----------------------------|:-------:|
| Text Message                |   âï¸    |
| Pictures                    |   âï¸    |
| Videos                      |   âï¸    |
| Audios                      |   âï¸    |
| Files                       |   âï¸    |
| Sticker                     |   âï¸    |
| Location                    |   âï¸    |
| Any other types of messages |   âï¸    |

| Discord -----to----> Line                    | Support |
|:---------------------------------------------|:-------:|
| Text Message                                 |   âï¸    |
| Pictures (jpg, jpeg, png)                    |   âï¸    | 
| Videos (mp4)                                 |   âï¸    |
| Audios (m4a, mp3, wav, aac, flac, ogg, opus) |   âï¸    |
| Other formats files                          |    â    |
| GIFs                                         |    â    |
| Sticker                                      |    â    |
| Any other types of messages                  |    â    |

You can definitely host this service yourself! and it's free!
Find it out by the following tutorial!

---

## Getting started to use the bot

### How to use

1. Download the latest release from [here](https://github.com/HappyGroupHub/Discord-Line-Message-Sync/releases)
2. Unzip the file then open up `config.yml`, [Notepad++](https://notepad-plus-plus.org/downloads/) is recommended
3. Fill in the following required information, see [here](#About-config.yml) for more details
4. Now run `run.bat` to start the bot
5. Make sure you've invited the bot to your Discord server and added it / Line Notify to your Line group
6. Enjoy!

### About config.yml

```yaml
# ++--------------------------------++
# | Discord-Line-Message-Sync ver.   |
# | Made by LD (MIT License)         |
# ++--------------------------------++

# Bot tokens and secrets
# You will need to fill in the tokens and secrets for both your Line and Discord bots
Line:
  channel_access_token: ''
  channel_secret: ''
Discord:
  bot_token: ''

# Sync channels
# This part will need you to fill in both Line and Discord channel IDs to listen to
# And line notify token, discord channel webhook to send messages.
# These four sets of data will be used to sync messages between Line and Discord
# You can create as many sets of channels as you want to sync
Sync_channels:
  1:
    line_group_id: ''
    line_notify_token: ''
    discord_channel_id: ''
    discord_channel_webhook: ''
```

#### - How to get Line channel access token and secret

1. Go to [Line Developers](https://developers.line.biz/console/) and login with your Line account
2. If you don't have a Business ID, simply create one by following the instructions
3. Then click `Create a new provider`
4. Fill in the required information and click `Create`
5. Click `Create a new channel` and select `Messaging API`
6. Fill in the required information and click `Create`
7. You can now find your channel secret in Basic settings and channel access token in Message API, click `Issue` to copy
   it

#### - How to get Discord bot token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications) and login with your Discord account
2. Click `New Application`
3. Fill in the name of application and click `Create`
4. Click `Bot` on the left side
5. Click `Add Bot`
6. Check `Presence Intent`, `Server Members Intent` and `Message Content Intent` under `Privileged Gateway Intents`
7. Now you can find your bot token in `Build-A-Bot` section, click `Reset Token` to copy it

#### - How to get Line group ID

1. Make sure you've added your Line bot to the group
2. Run `run.bat` to start the bot (You have to fill up Bot tokens and secrets first)
3. Send `!ID` to the group chat that you want to sync
4. The bot will reply with the group ID, simply copy and paste it to `config.yml`

Notes: If you can't add your Line bot to the group, please make sure you've checked `Allow bot to join group chats`
option in your Line bot settings, which can be found in `Messaging API` > `LINE Official Account features` section.

#### - How to get Line Notify token

1. Go to [Line Notify](https://notify-bot.line.me/my/) and login with your Line account
2. Click `Generate Token`
3. Enter `Discord Message` as token name and select a chat room
4. Click `Generate`

#### - How to get Discord channel ID

1. Go to your Discord server
2. Right-click on the channel you want to sync
3. Click `Copy ID`

Notes: If you didn't see `Copy ID` in the menu, you need to enable developer mode in Discord settings, which can be
found in `Settings` > `Advanced` > `Developer Mode`

#### - How to create a Discord channel webhook

1. Go to your Discord server
2. Right-click on the channel you want to create a webhook
3. Click `Edit Channel` and find `Integrations` category
4. Click `Create Webhook`

### Setting up Line webhook

1. Go to [Line Developers](https://developers.line.biz/console/) and login with your Line account
2. Select your channel application
3. Select Messaging API, find `Webhook URL` and click edit
4. Fill in the URL of your Line bot and add `/callback` at the end
5. Click `Save` and it's pretty done!
6. Remember to check `Use webhook` under the `Webhook URL` section

Notes: Line webhook only works with HTTPS, so you need to use a reverse proxy to make it work.
If you don't know how to create a reverse proxy, you can use [ngrok](https://ngrok.com/) to create a temporary one.

### Use Ngrok to create a reverse proxy

1. Go to [Ngrok](https://ngrok.com) sign up for an account and login
2. Find your auth token in [Dashboard](https://dashboard.ngrok.com/auth) and copy it
3. Download the latest version of ngrok from [here](https://ngrok.com/download)
4. Extract the zip file and run `ngrok.exe`
5. Run `ngrok authtoken <your_auth_token>` for first time use, it will save your auth token
6. Run `ngrok http 5000` (5000 is the default port of the bot)
7. Copy the URL from `Fowarding` then check
   out [here](https://github.com/HappyGroupHub/Discord-Line-Message-Sync#Setting-up-Line-webhook)

---

## Contribute to this project

### How to contribute

1. Fork this repository
2. Clone your forked repository
3. Create a new branch
4. Make your changes
5. Commit and push your changes
6. Create a pull request
7. Wait for review

### Libraries used

* [Flask](https://github.com/pallets/flask) for webhook server
* [LineBotSDK](https://github.com/line/line-bot-sdk-python) for Line bot
* [discord.py](https://github.com/Rapptz/discord.py) for Discord bot
* [ZeroMQ](https://github.com/zeromq/pyzmq) for messaging between Line bot and Discord bot
* [PyYAML](https://github.com/yaml/pyyaml) for reading config file
* [requests](https://github.com/psf/requests) for sending HTTP requests
* [moviepy](https://github.com/Zulko/moviepy) for creating video thumbnail
* [pydub](https://github.com/jiaaro/pydub) for ffmpeg wrapper

### Code style and commits

* 100 characters per line
* Use `snake_case` for variables and functions
* Add a blank line at the end of the file
* Optimize imports, remove the redundant ones
* [Google style](https://google.github.io/styleguide/pyguide.html) TODO comments
* Use [Sphinx Docstring](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html) style for docstrings
* Use these headers for commits
    - Update - your commit messages here
    - Fix bug - your commit messages here
    - Optimize - your commit messages here
    - Standardize - your commit messages here

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

---

# Discord Line è¨æ¯åæ­¥æ©å¨äºº

ð [English README.md](#Discord-Line-Message-Sync) ð

## ä¸åå°DiscordèLineè¨æ¯åæ­¥çèå¤©æ©å¨äºº

éåæ©å¨äººå°ç¡å¯è½çåæ­¥DiscordèLineçææè¨æ¯ï¼éç¨åæ¬Line botãLine NotifyãDiscord botåDiscord webhookç­æè¡ã

imgs/gifs

ç®åæ¯æ´/ä¸æ¯æ´çè¨æ¯ç¨®é¡:

| Line -----å³éè³----> Discord | æ¯æ´  |
|:---------------------------|:---:|
| æå­è¨æ¯                       | âï¸  |
| åç                         | âï¸  |
| å½±ç                         | âï¸  |
| é³æª                         | âï¸  |
| æªæ¡                         | âï¸  |
| è²¼å                         | âï¸  |
| ä½ç½®è¨æ¯                       | âï¸  |
| ä»»ä½å¶ä»ç¨®é¡çè¨æ¯                  | âï¸  |

| Discord -----å³éè³----> Line               | æ¯æ´  |
|:-----------------------------------------|:---:|
| æå­è¨æ¯                                     | âï¸  |
| åç (jpg, jpeg, png)                      | âï¸  | 
| å½±ç (mp4)                                 | âï¸  |
| é³æª (m4a, mp3, wav, aac, flac, ogg, opus) | âï¸  |
| å¶ä»ç¨®é¡çæªæ¡                                  |  â  |
| GIFs                                     |  â  |
| è²¼å                                       |  â  |
| ä»»ä½å¶ä»ç¨®é¡çè¨æ¯                                |  â  |

You can definitely host this service yourself! and it's free!
Find it out by the following tutorial!

---

## éå§ä½¿ç¨

### å¦ä½ä¸è¼åéè¡

1. å¾ [éè£¡](https://github.com/HappyGroupHub/Discord-Line-Message-Sync/releases) ä¸è¼ææ°ççæ¬
2. è§£å£ç¸®æªæ¡å¾ï¼æ¼è³æå¤¾å§éå `config.yml`, å»ºè­°ä½¿ç¨[Notepad++](https://notepad-plus-plus.org/downloads/)ä¾ç·¨è¼¯æªæ¡
3. éµç§å§æå®æå¡«å¯« `config.yml`ï¼è«åè [éè£¡](#éæ¼ config.yml)
4. éè¡ `run.bat`
5. ç¢ºèªä½ å·²ç¶éè«Line bot/Line Notify/Discord botè³ä½ çä¼ºæå¨åèå¤©å®¤
6. ç¡æä½¿ç¨!

### éæ¼ config.yml

```yaml
# ++--------------------------------++
# | Discord-Line-Message-Sync ver.   |
# | Made by LD (MIT License)         |
# ++--------------------------------++

# Bot tokens and secrets
# You will need to fill in the tokens and secrets for both your Line and Discord bots
Line:
  channel_access_token: ''
  channel_secret: ''
Discord:
  bot_token: ''

# Sync channels
# This part will need you to fill in both Line and Discord channel IDs to listen to
# And line notify token, discord channel webhook to send messages.
# These four sets of data will be used to sync messages between Line and Discord
# You can create as many sets of channels as you want to sync
Sync_channels:
  1:
    line_group_id: ''
    line_notify_token: ''
    discord_channel_id: ''
    discord_channel_webhook: ''
```

#### - ç²å Line channel access token å secret

1. åå¾ [Line Developers](https://developers.line.biz/console/) ä¸¦ä½¿ç¨ä½ çLineå¸³èç»å¥
2. å¦æä½ æ²æBusiness IDï¼è«æç§å®ç¶²çæç¤ºå»ºç«ä¸å
3. é»æ `Create a new provider`
4. å¡«å¯«å®éè¦çè³æå¾é»æ `Create`
5. é»æ `Create a new channel` ä¸¦é¸æ `Messaging API` çåé¡
6. å¡«å¯«å®éè¦çè³æå¾é»æ `Create`
7. ç¾å¨ä½ å¯ä»¥å¨ Basic settings æ¾å°ä½ ç `channel secret` ä»¥åå¨ Message API æ¾å° `channel access token`ï¼é»æ `Issue` ä¾è¤è£½

#### - ç²å Discord bot token

1. åå¾ [Discord Developer Portal](https://discord.com/developers/applications) ä¸¦ä½¿ç¨ä½ çDiscordå¸³èç»å¥
2. é»æ `New Application`
3. å¹«æ­¤æ©å¨äººååçº `Lineè¨æ¯` å¾é»æ `Create`
4. é»æå·¦å´åè¡¨ç `Bot`
5. é»æ `Add Bot`
6. å¨ `Privileged Gateway Intents` åºä¸å° `Presence Intent`, `Server Members Intent` å `Message Content Intent` é½æå¾
7. ç¾å¨ä½ å¯ä»¥å¨ `Build-A-Bot` åºä¸æ¾å°ä½ ç bot tokenï¼é»æ `Reset Token` ä¾è¤è£½

#### - ç²å Line group ID

1. ç¢ºèªä½ å·²ç¶å°ä½ çLine botå å¥å°ä½ æ³è¦åæ­¥çç¾¤çµ
2. éè¡ `run.bat` ä¾ååæ©å¨äºº (ä½ å¿é åå¡«å¯«æ©å¨äººçtokenåsecret)
3. å¨ä½ æ³è¦åæ­¥çç¾¤çµå§å³é `!ID`
4. æ©å¨äººæåè¦ç¾¤çµçIDï¼è«å°å®è¤è£½ä¸¦è²¼å° `config.yml` ä¸­

æ³¨æ: å¦æä½ ç¡æ³å°ä½ çLine botå å¥ç¾¤çµï¼è«ç¢ºèªä½ å·²ç¶å¨ `Messaging API` > `LINE Official Account features`
åºä¸å¾é¸ `Allow bot to join group chats` éåé¸é 

#### - ç²å Line Notify token

1. åå¾ [Line Notify](https://notify-bot.line.me/my/) ä¸¦ä½¿ç¨ä½ çLineå¸³èç»å¥
2. é»æ `ç¼è¡æ¬æ`
3. æ¬æåç¨±è¼¸å¥ `Discordè¨æ¯` ä¸¦é¸æä½ æ³åæ­¥çèå¤©å®¤
4. é»æ `ç¼è¡`

#### - ç²å Discordé »é ID

1. åå¾ä½ çDiscordä¼ºæå¨
2. å³éµé»æä½ æ³è¦åæ­¥çæå­é »é
3. é»æ `è¤è£½ID`

æ³¨æ: å¦æä½ æ²æçå° `è¤è£½ID` éåé¸é ï¼è«åå¨Discordçè¨­å®ä¸­åç¨éç¼èæ¨¡å¼ï¼ä½ å¯ä»¥å¨ `è¨­å®` > `é²é` > `éç¼èæ¨¡å¼` ä¸­æ¾å°

#### - å»ºç«ä¸å Discord channel webhook

1. åé²å¥ä½ çDiscordä¼ºæå¨
2. å³éµé»æä½ æ³è¦å»ºç« Webhook çæå­é »é
3. é¸æ `ç·¨è¼¯é »é` ä¸¦å¨è£¡é¢æ¾å° `æ´å` çåé¡
4. é»æ `å»ºç« Webhook`

### è¨­å®Line Webhook

1. åå¾ [Line Developers](https://developers.line.biz/console/) ä¸¦ä½¿ç¨ä½ çLineå¸³èç»å¥
2. é»æä½ è¦ä½¿ç¨ç `channel application`
3. é¸æ Messaging API åé¡, æ¾å° `Webhook URL` ä¸¦é»æ `edit`
4. è²¼ä¸ä½ æ¶è¨­Lineæ©å¨äººçURLä¸¦å¨å°¾èå ä¸ `/callback`
5. é»æ `Save`
6. å¨ `Webhook URL` åºä¸å¾é¸ `Use webhook`

æ³¨æ! Line Webhookåé©ç¨æ¼ `HTTPS` åè­°ï¼æä¸æ¥åä»»ä½æªç¶èªè­éçç¶²å
å¦æä½ ä¸ç¥éå¦ä½ç³è«ï¼å¯ä»¥ä½¿ç¨[ngrok](https://ngrok.com/)åµå»ºä¸åç°¡å®çå°åæå

### ä½¿ç¨Ngrokä»¥ç¬¦åHTTPSåè­°

1. åå¾ [Ngrok](https://ngrok.com) è¨»åä¸åå¸³èä¸¦ç»å¥
2. åå¾ [Dashboard](https://dashboard.ngrok.com/auth) ä¸¦è¤è£½ä½ ç `authtoken`
3. å¾ [éè£¡](https://ngrok.com/download) ä¸è¼ææ°çæ¬çä¸»ç¨å¼
4. è§£å£ç¸®æªæ¡ä¸¦éè¡ `ngrok.exe`
5. å·è¡ `ngrok authtoken <your_auth_token>` ä¾åæ¬¡åç¨æåï¼å®æèªåå²å­ä½ çèªè­ç¢¼
6. å·è¡ `ngrok http 5000` (5000å æ¯é è¨­çéé)
7. è¤è£½ `Fowarding` æçæçURLä¸¦æ¥ç [éè£¡](#è¨­å®Line-Webhook)

---

## åå©éåå°æ¡éç¼

### å¦ä½è²¢ç»

1. Fork éåå°æ¡
2. è¤è£½ä½ åå Fork çå°æ¡è³æ¬å°
3. å»ºç«æ°çåæ¯
4. ç¡æç¼æ®ä½ çè½å
5. Commit / Push ä½ çç¨å¼ç¢¼
6. å»ºç«æ°ç Pull Request
7. ç­å¾åè¦

### ä½¿ç¨çå½å¼åº«

* [Flask](https://github.com/pallets/flask) ç¨ä¾æ¶è¨­Webhookä¼ºæå¨
* [LineBotSDK](https://github.com/line/line-bot-sdk-python) ç¨ä¾èLine APIæºé
* [discord.py](https://github.com/Rapptz/discord.py) ç¨ä¾èDiscord APIæºé
* [ZeroMQ](https://github.com/zeromq/pyzmq) ç¨ä¾å¨å©åç¨å¼ä¹éé²è¡æºé
* [PyYAML](https://github.com/yaml/pyyaml) ç¨ä¾è®åconfig.ymlæªæ¡
* [requests](https://github.com/psf/requests) ç¨ä¾å³éHTTPè«æ±
* [moviepy](https://github.com/Zulko/moviepy) ç¨ä¾è£½ä½å½±ççç¸®å
* [pydub](https://github.com/jiaaro/pydub) ç¨ä¾ä½¿ç¨ffmpegèçå½±é³æªæ¡

### Code style and commits

* 100 characters per line
* Use `snake_case` for variables and functions
* Add a blank line at the end of the file
* Optimize imports, remove the redundant ones
* [Google style](https://google.github.io/styleguide/pyguide.html) TODO comments
* Use [Sphinx Docstring](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html) style for docstrings
* Use these headers for commits
    - Update - your commit messages here
    - Fix bug - your commit messages here
    - Optimize - your commit messages here
    - Standardize - your commit messages here

### çæ¬

æ­¤å°æ¡ççæ¬è¦ç¯æ¡ç¨ **MIT License** - è³ [LICENSE](LICENSE) æ¥çæ´å¤ç¸éè²æ
