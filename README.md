# Introduction

This was originally created back in 2021 [when the feature was announced](https://discord.com/blog/slash-commands-are-here).

Discord implemented [Slash Commands](https://discord.com/developers/docs/interactions/application-commands) as a way for users to interact with external services.
Slash commands are implemented by creating a web server that receives a webhook from Discord when a user uses the appropriate slash command.

To prevent abuse of the webservice, the slash commands are protected by a public key ed25519 signature. The web service must implement verification of the signature (discord will actually send invalid signatures to verify the service is checking) and all requests must be appropriately signed.

This is very similar to [Slack Slash Commands](https://api.slack.com/interactivity/slash-commands). The structure is slightly different and the public key infrastructure is also different.


## Discord Types
The discord types used here are for strong typing. They were translated from various Discord API pages.


## Deployment
This service is deployed as a [Google Cloud Run](https://cloud.google.com/run) service. The dockerfile describes the build. Python's cryptography library requires rust for some implementations and the container is built appropriately with rust.

The container is registered with gcloud run. Interactoins are registered via the `register_command.py` tool.


## Commands Implemented
The only interaction implemented is a service to translate Discord's _snowflake_ into an appropriate timestamp. Discord snowflakes are used to quickly ID resources across discord. Twitter originally developed their Snowflake service to replace the concept of UUIDs - snowflakes are sortable and unique.

## Tests
The only tests are for verifying the cryptography library.