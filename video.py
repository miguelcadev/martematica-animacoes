from manim import *


class Equacao(Scene):
    def construct(self):
        # Cria as fórmulas.
        primeira = MathTex("2x + 4 = 10")
        segunda = MathTex("2x = 10 - 4")
        terceira = MathTex("2x = 6")
        resultado = MathTex("x = 3", color=GREEN)

        # Mostra cada etapa.
        self.play(Write(primeira))
        self.wait(1)

        self.play(TransformMatchingTex(primeira, segunda))
        self.wait(1)

        self.play(TransformMatchingTex(segunda, terceira))
        self.wait(1)

        self.play(TransformMatchingTex(terceira, resultado))
        self.play(Circumscribe(resultado))
        self.wait(2)