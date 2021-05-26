import sympy
from typing import Union
from discord.ext.commands import Bot, Cog, Context, command


class Solvers(Cog):
    """Conjunto de comandos que contém funções capazes de resolver:

> Equações e inequações algébricas: **solve**;
> Equações Diferenciais Ordinárias (EDOs): **diffsolve**;
> Sistema de equações lineares: **solve_linear**;
> Sistemas de equações não lineares: **solve_nonlinear**.
    """
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(enabled=True, aliases=('solve_ode', 'resolver_edo',))
    async def diffsolve(self, ctx: Context, eq: str):
        """Resolve Equações Diferenciais Ordinárias (EDOs).

Atente para o fato de que a derivada primeira de uma função f qualquer com respeito à variável x é representada
por diff(f(x)).

A solução recorrentemente é expressa em termos de constantes C1, C2, C3, ..., Cn.

OBS: NÃO colocar o sinal de igualdade (=) dentro das equações. Por padrão, considera-se que qualquer expressão
inserida está igualada a zero (e.g. diff(f(x)) - x equivale a f'(x) - x = 0). Caso deseje, é possível usar o objeto
Eq(expr1, expr2) como argumento, representando expr1 = expr2 (e.g. Eq(diff(f(x)), cos(x)) equivale a f'(x) = cos(x),
como no Ex3).

Exemplos
========

Ex1: f'(x) - f(x) = 0
Input: +diffsolve "diff(f(x)) - f(x)"
Output: f(x) = C1*exp(x)

Ex2: f''(x) + f(x) = 0
Input: +diffsolve "diff(diff(f(x))) + f(x)"
Output: f(x) = C1*sin(x) + C2*cos(x)

Ex3: f'(x) = cos(x)
Input: +diffsolve "Eq(diff(f(x)), cos(x))"
Output: f(x) = C1 + sin(x)
        """
        dif_eq = sympy.sympify(eq)
        result = sympy.dsolve(dif_eq)
        result = f'{result.args[0]} = {result.args[1]}'
        result = f'```txt\n{result}```'
        await ctx.message.reply(result)
        await ctx.message.add_reaction(emoji='✅')

    @command(enabled=True, aliases=('solve_equation', 'solve_eq',
                                    'solve_inequation', 'solve_ineq',
                                    'resolver', 'resolver_equacao',
                                    'resolver_inequacao', 'resolver_eq',
                                    'resolver_ineq'))
    async def solve(self, ctx: Context, expr: str, symbol: str = None):
        """Resolve equações e inequações algébricas.

A solução recorrentemente é expressa como um conjunto de elementos. Caso a equação ou inequação inserida
não possua solução real ou complexa, o resultado será um conjunto vazio (/emptyset).

OBS1: NÃO colocar o sinal de igualdade (=) dentro das equações. Por padrão, considera-se que qualquer expressão
inserida está igualada a zero (e.g. x^2 + 2*x - 4 equivale a x² + 2x - 4 = 0, como no Ex1). Caso deseje, é possível
usar o objeto Eq(expr1, expr2) como argumento, representando expr1 = expr2 (e.g. Eq(x^3 - 6*x^2 + 11*x, 6) equivale a
x³ - 6x² + 11x = 6, como no Ex2).

OBS2: No caso de a sua equação ou inequação conter mais de uma incógnita, o símbolo que representa a variável deverá ser
obrigatoriamente especificado no parâmetro [symbol].
O restante dos símbolos será tratado como constantes, e o conjunto solução sairá em função destas (como no Ex4, no qual
especificou-se x como a variável independente).

OBS3: Os outputs do BOT podem ser convertidos para objetos matemáticos e visualizados no formato de LaTeX por meio do
comando '+to_latex <expr>' (para mais informações de como usar esse comando, utilize '+help to_latex').

Exemplos
========

Ex1: x² + 2x - 4 = 0
Input: +solve "x^2 + 2*x - 4"
Output: FiniteSet(-1 + sqrt(5), -sqrt(5) - 1)

Ex2: x³ - 6x² + 11x = 6
Input: +solve "Eq(x^3 - 6*x^2 + 11*x, 6)"
Output: FiniteSet(1, 2, 3)

Ex3: x² + 2x ≥ 𝝅
Input: +solve "x ** 2 + 2 * x >= pi"
Output: Union(Interval(-oo, -sqrt(1 + pi) - 1), Interval(-1 + sqrt(1 + pi), oo))

Ex4: x² - (𝝅 y + 1)x + 𝝅 y = 0
Input: +solve "x^2 - (pi * y + 1) * x + pi * y" "x"
Output: FiniteSet(1, pi*y)
        """
        expr = sympy.sympify(expr)
        if symbol is not None:
            symbol = sympy.symbols(symbol)

        try:
            result = sympy.solveset(expr, symbol)
        except NotImplementedError:
            result = sympy.solveset(expr, symbol, domain=sympy.S.Reals)

        result = f'```txt\n{result}```'
        await ctx.message.reply(result)
        await ctx.message.add_reaction(emoji='✅')

    @command(enabled=True, aliases=('linear_system', 'linear_sys', 'sistema_linear', 'resolver_sistema_linear'))
    async def solve_linear(self, ctx: Context, system: str, symbols: str = None):
        """Resolve um sistema de equações lineares.

A solução recorrentemente é expressa como um conjunto contendo uma tupla de ordem n do tipo (x₁, x₂, ...), tal que
n é a quantidade de variáveis dependentes do sistema.

O parâmetro <system> é bem versátil e aceita como argumento:
    • Matriz contendo os coeficientes dos termos dependentes e cuja última coluna contém os termos independentes;
    • Sequência de equações.

OBS1: No caso de o parâmetro <system> ser uma matriz, o parâmetro [symbols] permanece opcional, i.e não é necessário
especificar os símbolos das variáveis independentes (ver Ex1). No entanto, no caso de o parâmetro <system> se tratar
de uma sequência de equações algébricas, os símbolos que representam as variáveis independetes do sistema precisam ser
OBRIGATORIAMENTE especificados. O restante dos símbolos (se houver) será tratado como constantes.

OBS2: NÃO colocar o sinal de igualdade (=) dentro das equações. Por padrão, considera-se que qualquer expressão
inserida está igualada a zero (e.g. a equação 2x + y = 12 é representada como 2*x + y - 12, como no Ex2). Caso deseje,
é possível usar o objeto Eq(expr1, expr2) como argumento, representando expr1 = expr2 (e.g a equação 2x + y = 12 pode
ser representada por Eq(2*x + y, 12), como no Ex3).

Exemplos
========

Ex1:  x + y = 10
      2x + y = 12
Input: +solve_linear "
[1, 1, 10],
[2, 1, 12]"
Output: FiniteSet((2, 8))

Ex2: x + y = 10
     2x + y = 12
Input: +solve_linear "x + y - 10, 2*x + y - 12" "x, y"
Output: FiniteSet((2, 8))

Ex3: x + y = 10
     2x + y = 12
Input: +solve_linear "Eq(x + y, 10), Eq(2*x + y, 12)" "x, y"
Output: FiniteSet((2, 8))
        """
        system: Union[list, tuple] = sympy.sympify(system)
        result = None

        if isinstance(system[0], list) or isinstance(system[0], tuple):
            system = sympy.Matrix(system)
            if symbols is None:
                result = sympy.linsolve(system)

        if symbols is not None:
            symbols = sympy.sympify(symbols)
            result = sympy.linsolve(system, symbols)

        result = f'```txt\n{result}```'
        await ctx.message.reply(result)
        await ctx.message.add_reaction(emoji='✅')

    @command(enabled=False, aliases=('sistema_nao_linear', 'resolver_sistema_nao_linear'))
    async def solve_nonlinear(self, ctx: Context):
        """Resolve um sistema de equações não lineares. (em breve)"""
        ...


def setup(bot: Bot):
    bot.add_cog(Solvers(bot))
