# Discord Line Message Sync

## A bot that syncs messages between Discord and Line

📖 [繁體中文版README.md]() 📖

---

## Getting started to use the bot

### How to use

1. Download the latest release from [here]()
2. Extract the zip file
3. Run `discord_bot.py` or `line_bot.py` in order to generate the config files
4. Fill in the required information in `config.yml`
5. Now run `discord_bot.py` and `line_bot.py` both
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

#### How to get Line channel access token and secret

1. Go to [Line Developers](https://developers.line.biz/console/) and login with your Line account
2. Click `Create a new provider`
3. Fill in the required information and click `Create`
4. Click `Create a new channel` and select `Messaging API`
5. Fill in the required information and click `Create`
6. You can now find your channel secret in Basic settings and channel access token in Message API

#### How to get Line Notify token

1. Go to [Line Notify](https://notify-bot.line.me/my/)
2. Click `Generate Token`
3. Enter `Discord Message` as token name and select a chat room
4. Click `Generate`

#### How to get Discord bot token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click `New Application`
3. Fill in the name of application and click `Create`
4. Click `Bot` on the left side
5. Click `Add Bot`
6. Click `Copy` under `Token`

#### How to create a Discord channel webhook

1. Go to your Discord server
2. Right-click on the channel you want to create a webhook
3. Click `Edit Channel` and find `Integrations` category
4. Click `Create Webhook`

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