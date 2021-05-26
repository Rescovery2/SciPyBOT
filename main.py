import sympy
from discord import Message
from discord.errors import LoginFailure
from discord.ext.commands import Bot, Context, when_mentioned_or
from pretty_help import DefaultMenu, PrettyHelp


# BOT CONFIG
command_prefix = '+'

token = 'ODQzNjIwNjMxMjAyNjI3NTg1.YKGg8A.3lIhx_9L7-Y2kusy7-eoUqysoy4'
client = Bot(command_prefix=when_mentioned_or(command_prefix),
             case_insensitive=True)


@client.event
async def on_ready():
    print(f'Logged as {client.user}')

    bot_name = str(client.user)[:-5]

    # HELP COMMAND
    help_menu = DefaultMenu(active_time=30)
    help_command = PrettyHelp(index_title=f'**{bot_name} Commands**', no_category='Helpful Commands',
                              menu=help_menu, ending_note=f'Developed by Rescovery')
    client.help_command = help_command

    # BOT DESCRIPTION
    description = f'''
**COMO USAR O {bot_name}** :question:

> Digite `{command_prefix}help <command>` ou `@{bot_name} help <command>` para mais 
> informações sobre o comando. Você também pode digitar `{command_prefix}help <category>` 
> ou `@{bot_name} help <category>` para obter mais informações sobre a categoria.
'''
    client.description = description


@client.event
async def on_message_edit(before: Message, after: Message):
    if before:
        pass

    await client.process_commands(after)


@client.command(enabled=False)
async def say(ctx: Context, **kwargs):
    # msg = kwargs.pop('msg')
    await ctx.message.reply(kwargs)


# HELPFUL COMMANDS #
@client.command(enabled=True)
async def ping(ctx: Context):
    """Use para verificar se a instância do BOT está online. Caso sim, o BOT responderá com 'pong'.
    """
    await ctx.message.reply('pong')
    await ctx.message.add_reaction(emoji='✅')


@client.command(enabled=True, aliases=('latex', 'converter_para_latex'))
async def to_latex(ctx: Context, expr: str):
    """Converte uma expressão dada para seu formato em LaTeX.
    """
    expr = sympy.sympify(expr)
    result = sympy.latex(expr)
    result = f'```txt\n{result}```'
    await ctx.message.reply(result)
    await ctx.message.add_reaction(emoji='✅')


# CONSTANTS #
client.load_extension("cogs.constants")

# DIFFERENTIAL AND INTEGRAL CALCULUS #
client.load_extension("cogs.calculus")

# SOLVERS #
client.load_extension("cogs.solvers")

# GRAPHICS #
client.load_extension("cogs.graphics")


# MAINLOOP #
def main():
    try:
        client.run(token)
    except LoginFailure:
        print('401: Access denied')


if __name__ == '__main__':
    main()
