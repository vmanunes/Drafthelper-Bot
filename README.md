# Drafthelper-Bot

Discord bot focused on quality of life tools for drafting tournaments on smogon discord server and bracketmaker tools for a swiss tournament integrated with google sheets.

---

#### Tools:

- Python
- Google Spreadsheet API
- discord.py wrapper

#### Requirements:

Create a .env file with a variable "token", receiving the discord bot token generated in [Discord Developer Portal](https://discord.com/developers/applications).

###### _For more information, refer to [.env documentation](https://pypi.org/project/python-dotenv/)_

Generate google credentials on the google cloud console with sheets api enabled.

###### _For more information, refer to [google api documentation](https://cloud.google.com/apis/docs/overview)_
---

#### Auto setup:

Execute the bot script on the project root folder with:

`./bot.sh`

---

#### Manual setup:

On a terminal, generate a python environment with the following command:

`python -m venv env`

This will generate a environment called "env" (this is an arbitrary name, it can be changed in the previous command).

Navigate to the Scripts folder inside the environment:

`cd env\Scripts`

Activate the environment executing the script based on your current system:

![env scripts](https://i.imgur.com/EHnC2cd.png)

I.e.: To activate the environment in powershell:

`./Activate.ps1`

Lastly, head back to the root of the project with:

`cd ../..`

#### Executing:

Install all required packages in the environment with:

`pip install -r requirements.txt`

And run the bot with:

`python bot.py`
