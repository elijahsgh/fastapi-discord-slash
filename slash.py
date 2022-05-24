from discordtypes import (
    CommandCallbackData,
    InteractionResponse,
    ApplicationCommandInteractionDataOption,
)


class Slash:
    def __init__(self):
        self.commands = {}

    def command(
        self,
        name: str,
        description: str,
        options: ApplicationCommandInteractionDataOption = None,
    ):
        def wrap(function):
            def wrapped(*args, **kwargs):
                # TODO: Fix this so it can tell Type Dict vs Type Response so user can provide a response
                cmdresult = function(*args, **kwargs)

                response = InteractionResponse(
                    data=CommandCallbackData(content=cmdresult.get("content"))
                )

                if "type" in cmdresult.keys():
                    response.type = cmdresult["type"]

                if "flags" in cmdresult.keys():
                    response.data.flags = cmdresult["flags"]

                return response

            self.commands[name] = {
                "function": wrapped,
            }

            return wrapped

        return wrap
