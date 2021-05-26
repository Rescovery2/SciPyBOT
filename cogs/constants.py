import numpy as np
from discord.ext.commands import Bot, Cog, Context, command


class Constants(Cog):
    """
Conjunto de comandos que contém importantes constantes matemáticas e físicas.
    """
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(enabled=True)
    async def pi(self, ctx: Context, n: str = '4'):
        """
Arredonda o valor de pi para n casas decimais.

Caso nenhum argumento seja atribuído a n, por padrão a função é aplicada em n = 4.

Exemplos
========

Ex1:
Input: +pi
Output: 3.1416

Ex2:
Input: +pi 10
Output: 3.1415926536
        """
        result = f'```txt\n{np.pi:.{n}f}```'
        await ctx.message.reply(result)
        await ctx.message.add_reaction(emoji='✅')

    @command(enabled=True, aliases=('e', 'euler_constant', 'constante_euler'))
    async def euler(self, ctx: Context, n: str = '4'):
        """
Arredonda o valor da constante de Euler para n casas decimais.

Caso nenhum argumento seja atribuído a n, por padrão a função é aplicada em n = 4.

Exemplos
========

Ex1:
Input: +euler
Output: 2.7183

Ex2:
Input: +euler 10
Output: 2.7182818285
        """
        result = f'```txt\n{np.e:.{n}f}```'
        await ctx.message.reply(result)
        await ctx.message.add_reaction(emoji='✅')


def setup(bot: Bot):
    bot.add_cog(Constants(bot))
