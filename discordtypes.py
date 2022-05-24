# Assembled from https://discord.com/developers/docs/interactions/slash-commands on 2021-04-05
from enum import Enum
from pydantic import BaseModel, Field

from typing import Any, List, Optional


class ApplicationCommandOptionType(Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8


class InteractionType(Enum):
    PING = 1
    APPLICATIONCOMMAND = 2


class InteractionResponseType(Enum):
    PONG = 1
    ACKNOWLEDGE = 2
    CHANNELMESSAGE = 3
    CHANNELMESSAGEWITHSOURCE = 4
    DEFERREDCHANNELMESSAGEWITHSOURCE = 5


class AllowedMentionType(Enum):
    ROLE = "roles"
    USER = "users"
    EVERYONE = "everyone"


class NitroType(Enum):
    NONE = 0
    CLASSIC = 1
    NITRO = 2


class UserFlags(Enum):
    NONE = 0
    EMPLOYEE = 1 << 0
    PARTNERED = 1 << 1
    HYPESQUAD_EVENTS = 1 << 2
    BUGHUNTER_LEVEL1 = 1 << 3
    HOUSE_BRAVERY = 1 << 6
    HOUSE_BRILLIANCE = 1 << 7
    HOUSE_BALANCE = 1 << 8
    EARLY_SUPPORTER = 1 << 9
    TEAM_USER = 1 << 10
    SYSTEM = 1 << 12
    BUGHUTNER_LEVEL2 = 1 << 14
    VERIFIED_BOT = 1 << 16
    EARLY_VERIFIED_BOT_DEVELOPER = 1 << 17


class Snowflake(int):
    # TODO: Should a lso implement a created_at per Twitter Snowflake implementations
    pass


class EmbedFooter(BaseModel):
    text: str
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


class EmbedImage(BaseModel):
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedThumbnail(BaseModel):
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedVideo(BaseModel):
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedProvider(BaseModel):
    name: Optional[str]
    url: Optional[str]


class EmbedAuthor(BaseModel):
    name: Optional[str]
    url: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


class EmbedField(BaseModel):
    name: str
    value: str
    inline: Optional[bool]


class EmbedObject(BaseModel):
    title: Optional[str]
    type: str = "rich"
    description: Optional[str]
    url: Optional[str]
    timestamp: Optional[str]  # TODO: Make this a real ISO8601 timestamp type
    color: Optional[int]
    footer: Optional[EmbedFooter]
    image: Optional[EmbedImage]
    thumbnail: Optional[EmbedThumbnail]
    video: Optional[EmbedVideo]
    provider: Optional[EmbedProvider]
    author: Optional[EmbedAuthor]
    fields_: Optional[List[EmbedField]]

    class Config:
        fields = {"fields_": "fields"}


class AllowedMentions(BaseModel):
    parse: List[AllowedMentionType]
    roles: List[Snowflake]
    users: List[Snowflake]
    replied_user: bool = False


class InteractionApplicationCommandCallbackDataFlags(Enum):
    EPHEMERAL = 64


# Alias
class CommandCallbackDataFlags(Enum):
    EPHEMERAL = 64


class InteractionApplicationCommandCallbackData(BaseModel):
    tts: Optional[bool] = False
    content: Optional[str] = None
    embeds: Optional[List[EmbedObject]]
    allowed_mentions: Optional[AllowedMentions]
    flags: Optional[int]  # Set to 64 for user-only message


# Alias
class CommandCallbackData(InteractionApplicationCommandCallbackData):
    pass


class InteractionResponse(BaseModel):
    type: Optional[InteractionType] = InteractionResponseType.CHANNELMESSAGEWITHSOURCE
    data: Optional[InteractionApplicationCommandCallbackData]


class User(BaseModel):
    id: Snowflake
    username: str
    discriminator: str
    avatar: str
    bot: Optional[bool]
    system: Optional[bool]
    mfa_enabled: Optional[bool]
    locale: Optional[str]
    verified: Optional[bool]
    email: Optional[str]
    flags: Optional[int]
    premium_type: Optional[NitroType]
    public_flags: Optional[int]


class GuildMember(BaseModel):
    user: Optional[User]
    nick: Optional[str]
    roles: List[Snowflake]
    joined_at: str  # TODO: This is ISO8601 timestamp
    premium_since: Optional[str]  # TODO: This is ISO8601 timestamp
    deaf: bool
    mute: bool
    pending: Optional[bool]
    permissions: Optional[str]


class ApplicationCommandInteractionDataOptionNested(BaseModel):
    name: str
    value: Optional[ApplicationCommandOptionType]
    type: ApplicationCommandOptionType
    options: Optional[
        List[Any]
    ]  # This is a circular reference to ApplicationCommandInteractionDataOption


class ApplicationCommandInteractionDataOption(BaseModel):
    name: str
    value: Any
    type: ApplicationCommandOptionType
    options: Optional[List[ApplicationCommandInteractionDataOptionNested]]


class ApplicationCommandInteractionData(BaseModel):
    id: Snowflake
    name: str
    options: Optional[List[ApplicationCommandInteractionDataOption]]


class Interaction(BaseModel):
    id: Snowflake
    application_id: Snowflake
    type: InteractionType
    data: Optional[ApplicationCommandInteractionData]
    guild_id: Optional[Snowflake]
    channel_id: Optional[Snowflake]
    member: Optional[GuildMember]
    user: Optional[User]
    token: str
    version: int = 1


class ApplicationCommandOptionChoice(BaseModel):
    name: str
    value: Any


class ApplicationCommandOptionNested(BaseModel):
    type: ApplicationCommandOptionType
    name: str
    description: str
    required: Optional[bool]
    choices: Optional[List[ApplicationCommandOptionChoice]]
    options: Optional[
        List[Any]
    ]  # This is a circular reference to ApplicationCommandOption


class ApplicationCommandOption(BaseModel):
    type: ApplicationCommandOptionType
    name: str
    description: str
    required: Optional[bool]
    choices: Optional[List[ApplicationCommandOptionChoice]]
    options: Optional[List[ApplicationCommandOptionNested]]


class ApplicationCommand(BaseModel):
    id: Optional[Snowflake]
    application_id: Snowflake
    name: str
    description: str
    options: Optional[List[ApplicationCommandOption]]


class ClientCredentialsAccessTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
