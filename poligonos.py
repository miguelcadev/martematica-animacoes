from manim import *
import numpy as np


class PoligonoParaCirculo(Scene):
    def construct(self):
        titulo = Text(
            "Dos polígonos ao círculo",
            font_size=36,
        ).to_edge(UP)

        raio = 2.1
        centro = LEFT * 3

        def criar_poligono(lados):
            pontos = [
                centro + raio * np.array([
                    np.cos(PI / 2 + TAU * i / lados),
                    np.sin(PI / 2 + TAU * i / lados),
                    0,
                ])
                for i in range(lados)
            ]

            return Polygon(
                *pontos,
                color=BLUE,
                fill_color=BLUE,
                fill_opacity=0.2,
                stroke_width=4,
            )

        # Fórmulas das áreas dos polígonos regulares.
        dados = {
            3: (
                "Triângulo equilátero",
                r"A = \frac{\sqrt{3}}{4}L^2",
            ),
            4: (
                "Quadrado",
                r"A = L^2",
            ),
            5: (
                "Pentágono regular",
                r"A = \frac{\sqrt{25+10\sqrt{5}}}{4}L^2",
            ),
            6: (
                "Hexágono regular",
                r"A = \frac{3\sqrt{3}}{2}L^2",
            ),
            7: (
                "Heptágono regular",
                r"A = \frac{7L^2}{4\tan(\pi/7)}",
            ),
            8: (
                "Octógono regular",
                r"A = 2(1+\sqrt{2})L^2",
            ),
        }

        def criar_painel(lados):
            nome, formula = dados[lados]

            cabecalho = Text(nome, font_size=28)
            expressao = MathTex(
                formula,
                font_size=42,
                color=YELLOW,
            )
            legenda = Text(
                "L = comprimento do lado",
                font_size=22,
            )

            painel = VGroup(cabecalho, expressao, legenda)
            painel.arrange(DOWN, buff=0.5)

            if painel.width > 6:
                painel.scale_to_fit_width(6)

            painel.move_to(RIGHT * 3.3)
            return painel

        referencia = Circle(
            radius=raio,
            color=GRAY,
            stroke_opacity=0.4,
        ).move_to(centro)

        poligono = criar_poligono(3)
        painel = criar_painel(3)

        numero = Integer(3, font_size=32, color=YELLOW)
        contador = VGroup(
            Text("Lados:", font_size=28),
            numero,
        ).arrange(RIGHT, buff=0.3)
        contador.move_to(centro + DOWN * 2.7)

        self.play(Write(titulo))
        self.play(
            Create(referencia),
            Create(poligono),
            FadeIn(contador),
            FadeIn(painel),
        )
        self.wait(3)

        # Mostra cada fórmula, do quadrado ao octógono.
        for lados in range(4, 9):
            novo_poligono = criar_poligono(lados)
            novo_painel = criar_painel(lados)

            self.play(
                Transform(poligono, novo_poligono),
                ChangeDecimalToValue(numero, lados),
                FadeOut(painel, shift=UP * 0.2),
                FadeIn(novo_painel, shift=UP * 0.2),
                run_time=1,
            )

            painel = novo_painel
            self.wait(3)

        # Depois do octógono, mostra a fórmula geral.
        painel_geral = VGroup(
            Text("Polígono regular de n lados", font_size=27),
            MathTex(
                r"A = \frac{nL^2}{4\tan(\pi/n)}",
                font_size=42,
                color=YELLOW,
            ),
            Text("n = quantidade de lados", font_size=22),
            Text("L = comprimento do lado", font_size=22),
        ).arrange(DOWN, buff=0.4)
        painel_geral.move_to(RIGHT * 3.3)

        self.play(
            FadeOut(painel),
            FadeIn(painel_geral),
        )

        for lados in [9, 10, 12, 16, 24, 32, 48, 64, 96]:
            self.play(
                Transform(poligono, criar_poligono(lados)),
                ChangeDecimalToValue(numero, lados),
                run_time=0.7,
            )
            self.wait(0.3)

        # Encerra com o círculo e sua fórmula.
        circulo = Circle(
            radius=raio,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.2,
            stroke_width=4,
        ).move_to(centro)

        painel_circulo = VGroup(
            Text("Círculo", font_size=32),
            MathTex(
                r"A = \pi r^2",
                font_size=48,
                color=YELLOW,
            ),
            Text("r = raio do círculo", font_size=22),
        ).arrange(DOWN, buff=0.5)
        painel_circulo.move_to(RIGHT * 3.3)

        self.play(
            Transform(poligono, circulo),
            FadeOut(referencia),
            FadeOut(contador),
            FadeOut(painel_geral),
            FadeIn(painel_circulo),
            run_time=2,
        )
        self.wait(4)