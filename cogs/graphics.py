import asyncio
import sympy
import numpy as np
import matplotlib.pyplot as plt
from discord import File, Embed, Message
from discord.ext.commands import Bot, Cog, Context, command


class Func(object):
    def __init__(self, expr: str):
        self.expr = sympy.sympify(expr)

    @property
    def args(self):
        return list(self.expr.free_symbols)

    def __call__(self, *args, **kwargs):
        subs = {}
        for i, arg in enumerate(args):
            subs[self.args[i]] = arg

        return float(self.expr.evalf(subs=subs))


class Graphics(Cog):
    """Conjunto de comandos criados com o intuito de mostrar a visualização de funções e curvas em 2D e 3D.
    """
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def graph_2d_generate(fmt: str, x, *functions) -> File:
        for func in functions:
            f = Func(func)
            y = [f(t) for t in x]
            plt.plot(x, y, label=rf'${sympy.latex(f.expr)}$')

        plt.legend()
        file_name = f'Client Data/graph.{fmt}'
        plt.savefig(fname=file_name)
        plt.close()
        return File(file_name)

    @command(enabled=True, aliases=('plot', 'plotar2d', 'plotar'))
    async def plot2d(self, ctx: Context, interval: str, *functions: str):
        """Plota um gráfico 2D personalizável de todas as funções dadas dentro do intervalo inserido.

Exemplos
========

Para plotar a função f(x) = sin(x) no intervalo [0, 2𝛑], fazemos:

Ex1: f: [0, 2𝛑] → ℝ; f(x) = sin(x)
Input: +plot2d "0, 2*pi" "sin(x)"

É possível plotar mais de uma função no mesmo intervalo.
Por exemplo, considere as funções f, g, h: [1, 20] → ℝ; f(x) = -1/x, g(x) = sin(x) / x e h(x) = -f(x) = 1/x, então:

Ex2: f, g, h: [1, 20] → ℝ; f(x) = -1/x, g(x) = sin(x) / x, h(x) = -f(x) = 1/x
Input: +plot2d "1, 20" "-1/x" "sin(x) / x" "1/x"
        """
        def check_reaction(reaction, user):
            return user == ctx.author and (str(reaction) == '🔄' or str(reaction) == '📃')

        fmt = ['png', 'jpeg', 'jpg', 'pdf', 'svg', 'svgz', 'eps', 'pgf', 'ps', 'raw', 'rgba', 'tif', 'tiff']
        count_style = count_fmt = 0

        a, b = sympy.sympify(interval)
        a, b = float(a), float(b)
        x = np.linspace(start=a, stop=b, num=100)

        while True:
            with plt.style.context(plt.style.available[count_style]):
                img = self.graph_2d_generate(fmt[count_fmt], x, *functions)

            embed = Embed(title=f'✅ Arquivo .{fmt[count_fmt]} gerado com sucesso!',
                          description='''🔄 Atualizar o estilo do gráfico.
📃 Atualizar o formato do arquivo.''')
            response1: Message = await ctx.send(embed=embed)
            response2: Message = await ctx.send(file=img)

            await response1.add_reaction(emoji='🔄')
            await response1.add_reaction(emoji='📃')
            await ctx.message.add_reaction(emoji='✅')

            try:
                react, u = await self.bot.wait_for(event='reaction_add', timeout=60., check=check_reaction)
                if str(react) == '🔄':
                    count_style += 1

                    if count_style == 26:
                        count_style = 0

                if str(react) == '📃':
                    count_fmt += 1

                    if count_fmt == 13:
                        count_fmt = 0

            except asyncio.exceptions.TimeoutError:
                await response1.clear_reactions()
                embed = Embed(title=f'✅ Arquivo .{fmt[count_fmt]} gerado com sucesso!')
                await response1.edit(embed=embed)
                break

            else:
                await response1.delete()
                await response2.delete()

    @command(enabled=True, aliases=('plotar3d',))
    async def plot3d(self, ctx: Context, interval_x: str, interval_y: str, *functions: str):
        """Plota um gráfico 3D de todas as funções de duas variáveis dadas dentro do intervalo inserido."""
        def check_reaction(reaction, user):
            return user == ctx.author and str(reaction) == '📃'

        fmt = ['png', 'jpeg', 'jpg', 'pdf', 'svg', 'svgz', 'eps', 'pgf', 'ps', 'raw', 'rgba', 'tif', 'tiff']
        count_fmt = 0

        x, y = sympy.sympify(interval_x), sympy.sympify(interval_y)
        graph = sympy.plotting.plot3d(*functions, x, y, show=False)

        while True:
            file_name = f'Client Data/graph3d.{fmt[count_fmt]}'
            graph.save(file_name)
            img = File(file_name)

            embed = Embed(title=f'✅ Arquivo .{fmt[count_fmt]} gerado com sucesso!',
                          description='''📃 Atualizar o formato do arquivo.''')
            response1: Message = await ctx.send(embed=embed)
            response2: Message = await ctx.send(file=img)

            await response1.add_reaction(emoji='📃')
            await ctx.message.add_reaction(emoji='✅')

            try:
                react, u = await self.bot.wait_for(event='reaction_add', timeout=60., check=check_reaction)
                if str(react) == '📃':
                    count_fmt += 1

                    if count_fmt == 13:
                        count_fmt = 0

            except asyncio.exceptions.TimeoutError:
                await response1.clear_reactions()
                embed = Embed(title=f'✅ Arquivo .{fmt[count_fmt]} gerado com sucesso!')
                await response1.edit(embed=embed)
                break

            else:
                await response1.delete()
                await response2.delete()

    @command(enabled=True, aliases=('plot_parametric', 'plot_parametric_curve',
                                    'plotar_curva_parametrica', 'curva_parametrica'))
    async def plot_parametric2d(self, ctx: Context, interval: str, *expr: str):
        """"""
        def check_reaction(reaction, user):
            return user == ctx.author and str(reaction) == '📃'

        fmt = ['png', 'jpeg', 'jpg', 'pdf', 'svg', 'svgz', 'eps', 'pgf', 'ps', 'raw', 'rgba', 'tif', 'tiff']
        count_fmt = 0
        
        interval = tuple(sympy.sympify(interval))
        args = []
        for e in expr:
            arg = sympy.sympify(e)
            args.append(arg)

        graph = sympy.plot_parametric(*args, interval, show=False)

        while True:
            file_name = f'Client Data/graph_parametric.{fmt[count_fmt]}'
            graph.save(file_name)
            img = File(file_name)

            embed = Embed(title=f'✅ Arquivo .{fmt[count_fmt]} gerado com sucesso!',
                          description='''📃 Atualizar o formato do arquivo.''')
            response1: Message = await ctx.send(embed=embed)
            response2: Message = await ctx.send(file=img)

            await response1.add_reaction(emoji='📃')
            await ctx.message.add_reaction(emoji='✅')

            try:
                react, u = await self.bot.wait_for(event='reaction_add', timeout=60., check=check_reaction)
                if str(react) == '📃':
                    count_fmt += 1

                    if count_fmt == 13:
                        count_fmt = 0

            except asyncio.exceptions.TimeoutError:
                await response1.clear_reactions()
                embed = Embed(title=f'✅ Arquivo .{fmt[count_fmt]} gerado com sucesso!')
                await response1.edit(embed=embed)
                break

            else:
                await response1.delete()
                await response2.delete()

    @command(enabled=True, aliases=())
    async def plot_parametric3d_line(self, ctx: Context, expr: str, interval: str = None):
        """"""
        def check_reaction(reaction, user):
            return user == ctx.author and str(reaction) == '📃'

        fmt = ['png', 'jpeg', 'jpg', 'pdf', 'svg', 'svgz', 'eps', 'pgf', 'ps', 'raw', 'rgba', 'tif', 'tiff']
        count_fmt = 0
        
        expr = tuple(sympy.sympify(expr))

        if interval is not None:
            interval = tuple(sympy.sympify(interval))
            graph = sympy.plotting.plot3d_parametric_line(*expr, interval, show=False)
        else:
            graph = sympy.plotting.plot3d_parametric_line(*expr, show=False)

        while True:
            file_name = 'Client Data/graph_parametric3d_line.png'
            graph.save(file_name)
            img = File(file_name)

            embed = Embed(title=f'✅ Arquivo .{fmt[count_fmt]} gerado com sucesso!',
                          description='''📃 Atualizar o formato do arquivo.''')
            response1: Message = await ctx.send(embed=embed)
            response2: Message = await ctx.send(file=img)

            await response1.add_reaction(emoji='📃')
            await ctx.message.add_reaction(emoji='✅')

            try:
                react, u = await self.bot.wait_for(event='reaction_add', timeout=60., check=check_reaction)
                if str(react) == '📃':
                    count_fmt += 1

                    if count_fmt == 13:
                        count_fmt = 0

            except asyncio.exceptions.TimeoutError:
                await response1.clear_reactions()
                embed = Embed(title=f'✅ Arquivo .{fmt[count_fmt]} gerado com sucesso!')
                await response1.edit(embed=embed)
                break

            else:
                await response1.delete()
                await response2.delete()

    @command(enabled=True, aliases=())
    async def plot_parametric3d_surface(self, ctx: Context, expr: str, interval_u: str = None, interval_v: str = None):
        """"""
        def check_reaction(reaction, user):
            return user == ctx.author and str(reaction) == '📃'

        fmt = ['png', 'jpeg', 'jpg', 'pdf', 'svg', 'svgz', 'eps', 'pgf', 'ps', 'raw', 'rgba', 'tif', 'tiff']
        count_fmt = 0
        
        expr = tuple(sympy.sympify(expr))
        intervals = []

        if interval_u is not None:
            interval_u = tuple(sympy.sympify(interval_u))
            intervals.append(interval_u)

        if interval_v is not None:
            interval_v = tuple(sympy.sympify(interval_v))
            intervals.append(interval_v)

        graph = sympy.plotting.plot3d_parametric_surface(*expr, *intervals, show=False)
        
        while True:
            file_name = f'Client Data/graph_parametric3d_surface.{fmt[count_fmt]}'
            graph.save(file_name)
            img = File(file_name)

            embed = Embed(title=f'✅ Arquivo .{fmt[count_fmt]} gerado com sucesso!',
                          description='''📃 Atualizar o formato do arquivo.''')
            response1: Message = await ctx.send(embed=embed)
            response2: Message = await ctx.send(file=img)

            await response1.add_reaction(emoji='📃')
            await ctx.message.add_reaction(emoji='✅')

            try:
                react, u = await self.bot.wait_for(event='reaction_add', timeout=60., check=check_reaction)
                if str(react) == '📃':
                    count_fmt += 1

                    if count_fmt == 13:
                        count_fmt = 0

            except asyncio.exceptions.TimeoutError:
                await response1.clear_reactions()
                embed = Embed(title=f'✅ Arquivo .{fmt[count_fmt]} gerado com sucesso!')
                await response1.edit(embed=embed)
                break

            else:
                await response1.delete()
                await response2.delete()


def setup(bot: Bot):
    bot.add_cog(Graphics(bot))
