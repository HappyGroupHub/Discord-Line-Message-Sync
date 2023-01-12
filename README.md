# Discord Line Message Sync

## A bot that syncs messages between Discord and Line

📖 [繁體中文版README.md](#Discord-Line-訊息同步機器人) 📖

---

## Getting started to use the bot

### How to use

1. Download the latest release from [here](https://github.com/HappyGroupHub/Discord-Line-Message-Sync/releases)
2. Run `discord_bot.py` or `line_bot.py` in order to generate the config files
3. Fill in the required information in `config.yml`
4. Now run `discord_bot.py` and `line_bot.py` both
5. Finish setting up Line webhook service
6. Enjoy!

### About config.yml

```yaml
Line:
  channel_access_token: ''
  channel_secret: ''
  line_notify_token: ''

  # 以下為聊天室綁定設定:
  # 聊天室屬性, 目前只有私人訊息以及群組訊息兩種 (user, group)
  chat_type: ''

  # 私人訊息: 請在user_id填入你的line_user_id
  # 群組訊息: 請在group_id填入你的群組id
  # 依照上面聊天室屬性對應填入一個即可
  user_id: ''
  group_id: ''

Discord:
  bot_token: ''
  channel_id: ''
  channel_webhook: ''
```

#### - How to get Line channel access token and secret

1. Go to [Line Developers](https://developers.line.biz/console/) and login with your Line account
2. Click `Create a new provider`
3. Fill in the required information and click `Create`
4. Click `Create a new channel` and select `Messaging API`
5. Fill in the required information and click `Create`
6. You can now find your channel secret in Basic settings and channel access token in Message API

#### - How to get Line Notify token

1. Go to [Line Notify](https://notify-bot.line.me/my/) and login with your Line account
2. Click `Generate Token`
3. Enter `Discord Message` as token name and select a chat room
4. Click `Generate`

#### - How to get Discord bot token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications) and login with your Discord account
2. Click `New Application`
3. Fill in the name of application and click `Create`
4. Click `Bot` on the left side
5. Click `Add Bot`
6. Click `Copy` under `Token`

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
5. Click `Save` and you are done!

Note that Line webhook only works with HTTPS, so you need to use a reverse proxy to make it work.
If you don't know how to create a reverse proxy, you can use [ngrok](https://ngrok.com/) to create a temporary one.

### Use Ngrok to create a reverse proxy

1. Go to [Ngrok](https://ngrok.com) sign up for an account and login
2. Find your auth token in [Dashboard](https://dashboard.ngrok.com/auth) and copy it
3. Download the latest version of ngrok from [here](https://ngrok.com/download)
4. Extract the zip file and run `ngrok.exe` 
5. Run `ngrok authtoken <your_auth_token>` for first time use, it will save your auth token
6. Run `ngrok http 5000` (5000 is the default port of the bot)
7. Copy the URL from `Fowarding` then check out [here](https://github.com/HappyGroupHub/Discord-Line-Message-Sync#Setting-up-Line-webhook)

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

# Discord Line 訊息同步機器人

## 一個將Discord與Line訊息同步的聊天機器人

📖 [English README.md](#Discord-Line-Message-Sync) 📖

---

## 開始使用

### 如何下載及運行

1. 從 [這裡](https://github.com/HappyGroupHub/Discord-Line-Message-Sync/releases) 下載最新的版本
2. 運行 `discord_bot.py` 或 `line_bot.py` 讓系統首次生成檔案
3. 完成填寫 `config.yml`
4. 同時運行 `discord_bot.py` 以及 `line_bot.py` 
5. 完成 Line webhook 的設定
6. 盡情使用!

### 關於 config.yml

```yaml
Line:
  channel_access_token: ''
  channel_secret: ''
  line_notify_token: ''

  # 以下為聊天室綁定設定:
  # 聊天室屬性, 目前只有私人訊息以及群組訊息兩種 (user, group)
  chat_type: ''

  # 私人訊息: 請在user_id填入你的line_user_id
  # 群組訊息: 請在group_id填入你的群組id
  # 依照上面聊天室屬性對應填入一個即可
  user_id: ''
  group_id: ''

Discord:
  bot_token: ''
  channel_id: ''
  channel_webhook: ''
```

#### - 獲取 Line channel access token 及 secret

1. 前往 [Line Developers](https://developers.line.biz/console/) 並使用你的Line帳號登入
2. 點擊 `Create a new provider`
3. 填寫完官網需要的資料後點擊 `Create`
4. 點擊 `Create a new channel` 並選擇 `Messaging API` 的分類
5. 填寫完需要的資料後點擊 `Create`
6. 現在你可以在 Basic settings 找到你的 `channel secret` 以及在 Message API 找到 `channel access token`

#### - 獲取 Line Notify token

1. 前往 [Line Notify](https://notify-bot.line.me/my/) 並使用你的Line帳號登入
2. 點擊 `發行權杖`
3. 權杖名稱輸入 `Discord訊息` 並選擇你想同步的聊天室
4. 點擊 `發行`

#### - 獲取 Discord bot token

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications) 並使用你的Discord帳號登入
2. 點擊 `New Application`
3. 幫此機器人取名為 `Line訊息` 後點擊 `Create`
4. 點擊左側列表的 `Bot`
5. 點擊 `Add Bot`
6. 點擊 `Token` 底下的 `Copy` 來複製金鑰

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
5. 點擊 `Save` 就完成囉!

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

### 版權

此專案的版權規範採用 **MIT License** - 至 [LICENSE](LICENSE) 查看更多相關聲明
