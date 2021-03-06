import lightbulb
import random

from bot.bot import Bot


class Fun(lightbulb.Plugin):
    @lightbulb.command(name='hello', aliases=('hi', 'hey',))
    async def command_hello(self, ctx: lightbulb.Context) -> None:
        greeting = random.choice(('Hello', "Hi", 'Hey'))
        await ctx.respond(f"{greeting} {ctx.member.mention}", user_mentions=True)

    @lightbulb.command(name='dice', aliases=('roll',))
    async def command_dice(self, ctx:lightbulb.Context, dice: str) -> None:
        number, highets = (int(term) for term in dice.split('d'))

        if number > 25:
            return await ctx.respond("I can only roll up to 20 dice at one time")

        rolls = [random.randint(1, highets) for i in range(number)]
        await ctx.respond(" + ".join(str(r) for r in rolls) + f" = {sum(rolls)}", reply=True, mentions_reply=True)


def load(bot: Bot) -> None:
    bot.add_plugin(Fun())


def unload(bot: Bot) -> None:
    bot.remove_plugin('Meta')