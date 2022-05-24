import requests
import os
from discordtypes import (
    ApplicationCommand,
    ClientCredentialsAccessTokenResponse,
    ApplicationCommandOptionType,
)

GUILD_ID = os.getenv('GUILD_ID')
APP_ID = os.getenv('APP_ID')
TOKEN_ENDPOINT = "https://discord.com/api/v8/oauth2/token"
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

data = {"grant_type": "client_credentials", "scope": "applications.commands.update"}

r = requests.post(TOKEN_ENDPOINT, data=data, auth=(APP_ID, CLIENT_SECRET))

r.raise_for_status()

creds = ClientCredentialsAccessTokenResponse(**r.json())

command = ApplicationCommand(
    application_id=APP_ID, name="hello", description="Say hello", options=[]
)

commands_url = (
    f"https://discord.com/api/v8/applications/{APP_ID}/guilds/{GUILD_ID}/commands"
)

headers = {
    "Content-type": "application/json",
    "Authorization": f"Bearer {creds.access_token}",
}

json = command.json()
r = requests.post(commands_url, headers=headers, data=json)
r.raise_for_status()
registered_command = ApplicationCommand(**r.json())

command = ApplicationCommand(
    application_id=APP_ID,
    name="snowflaketime",
    description="Convert snowflake to timestamp",
    options=[
        {
            "name": "snowflake",
            "description": "Discord snowflake",
            "type": ApplicationCommandOptionType.INTEGER,
            "required": True,
        }
    ],
)

json = command.json()
r = requests.post(commands_url, headers=headers, data=json)
r.raise_for_status()
registered_command = ApplicationCommand(**r.json())
