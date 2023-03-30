# Discord Line Message Sync

📖 [繁體中文版README.md](#Discord-Line-訊息同步機器人) 📖

## A bot that syncs messages between Discord and Line

![Banner](./readme_imgs/banner.jpg)
This bot is made to sync all kinds of messages between Discord and Line, using four applications including Line bot,
Line Notify, Discord bot and Discord webhook.

![Demo](./readme_imgs/demo.gif)

Supported messages sync types:

| Line -----to----> Discord   | Support |
|:----------------------------|:-------:|
| Text Message                |   ☑️    |
| Pictures                    |   ☑️    |
| Videos                      |   ☑️    |
| Audios                      |   ☑️    |
| Files                       |   ❌️    |
| Sticker                     |   ❌️    |
| Location                    |   ❌️    |
| Any other types of messages |   ❌️    |

| Discord -----to----> Line                    | Support |
|:---------------------------------------------|:-------:|
| Text Message                                 |   ☑️    |
| Pictures (jpg, jpeg, png)                    |   ☑️    | 
| Videos (mp4)                                 |   ☑️    |
| Audios (m4a, mp3, wav, aac, flac, ogg, opus) |   ☑️    |
| Other formats files                          |    ❌    |
| GIFs                                         |    ❌    |
| Sticker                                      |    ❌    |
| Any other types of messages                  |    ❌    |

You can definitely host this service yourself! and it's free!
Find it out by the following tutorial!

---

## Getting started to use the bot

### How to use

1. Download the latest release from [here](https://github.com/HappyGroupHub/Discord-Line-Message-Sync/releases)
2. Unzip the file then open up `config.yml`, [Notepad++](https://notepad-plus-plus.org/downloads/) is recommended
3. Fill in the following required information, see [here](#About-configyml) for more details
4. Now run `run.bat` to start the bot
5. Make sure you've invited the bot to your Discord server and added it / Line Notify to your Line group
6. Enjoy!

### Dependencies

- [ffmpeg](https://ffmpeg.org/download.html) - You need to install ffmpeg and add it to your PATH environment variable
  to use this bot

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

### Find bugs or having suggestions?

If you have any suggestions or found any bugs, please open an
issue [here](https://github.com/HappyGroupHub/Discord-Line-Message-Sync/issues), will try to fix it as soon as possible.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

---

# Discord Line 訊息同步機器人

📖 [English README.md](#Discord-Line-Message-Sync) 📖

## 一個將Discord與Line訊息同步的聊天機器人

![Banner](./readme_imgs/banner.jpg)
這個機器人將盡可能的同步Discord與Line的所有訊息，運用包括Line bot、Line Notify、Discord bot及Discord webhook等技術。

![Demo](./readme_imgs/demo.gif)

目前支援同步的訊息種類:

| Line -----傳送至----> Discord | 支援  |
|:---------------------------|:---:|
| 文字訊息                       | ☑️  |
| 圖片                         | ☑️  |
| 影片                         | ☑️  |
| 音檔                         | ☑️  |
| 檔案                         | ❌️  |
| 貼圖                         | ❌️  |
| 位置訊息                       | ❌️  |
| 任何其他種類的訊息                  | ❌️  |

| Discord -----傳送至----> Line               | 支援  |
|:-----------------------------------------|:---:|
| 文字訊息                                     | ☑️  |
| 圖片 (jpg, jpeg, png)                      | ☑️  | 
| 影片 (mp4)                                 | ☑️  |
| 音檔 (m4a, mp3, wav, aac, flac, ogg, opus) | ☑️  |
| 其他種類的檔案                                  |  ❌  |
| GIFs                                     |  ❌  |
| 貼圖                                       |  ❌  |
| 任何其他種類的訊息                                |  ❌  |

想要自己架設這個訊息同步機器人嗎?
快點看看下面的使用教學吧!

---

## 開始使用

### 如何下載及運行

1. 從 [這裡](https://github.com/HappyGroupHub/Discord-Line-Message-Sync/releases) 下載最新的版本
2. 解壓縮檔案後，於資料夾內開啟 `config.yml`, 建議使用[Notepad++](https://notepad-plus-plus.org/downloads/)來編輯檔案
3. 遵照內文完成填寫 `config.yml`，請參考 [這裡](#關於-configyml)
4. 運行 `run.bat`
5. 確認你已經邀請Line bot/Line Notify/Discord bot至你的伺服器及聊天室
6. 盡情使用!

### 系統需求

* [ffmpeg](https://ffmpeg.org/download.html) - 你必須安裝ffmpeg，並將其路徑加入環境變數才可使用此機器人

### 關於 config.yml

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

#### - 獲取 Line channel access token 及 secret

1. 前往 [Line Developers](https://developers.line.biz/console/) 並使用你的Line帳號登入
2. 如果你沒有Business ID，請按照官網的指示建立一個
3. 點擊 `Create a new provider`
4. 填寫完需要的資料後點擊 `Create`
5. 點擊 `Create a new channel` 並選擇 `Messaging API` 的分類
6. 填寫完需要的資料後點擊 `Create`
7. 現在你可以在 Basic settings 找到你的 `channel secret` 以及在 Message API 找到 `channel access token`，點擊 `Issue` 來複製

#### - 獲取 Discord bot token

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications) 並使用你的Discord帳號登入
2. 點擊 `New Application`
3. 幫此機器人取名為 `Line訊息` 後點擊 `Create`
4. 點擊左側列表的 `Bot`
5. 點擊 `Add Bot`
6. 在 `Privileged Gateway Intents` 底下將 `Presence Intent`, `Server Members Intent` 及 `Message Content Intent` 都打勾
7. 現在你可以在 `Build-A-Bot` 底下找到你的 bot token，點擊 `Reset Token` 來複製

#### - 獲取 Line group ID

1. 確認你已經將你的Line bot加入到你想要同步的群組
2. 運行 `run.bat` 來啟動機器人 (你必須先填寫機器人的token及secret)
3. 在你想要同步的群組內傳送 `!ID`
4. 機器人會回覆群組的ID，請將它複製並貼到 `config.yml` 中

注意: 如果你無法將你的Line bot加入群組，請確認你已經在 `Messaging API` > `LINE Official Account features`
底下勾選 `Allow bot to join group chats` 這個選項

#### - 獲取 Line Notify token

1. 前往 [Line Notify](https://notify-bot.line.me/my/) 並使用你的Line帳號登入
2. 點擊 `發行權杖`
3. 權杖名稱輸入 `Discord訊息` 並選擇你想同步的聊天室
4. 點擊 `發行`

#### - 獲取 Discord頻道 ID

1. 前往你的Discord伺服器
2. 右鍵點擊你想要同步的文字頻道
3. 點擊 `複製ID`

注意: 如果你沒有看到 `複製ID` 這個選項，請先在Discord的設定中啟用開發者模式，你可以在 `設定` > `進階` > `開發者模式` 中找到

#### - 建立一個 Discord channel webhook

1. 先進入你的Discord伺服器
2. 右鍵點擊你想要建立 Webhook 的文字頻道
3. 選擇 `編輯頻道` 並在裡面找到 `整合` 的分類
4. 點擊 `建立 Webhook`

### 設定Line Webhook

1. 前往 [Line Developers](https://developers.line.biz/console/) 並使用你的Line帳號登入
2. 點擊你要使用的 `channel application`
3. 選擇 Messaging API 分類, 找到 `Webhook URL` 並點擊 `edit`
4. 貼上你架設Line機器人的URL並在尾處加上 `/callback`
5. 點擊 `Save`
6. 在 `Webhook URL` 底下勾選 `Use webhook`

注意! Line Webhook僅適用於 `HTTPS` 協議，恕不接受任何未經認證過的網址
如果你不知道如何申請，可以使用[ngrok](https://ngrok.com/)創建一個簡單的導向服務

### 使用Ngrok以符合HTTPS協議

1. 前往 [Ngrok](https://ngrok.com) 註冊一個帳號並登入
2. 前往 [Dashboard](https://dashboard.ngrok.com/auth) 並複製你的 `authtoken`
3. 從 [這裡](https://ngrok.com/download) 下載最新版本的主程式
4. 解壓縮檔案並運行 `ngrok.exe`
5. 執行 `ngrok authtoken <your_auth_token>` 來初次啟用服務，它會自動儲存你的認證碼
6. 執行 `ngrok http 5000` (5000埠是預設的閘道)
7. 複製 `Fowarding` 所生成的URL並查看 [這裡](#設定Line-Webhook)

---

## 協助這個專案開發

### 如何貢獻

1. Fork 這個專案
2. 複製你剛剛 Fork 的專案至本地
3. 建立新的分支
4. 盡情發揮你的能力
5. Commit / Push 你的程式碼
6. 建立新的 Pull Request
7. 等待回覆

### 使用的函式庫

* [Flask](https://github.com/pallets/flask) 用來架設Webhook伺服器
* [LineBotSDK](https://github.com/line/line-bot-sdk-python) 用來與Line API溝通
* [discord.py](https://github.com/Rapptz/discord.py) 用來與Discord API溝通
* [ZeroMQ](https://github.com/zeromq/pyzmq) 用來在兩個程式之間進行溝通
* [PyYAML](https://github.com/yaml/pyyaml) 用來讀取config.yml檔案
* [requests](https://github.com/psf/requests) 用來傳送HTTP請求
* [moviepy](https://github.com/Zulko/moviepy) 用來製作影片的縮圖
* [pydub](https://github.com/jiaaro/pydub) 用來使用ffmpeg處理影音檔案

### 程式碼撰寫/提交規範

* 每行不超過100個字元
* 使用 `snake_case` 命名變數及函式
* 在檔案尾處加上一個空行
* 最佳化程式碼並移除不必要的import
* [Google style](https://google.github.io/styleguide/pyguide.html) TODO註解
* 使用 [Sphinx Docstring](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html) 進行函式註解
* 提交請求時請使用以下格式，並全英文撰寫
    - Update - your commit messages here
    - Fix bug - your commit messages here
    - Optimize - your commit messages here
    - Standardize - your commit messages here

### 建議/問題回報

如果你有任何建議或是發現了任何問題，請在 [Issues](https://github.com/HappyGroupHub/Ethereum-Wallet-Tracker/issues)
提交你的意見，我會盡快回覆你!

### 版權

此專案的版權規範採用 **MIT License** - 至 [LICENSE](LICENSE) 查看更多相關聲明
