import sympy
from discord.ext.commands import Bot, Cog, Context, command


class Calculus(Cog):
    """Conjunto de comandos que contém operações fundamentais do Cálculo (limites,
derivadas e integrais), bem como séries, transformadas e funções especiais.
    """
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(enabled=True, aliases=('limite',))
    async def limit(self, ctx: Context, func: str, var: str, value: str, way: str = '+-'):
        """Calcula limites laterais e bilaterais de funções de uma única variável.

Parâmetros
==========
        func: Função de uma variável.
        var: Variável independete da função.
        value: Valor para o qual tende a variável independente.
        way: Especifica se o limite é lateral pela direita (+), pela esquerda (-) ou bilateral (+-). Por padrão,
        way = +- ;

Exemplos
========

Ex1: lim sin(𝝅 x)/x
     x->0
Input: +limit "sin(pi*x)/x" "x" "0"
Output: pi

Ex2: lim (1 + x)^(1/x)
    x->0⁺
Input: +limit "(1+x)^(n/x)" "x" "0" "+"
Output: exp(n)

Ex3: lim 1/x
    x->-∞
Input: +limit "1/x" "x" "-oo"
Output: 0
        """
        result = sympy.limit(func, var, value, dir=way)
        result = f'```txt\n{result}```'
        await ctx.message.reply(result)
        await ctx.message.add_reaction(emoji='✅')

    @command(enabled=True, aliases=('derivative', 'derivada'))
    async def diff(self, ctx: Context, func: str, *symbols):
        """Calcula a n-esima derivada de uma função de uma ou mais variáveis.

Exemplos
========

Para calcular a derivada primeira de f(x) = sin(x), basta escrever:

Ex1:
Input: +diff "sin(x)"
Output: cos(x)

No caso de a função possuir mais de um símbolo, você deve especificar a variável independente.

Ex2:
Input: +diff "a * x^2" "x"
Output: 2*a*x

Se deseja calcular a derivada parcial de ordem 2 da função f(x, y) = x² + y² com respeito a x e y, escreva:

Ex3:
Input: +diff "x^2 + y^2" "x" "y"
Output: 0

No caso de derivadas parciais de ordem igual ou superior a 3, é necessário especificar a ordem de cada uma das variáveis
independentes. Por exemplo, suponha que queiramos calcular a derivada parcial de ordem 3 da função
f(x, y) = x⁵y³ + x³y⁴ + 2x + y + 1 com respeito a x² e y¹. Então:

Ex4:
Input: +diff "x^5 * y^3 + x^3 * y^4 + 2 * x + y + 1" "(x, 2)" "(y, 1)"
Output: 12*x*y**2*(5*x**2 + 2*y)

ou então:

Input: +diff "x^5 * y^3 + x^3 * y^4 + 2 * x + y + 1" "x" "2" "y" "1"
Output: 12*x*y**2*(5*x**2 + 2*y)
        """
        result = sympy.diff(func, *symbols)
        result = f'```txt\n{result}```'
        await ctx.message.reply(result)
        await ctx.message.add_reaction(emoji='✅')

    @command(enabled=True, aliases=('integral',))
    async def integrate(self, ctx: Context, func: str, *symbols: str):
        """Calcula a integral (indefinida ou definida) de uma função de várias variáveis.

Exemplos
========

Para obter a primitva de f(x) = cos(x), basta escrever:

Ex1:
Input: +integrate "cos(x)"
Output: sin(x)

A integral definida de f(x) = cos(x) no intervalo de 0 a 𝝅 / 2 é obtida por:

Ex2:
Input: +integrate "cos(x)" "(x, 0, pi/2)"
Output: 1

ou ainda

Input: +integrate "cos(x)" "x, 0, pi/2"
Output: 1

Se quisermos obter a primitiva de f(x) = ln(ax) com respeito a x, fazemos:

Ex3:
Input: +integrate "log(a*x)" "x"
Output: x*log(a*x) - x

OBS: A função log recebe dois parâmetros: arg e base. Por padrão, se a base não for especificada, considera-se
o logaritmo natual ln(x).

Para o caso das integrais múltiplas, suponha que queiramos obter a primitiva de f(x, y) = x + 2y com respeito a
y e x, com y ∈ [2x², 1 + x²] e x ∈ [-1, 1], então:

Ex4:
Input: +integrate "x + 2*y" "y, 2x^2, 1 + x^2" "x, -1, 1"
Output: 32/15
        """
        args = []
        for symbol in symbols:
            arg = sympy.sympify(symbol)
            args.append(arg)

        result = sympy.integrate(func, *args)
        result = f'```txt\n{result}```'
        await ctx.message.reply(result)
        await ctx.message.add_reaction(emoji='✅')

    @command(enabled=True, aliases=('laplace', 'transformada_laplace'))
    async def laplace_transform(self, ctx: Context, func: str, t: str, s: str = 's'):
        """Calcula a transformada de Laplace para uma função de uma variável dada, em função da frequência s.

Exemplos
========

A transformada de Laplace para a função f(t) = cos(t) é dada por:

Ex:
Input: +laplace_transform "cos(t)" "t"
Output: s/(s**2 + 1)

onde 's' é a frequência da transformada de Laplace da função f(t) = cos(t)
        """
        result = sympy.laplace_transform(func, t, s)[0]
        result = f'```txt\n{result}```'
        await ctx.message.reply(result)
        await ctx.message.add_reaction(emoji='✅')

    @command(enabled=True, aliases=('gamma_function', 'gamma_func', 'funcao_gama', 'funcao_gamma_euler'))
    async def gamma(self, ctx: Context, n: str):
        """Calcula a função Gamma de Euler aplicada em um número complexo n, tal que Re(n) > 0.

OBS1: A unidade imaginária, por padrão, é representada pela letra 'I' maiúsculo.

Exemplos
========

Ex1: Γ(1/2) = √𝝅
Input: +gamma "1/2"
Output: 1.77245385090552

Ex2:
Input: +gamma "-5 * exp(I * pi)"
Output: 24.0000000000000
        """
        result = sympy.gamma(n).evalf()
        result = f'```txt\n{result}```'
        await ctx.message.reply(result)
        await ctx.message.add_reaction(emoji='✅')

    @command(enabled=True, aliases=('taylor', 'taylor_series', 'serie_taylor'))
    async def series(self, ctx: Context, expr: str, var: str = None, n: str = 6, x0: str = 0):
        """"""
        result = sympy.series(expr, x=var, n=n, x0=x0)
        result = f'```txt\n{result}```'
        await ctx.message.reply(result)
        await ctx.message.add_reaction(emoji='✅')

    @command(enabled=True, aliases=('somatorio',))
    async def summation(self, ctx: Context, expr: str, symbol: str, start: str, end: str):
        """"""
        serie = sympy.summation(expr, (symbol, start, end))
        try:
            result = float(serie.evalf())
        except TypeError:
            result = serie.evalf()

        result = f'```txt\n{result}```'
        await ctx.message.reply(result)
        await ctx.message.add_reaction(emoji='✅')

    @command(enabled=True, aliases=('produtorio',))
    async def product(self, ctx: Context, expr: str, symbol: str, start: str, end: str):
        """"""
        serie = sympy.product(expr, (symbol, start, end))
        try:
            result = float(serie.evalf())
        except TypeError:
            result = serie.evalf()

        result = f'```txt\n{result}```'
        await ctx.message.reply(result)
        await ctx.message.add_reaction(emoji='✅')


def setup(bot: Bot):
    bot.add_cog(Calculus(bot))
