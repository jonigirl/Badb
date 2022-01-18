from discord.ext import commands, vbu
import json


class DataIO(vbu.Cog):

    def __init__(self, bot):
        self.bot = bot

    def fileIO(filename, IO, data=None):
        if IO == "save" and data is None:
            with open(filename, encoding='utf-8', mode="w") as f:
                f.write(
                    json.dumps(data, indent=4, sort_keys=True, separators=(
                        ',', ' : ')))
        elif IO == "load" and data is None:
            with open(filename, encoding='utf-8', mode="r") as f:
                return json.loads(f.read())
        elif IO == "check" and data is None:
            try:
                with open(filename, encoding='utf-8', mode="r") as f:
                    return True
            except Exception as e:
                logging.exception()
                return False
        else:
            raise("Invalid fileIO call")

    def get_value(filename, key):
        with open(filename, encoding='utf-8', mode="r") as f:
            data = json.loads(f.read())
        return data[key]

    def set_value(filename, key, value):
        data = fileIO(filename, "load")
        data[key] = value
        fileIO(filename, "save", data)
        return True


def setup(bot: vbu.Bot):
    x = DataIO(bot)
    bot.add_cog(x)
