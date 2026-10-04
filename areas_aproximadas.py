"""Áreas com o mesmo perímetro: das raízes aos números decimais.

Renderize na pasta deste arquivo:
    uv run manim -pqh --fps 120 areas_aproximadas.py AreasAproximadas

Animação em português, sem narração, com pausas para leitura.
Requer Manim Community e LaTeX. Nenhum outro arquivo do projeto é necessário.
--fps escolhe a taxa de quadros; FATOR_PAUSAS ajusta o tempo de leitura.
"""

from manim import *
from manimpango import list_fonts
import json
import os
from pathlib import Path


BG = "#0D1526"
PANEL = "#152139"
INK = "#F3F6FC"
MUTED = "#A7B4CB"
LINE = "#2C3B58"
TRI = "#54D4BC"
QUAD = "#FFCB66"
HEX = "#AC9BFA"
K_COLOR = "#FFE28B"
SUCCESS = "#72E0AA"
FONT = next((name for name in ("DejaVu Sans", "Arial", "Liberation Sans") if name in list_fonts()), "")
FATOR_PAUSAS = 1.0


class AreasAproximadas(Scene):
    def text(self, value, size=28, color=INK, max_width=12.6):
        mob = Text(value, font=FONT, font_size=size, color=color)
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        return mob

    def math(self, *values, size=40, color=INK, max_width=7.3):
        mob = MathTex(*values, font_size=size, color=color)
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        return mob

    def mark(self, name):
        self.timeline.append({"name": name, "time": float(self.renderer.time)})

    def pausa(self, seconds):
        self.wait(seconds * FATOR_PAUSAS)

    def header(self, step, title):
        small = self.text(step, 16, MUTED).move_to([-6.4, 3.7, 0], aligned_edge=LEFT)
        heading = self.text(title, 33).move_to([0, 3.18, 0])
        rule = Line([-6.4, 2.78, 0], [6.4, 2.78, 0], color=LINE, stroke_width=2)
        self.add(small, heading, rule)

    def caption(self, *lines):
        if self.caption_mob is not None:
            self.remove(self.caption_mob)
        rule = Line([-6.4, -3.15, 0], [6.4, -3.15, 0], color=LINE, stroke_width=2)
        words = VGroup(*[self.text(line, 22, MUTED) for line in lines])
        words.arrange(DOWN, buff=0.1).move_to([0, -3.57, 0])
        self.caption_mob = VGroup(rule, words)
        self.add(self.caption_mob)

    def wipe(self):
        if self.mobjects:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.clear()
        self.caption_mob = None

    def polygon(self, n, perimeter, center, color):
        radius = perimeter / (2 * n * np.sin(PI / n))
        start = PI / 2 if n == 3 else (PI / 4 if n == 4 else 0)
        points = [np.array(center) + radius * np.array([
            np.cos(start + i * TAU / n), np.sin(start + i * TAU / n), 0
        ]) for i in range(n)]
        return Polygon(*points, color=color, stroke_width=4,
                       fill_color=color, fill_opacity=0.16)

    def construct(self):
        self.camera.background_color = BG
        self.timeline = []
        self.caption_mob = None
        self.intro()
        self.root()
        self.calculate(3, "Triângulo equilátero", TRI)
        self.calculate(4, "Quadrado", QUAD)
        self.calculate(6, "Hexágono regular", HEX)
        self.compare()
        self.refine()
        self.example()
        self.answer()
        self.mark("Fim")
        timeline_path = os.environ.get("MANIM_TIMELINE")
        if timeline_path:
            Path(timeline_path).write_text(json.dumps(self.timeline, ensure_ascii=False, indent=2), encoding="utf-8")

    def intro(self):
        self.mark("Fórmulas de partida")
        self.header("CONTINUAÇÃO / QUESTÃO 171", "Agora vamos calcular os valores aproximados")
        subtitle = self.text("Mesmo perímetro K > 0 para as três formas", 27, MUTED).move_to([0, 2.22, 0])
        self.play(FadeIn(subtitle), run_time=0.8)
        entries = [
            (-4.4, 3, "Triângulo equilátero", TRI, r"A=\frac{K^2\sqrt{3}}{36}"),
            (0, 4, "Quadrado", QUAD, r"A=\frac{K^2}{16}"),
            (4.4, 6, "Hexágono regular", HEX, r"A=\frac{K^2\sqrt{3}}{24}"),
        ]
        cards = VGroup()
        for x, n, name, color, formula in entries:
            bg = RoundedRectangle(width=4.05, height=4.1, corner_radius=0.16,
                                  stroke_color=LINE, fill_color=PANEL, fill_opacity=1).move_to([x, -0.27, 0])
            label = self.text(name, 24, color, max_width=3.7).move_to([x, 1.48, 0])
            poly = self.polygon(n, 6.0, [x, -0.10, 0], color)
            eq = self.math(formula, size=37, color=color, max_width=3.6).move_to([x, -1.46, 0])
            cards.add(VGroup(bg, label, poly, eq))
        self.play(LaggedStart(*[FadeIn(card) for card in cards], lag_ratio=0.2), run_time=1.5)
        self.caption("Substituiremos √3 por um decimal e faremos as divisões.",
                     "K continua na fórmula: o enunciado não informa um valor numérico para ele.")
        self.pausa(7)
        self.wipe()

    def root(self):
        self.mark("Aproximando a raiz de 3")
        self.header("01 / APROXIMAÇÃO", "Por que podemos usar √3 ≈ 1,7?")
        root = self.math(r"\sqrt{3}=1{,}7320508\ldots", size=55, color=K_COLOR,
                         max_width=11).move_to([0, 1.86, 0])
        self.play(Write(root), run_time=1.4)
        self.caption("√3 tem infinitas casas decimais, sem um período que se repete.")
        self.pausa(3)
        left = self.math(r"1{,}7^2=2{,}89<3", size=40).move_to([-3.4, 0.47, 0])
        right = self.math(r"1{,}8^2=3{,}24>3", size=40).move_to([3.4, 0.47, 0])
        between = self.math(r"1{,}7<\sqrt{3}<1{,}8", size=45).move_to([0, -0.69, 0])
        self.play(Write(left), Write(right), run_time=1.4)
        self.play(Write(between), run_time=1)
        self.pausa(4)
        rough = self.math(r"\sqrt{3}\approx1{,}7", size=49, color=SUCCESS).move_to([0, -2.04, 0])
        self.play(Write(rough), run_time=1)
        self.caption("Arredondando para uma casa decimal, usamos 1,7.",
                     "O símbolo ≈ significa aproximadamente igual; não é uma igualdade exata.")
        self.pausa(6)
        self.wipe()

    def calculate(self, n, name, color):
        self.mark("Cálculo: " + name)
        self.header("02 / CONTAS", name + ": transformar a fórmula em decimal")
        poly = self.polygon(n, 8.4, [-4.45, 0.20, 0], color)
        label = self.text(name, 26, color, max_width=3.9).move_to([-4.45, 2.18, 0])
        side = self.math(rf"L=\frac{{K}}{{{n}}}", size=38, color=K_COLOR).move_to([-4.45, -1.58, 0])
        divider = Line([-1.8, 2.35, 0], [-1.8, -2.55, 0], color=LINE, stroke_width=2)
        self.play(Create(poly), FadeIn(label), Write(side), Create(divider), run_time=1.1)
        if n == 3:
            values = [r"A=\frac{K^2\sqrt{3}}{36}",
                      r"A\approx\frac{1{,}7}{36}\,K^2",
                      r"\frac{1{,}7}{36}=0{,}047222\ldots",
                      r"A\approx0{,}0472\,K^2"]
            captions = ["Partimos da fórmula obtida: A = K²√3/36.",
                        "Trocamos √3 por 1,7. O K² continua multiplicando.",
                        "Dividimos 1,7 por 36. O resultado é 0,047222…",
                        "Arredondamos o coeficiente para quatro casas decimais."]
        elif n == 4:
            values = [r"A=\frac{K^2}{16}",
                      r"A=\frac{1}{16}\,K^2",
                      r"\frac{1}{16}=0{,}0625",
                      r"A=0{,}0625\,K^2"]
            captions = ["O quadrado não tem raiz: A = K²/16.",
                        "Dividir K² por 16 é multiplicar K² por 1/16.",
                        "Fazemos a divisão: 1 ÷ 16 = 0,0625.",
                        "Este decimal é exato. Usamos =, sem aproximar."]
        else:
            values = [r"A=\frac{K^2\sqrt{3}}{24}",
                      r"A\approx\frac{1{,}7}{24}\,K^2",
                      r"\frac{1{,}7}{24}=0{,}070833\ldots",
                      r"A\approx0{,}0708\,K^2"]
            captions = ["Partimos da fórmula obtida: A = K²√3/24.",
                        "Trocamos √3 por 1,7 e mantemos a divisão por 24.",
                        "Dividimos 1,7 por 24. O resultado é 0,070833…",
                        "Arredondamos o coeficiente para quatro casas decimais."]
        rows = []
        for i, value in enumerate(values):
            row = self.math(value, size=43 if i == 3 else 39,
                            color=color if i == 3 else INK, max_width=7.7)
            row.move_to([2.63, 2.00 - 1.3 * i, 0])
            self.caption(captions[i])
            if i == 0:
                self.play(Write(row), run_time=1.1)
            else:
                self.play(TransformFromCopy(rows[-1], row), run_time=1.1)
            rows.append(row)
            if i == 3:
                self.play(Create(SurroundingRectangle(row, color=color, buff=0.2,
                                                      corner_radius=0.12)), run_time=0.7)
            self.pausa(5 if i == 3 else 3.5)
        self.wipe()

    def compare(self):
        self.mark("Comparação usando 1,7")
        self.header("03 / COMPARAÇÃO", "Basta comparar os números que multiplicam K²")
        entries = [(-4.4, "Triângulo equilátero", TRI, r"A\approx0{,}0472\,K^2"),
                   (0, "Quadrado", QUAD, r"A=0{,}0625\,K^2"),
                   (4.4, "Hexágono regular", HEX, r"A\approx0{,}0708\,K^2")]
        cards = VGroup()
        for x, name, color, value in entries:
            bg = RoundedRectangle(width=4.05, height=2.15, corner_radius=0.16,
                                  stroke_color=LINE, fill_color=PANEL, fill_opacity=1).move_to([x, 1.0, 0])
            label = self.text(name, 23, color, max_width=3.6).move_to([x, 1.62, 0])
            eq = self.math(value, size=37, color=color, max_width=3.6).move_to([x, 0.67, 0])
            cards.add(VGroup(bg, label, eq))
        self.play(LaggedStart(*[FadeIn(card) for card in cards], lag_ratio=0.2), run_time=1.5)
        numbers = self.math(r"0{,}0472<0{,}0625<0{,}0708", size=45, max_width=11).move_to([0, -0.93, 0])
        order = self.math(r"A_{\triangle}<A_{\square}<A_{\mathrm{hex}}", size=45).move_to([0, -2.1, 0])
        self.caption("Como K > 0, K² é positivo e igual nas três comparações.",
                     "O maior coeficiente corresponde à maior área.")
        self.play(Write(numbers), run_time=1.2)
        self.pausa(3)
        self.play(Write(order), cards[2][0].animate.set_stroke(HEX, width=4), run_time=1.2)
        self.pausa(6)
        self.wipe()

    def refine(self):
        self.mark("Refinando para 1,732")
        self.header("04 / MAIS PRECISÃO", "Usar mais casas decimais melhora a aproximação")
        root = self.math(r"\sqrt{3}\approx1{,}732", size=48, color=K_COLOR).move_to([0, 2.04, 0])
        self.play(Write(root), run_time=1.2)
        self.caption("Agora dividimos 1,732 por 36 e por 24, em vez de usar 1,7.")
        tri = self.math(r"\frac{1{,}732}{36}=0{,}048111\ldots\ \approx0{,}0481", size=37,
                        color=TRI, max_width=11.8).move_to([0, 0.91, 0])
        hexagon = self.math(r"\frac{1{,}732}{24}=0{,}072166\ldots\ \approx0{,}0722", size=37,
                            color=HEX, max_width=11.8).move_to([0, -0.24, 0])
        self.play(Write(tri), run_time=1.3)
        self.pausa(4)
        self.play(Write(hexagon), run_time=1.3)
        self.pausa(4)
        exact = self.text("Quadrado: 1/16 = 0,0625 continua exato", 26, QUAD).move_to([0, -1.43, 0])
        order = self.math(r"0{,}0481<0{,}0625<0{,}0722", size=43).move_to([0, -2.39, 0])
        self.play(FadeIn(exact), Write(order), run_time=1.2)
        self.caption("Os decimais do triângulo e do hexágono ficam mais próximos dos valores reais.",
                     "A conclusão continua a mesma: o hexágono tem a maior área.")
        self.pausa(7)
        self.wipe()

    def example(self):
        self.mark("Exemplo com K igual a 12")
        self.header("05 / EXEMPLO NUMÉRICO", "Se a cerca tivesse 12 metros de perímetro")
        perimeter = self.math(r"K=12\ \mathrm{m}\quad\Longrightarrow\quad K^2=144\ \mathrm{m}^2",
                              size=39, color=K_COLOR, max_width=11.8).move_to([0, 2.12, 0])
        self.play(Write(perimeter), run_time=1.3)
        self.caption("Este é apenas um exemplo: escolhemos K = 12 m para obter áreas em m².")
        entries = [("Triângulo", TRI, r"\frac{144\sqrt{3}}{36}=4\sqrt{3}\approx6{,}93\ \mathrm{m}^2"),
                   ("Quadrado", QUAD, r"\frac{144}{16}=9\ \mathrm{m}^2"),
                   ("Hexágono", HEX, r"\frac{144\sqrt{3}}{24}=6\sqrt{3}\approx10{,}39\ \mathrm{m}^2")]
        for i, (name, color, formula) in enumerate(entries):
            y = 0.83 - 1.2 * i
            label = self.text(name, 26, color, max_width=2.8).move_to([-5.0, y, 0])
            eq = self.math(formula, size=37, color=color, max_width=8.6).move_to([1.52, y, 0])
            self.play(FadeIn(label), Write(eq), run_time=1.2)
            self.pausa(3)
        self.caption("Calculamos com √3 e arredondamos apenas as áreas finais para duas casas decimais.")
        self.pausa(5)
        self.wipe()

    def answer(self):
        self.mark("Resumo e resposta")
        self.header("RESPOSTA", "O hexágono regular continua sendo a melhor escolha")
        entries = [("Triângulo", TRI, r"A_{\triangle}\approx0{,}0481\,K^2"),
                   ("Quadrado", QUAD, r"A_{\square}=0{,}0625\,K^2"),
                   ("Hexágono", HEX, r"A_{\mathrm{hex}}\approx0{,}0722\,K^2")]
        for i, (name, color, formula) in enumerate(entries):
            y = 1.8 - i * 1.3
            label = self.text(name, 28, color).move_to([-4.6, y, 0])
            eq = self.math(formula, size=45, color=color, max_width=8.7).move_to([1.3, y, 0])
            self.play(FadeIn(label), Write(eq), run_time=1)
        final = self.math(r"\boxed{A_{\mathrm{hex}}=\frac{K^2\sqrt{3}}{24}}", size=45,
                          color=SUCCESS).move_to([0, -2.14, 0])
        self.play(Write(final), run_time=1.3)
        self.caption("A fórmula com √3 é exata. Os decimais ajudam a comparar as áreas.",
                     "Resultado da questão: alternativa A.")
        self.pausa(8)
