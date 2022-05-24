from fastapi import FastAPI, status, HTTPException, Header, Request, Depends
from typing import Optional
from cryptography.exceptions import InvalidSignature
import logging
import os

from discordtypes import (
    Interaction,
    InteractionType,
    InteractionResponse,
    InteractionResponseType,
    CommandCallbackData,
    CommandCallbackDataFlags,
    ApplicationCommandOptionType,
    ApplicationCommandInteractionDataOption,
)
from slash import Slash

PUBLIC_KEY = os.getenv("PUBLIC_KEY")
app = FastAPI()
slash = Slash()


async def signed_request(
    request: Request,
    x_signature_ed25519: str = Header(...),
    x_signature_timestamp: str = Header(...),
):

    body = await request.body()

    try:
        await sigverify(PUBLIC_KEY, x_signature_ed25519, x_signature_timestamp, body)
    except Exception as e:
        logger = logging.getLogger("uvicorn.error")
        logger.error(f"Signature failure exception: {e.__repr__()}")
        raise HTTPException(status_code=401, detail="Invalid signature")

    return True


async def sigverify(public_key: str, signature: str, timestamp: str, body: str):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

    verify_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key))
    verify_key.verify(bytes.fromhex(signature), timestamp.encode() + body)


@app.get("/health_check")
async def health_check():
    return {"status": "ok"}


@slash.command("hello", description="Hello world")
def command_hello(interaction):
    return {
        "content": "Hello",
        "type": InteractionResponseType.CHANNELMESSAGEWITHSOURCE,
        "flags": CommandCallbackDataFlags.EPHEMERAL,
    }


@slash.command(
    "snowflaketime",
    description="Convert timestamp from snowflake",
    options=[
        {
            "name": "snowflake",
            "description": "Discord snowflake",
            "type": ApplicationCommandOptionType.INTEGER,
            "required": True,
        }
    ],
)
def command_snowflaketime(interaction):
    import datetime

    snowflake = None

    # Can we move this to kwarg?
    for option in interaction.data.options:
        if option.name == "snowflake":
            snowflake = int(option.value)

    # From discord.py utils
    DISCORD_EPOCH = 1420070400000
    ts = ((snowflake >> 22) + DISCORD_EPOCH) / 1000
    sfdt = datetime.datetime.utcfromtimestamp(ts).replace(tzinfo=datetime.timezone.utc)
    # End discord.py utils

    snowflaketime = sfdt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    fsnowflaketime = sfdt.strftime("%Y-%m-%d %I:%M:%S%p %Z")
    return {
        "content": f"{snowflaketime}\n**{fsnowflaketime}**",
        "type": InteractionResponseType.CHANNELMESSAGEWITHSOURCE,
    }


@app.post("/interaction")
async def interaction(
    interaction: Interaction, verified: bool = Depends(signed_request)
):
    logger = logging.getLogger("uvicorn.access")
    logger.info(interaction)

    if interaction.type == InteractionType.PING:
        return InteractionResponse(type=InteractionResponseType.PONG)

    if interaction.type == InteractionType.APPLICATIONCOMMAND:
        cmd = interaction.data.name
        if cmd in slash.commands.keys():
            return slash.commands[cmd]["function"](interaction)

    raise HTTPException(status_code=501, detail="Not implemented")
