"""Questão 171: jardins regulares com o mesmo perímetro.

Renderize na pasta deste arquivo:
    uv run manim -pqh --fps 30 perimetro_jardim.py JardimPerimetro

O vídeo é uma demonstração visual em português, sem narração.
O enunciado está transcrito abaixo: não é necessário nenhum arquivo de imagem.
Testado com Manim Community. Requer LaTeX, como as demais cenas com MathTex.
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


class JardimPerimetro1(Scene):
    """Enunciado → perímetros → áreas → substituições → resposta."""

    def text(self, value, size=28, color=INK, max_width=12.8, **kwargs):
        mob = Text(value, font=FONT, font_size=size, color=color, **kwargs)
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

    def header(self, step, title):
        small = self.text(step, 16, MUTED).move_to([-6.42, 3.70, 0], aligned_edge=LEFT)
        heading = self.text(title, 34, max_width=12.8).move_to([0, 3.19, 0])
        rule = Line([-6.4, 2.78, 0], [6.4, 2.78, 0], color=LINE, stroke_width=2)
        self.chrome = VGroup(small, heading, rule)
        self.add(self.chrome)

    def caption(self, *lines):
        if hasattr(self, "caption_mob") and self.caption_mob is not None:
            self.remove(self.caption_mob)
        rule = Line([-6.4, -3.15, 0], [6.4, -3.15, 0], color=LINE, stroke_width=2)
        words = VGroup(*[self.text(line, 22, MUTED, max_width=12.7) for line in lines])
        words.arrange(DOWN, buff=0.10).move_to([0, -3.57, 0])
        self.caption_mob = VGroup(rule, words)
        self.add(self.caption_mob)

    def clear(self):
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=0.65)
        self.caption_mob = None

    def polygon(self, n, perimeter, center, color):
        # Todos os desenhos de uma comparação usam a mesma escala e perímetro.
        radius = perimeter / (2 * n * np.sin(PI / n))
        start = PI / 2 if n == 3 else (PI / 4 if n == 4 else 0)
        points = [
            np.array(center) + radius * np.array([np.cos(start + i * TAU / n),
                                                np.sin(start + i * TAU / n), 0])
            for i in range(n)
        ]
        return Polygon(*points, color=color, stroke_width=4,
                       fill_color=color, fill_opacity=0.15)

    def side_labels(self, poly, color=INK, size=29, distance=0.27):
        points = poly.get_vertices()
        center = np.mean(points, axis=0)
        labels = VGroup()
        for i, p in enumerate(points):
            midpoint = (p + points[(i + 1) % len(points)]) / 2
            direction = midpoint - center
            direction /= np.linalg.norm(direction)
            labels.add(self.math("L", size=size, color=color).move_to(midpoint + distance * direction))
        return labels

    def construct(self):
        self.camera.background_color = BG
        self.timeline = []
        self.caption_mob = None
        self.question()
        self.perimeters()
        self.triangle_area()
        self.square_area()
        self.hexagon_area()
        self.substitute(3, "Triângulo equilátero", TRI)
        self.substitute(4, "Quadrado", QUAD)
        self.substitute(6, "Hexágono regular", HEX)
        self.compare()
        self.answer()
        self.mark("Fim")
        # Usado apenas na conferência do vídeo; não cria arquivos no uso normal.
        timeline_path = os.environ.get("MANIM_TIMELINE")
        if timeline_path:
            Path(timeline_path).write_text(json.dumps(self.timeline, ensure_ascii=False, indent=2), encoding="utf-8")

    def question(self):
        self.mark("Enunciado")
        self.header("QUESTÃO 171", "Mesma cerca. Qual jardim terá a maior área?")
        statement = VGroup(
            self.text("Um jardineiro dispõe de K metros lineares de cerca baixa para fazer um jardim ornamental.", 23),
            self.text("O jardim deve ter a forma de um triângulo equilátero, um quadrado ou um hexágono regular.", 23),
            self.text("A escolha será pela forma que resulte na maior área.", 23),
        ).arrange(DOWN, buff=0.14).move_to([0, 2.03, 0])
        self.play(FadeIn(statement), run_time=0.9)
        options = [
            ("A", "Hexágono regular", r"A=\frac{K^2\sqrt{3}}{24}"),
            ("B", "Hexágono regular", r"A=\frac{3K^2\sqrt{3}}{2}"),
            ("C", "Quadrado", r"A=\frac{K^2}{16}"),
            ("D", "Triângulo equilátero", r"A=\frac{K^2\sqrt{3}}{36}"),
            ("E", "Triângulo equilátero", r"A=\frac{K^2\sqrt{3}}{4}"),
        ]
        rows = VGroup()
        for i, (letter, name, formula) in enumerate(options):
            y = 0.90 - i * 0.82
            badge = Circle(radius=0.17, color=LINE, fill_color=PANEL, fill_opacity=1).move_to([-5.3, y, 0])
            letter_mob = self.text(letter, 20).move_to(badge)
            name_mob = self.text(name, 23).move_to([-4.87, y, 0], aligned_edge=LEFT)
            formula_mob = self.math(formula, size=27).move_to([3.15, y, 0])
            rows.add(VGroup(badge, letter_mob, name_mob, formula_mob))
        self.play(LaggedStart(*[FadeIn(row) for row in rows], lag_ratio=0.16), run_time=1.6)
        self.caption("K é o perímetro total da cerca, com K > 0. Vamos calcular a área de cada forma.")
        self.wait(6)
        self.clear()

    def perimeters(self):
        for n, name, color in [(3, "Triângulo equilátero", TRI), (4, "Quadrado", QUAD), (6, "Hexágono regular", HEX)]:
            self.mark("Perímetro: " + name)
            self.header("01 / PERÍMETRO", "O perímetro é a soma de todos os lados")
            self.caption(f"O {name.lower()} tem {n} lados iguais. Cada lado mede L.")
            poly = self.polygon(n, 8.4, [-4.1, 0.45, 0], color)
            label = self.text(name, 28, color, max_width=4).move_to([-4.1, 2.35, 0])
            points = poly.get_vertices()
            edges = VGroup(*[Line(points[i], points[(i + 1) % n], color=color, stroke_width=5) for i in range(n)])
            side_labels = self.side_labels(poly, color)
            poly.set_stroke(opacity=0)
            self.play(FadeIn(poly), FadeIn(label), run_time=0.5)
            self.play(LaggedStart(*[
                AnimationGroup(Create(edge), FadeIn(side_label))
                for edge, side_label in zip(edges, side_labels)
            ], lag_ratio=0.27), run_time=2)
            sum_eq = self.math("K=" + "+".join(["L"] * n), size=37, max_width=7.1).move_to([2.25, 1.50, 0])
            self.play(Write(sum_eq), run_time=1.2)
            self.wait(1.1)
            simple = self.math(f"K={n}L", size=44).move_to([2.25, 0.28, 0])
            self.play(TransformFromCopy(sum_eq, simple), run_time=0.9)
            self.caption(f"Dividindo os dois lados da igualdade por {n}, isolamos a medida L.")
            result = self.math(rf"L=\frac{{K}}{{{n}}}", size=50, color=K_COLOR).move_to([2.25, -1.08, 0])
            box = SurroundingRectangle(result, color=color, buff=0.22, corner_radius=0.12)
            self.play(TransformFromCopy(simple, result), Create(box), run_time=1)
            # As cópias dos lados são alinhadas: o comprimento total continua K.
            fence = VGroup(*[
                Line([-4.2 + i * 8.4 / n, -2.35, 0], [-4.2 + (i + 1) * 8.4 / n, -2.35, 0],
                     color=color, stroke_width=6)
                for i in range(n)
            ])
            self.play(*[TransformFromCopy(edges[i], fence[i]) for i in range(n)], run_time=1.2)
            divisions = VGroup(*[Line([-4.2 + i * 8.4 / n, -2.49, 0], [-4.2 + i * 8.4 / n, -2.21, 0],
                                     color=INK, stroke_width=2) for i in range(n + 1)])
            total = self.math("K", size=29, color=K_COLOR).move_to([0, -2.82, 0])
            self.play(FadeIn(divisions), Write(total), run_time=0.5)
            self.wait(3)
            self.clear()

    def triangle_area(self):
        self.mark("Área do triângulo")
        self.header("02 / ÁREAS", "Triângulo equilátero: de onde vem a fórmula?")
        self.caption("A altura divide a base L em duas metades: L/2. Forma-se um triângulo retângulo.")
        poly = self.polygon(3, 9.6, [-4, 0.2, 0], TRI)
        points = poly.get_vertices()
        top, a, b = points
        middle = (a + b) / 2
        altitude = DashedLine(top, middle, color=INK, dash_length=0.09)
        right_angle = RightAngle(Line(middle, top), Line(middle, b), length=0.16, color=INK)
        h_label = self.math("h", size=30).move_to((top + middle) / 2 + LEFT * 0.27)
        side_label = self.math("L", size=30, color=TRI).move_to((top + b) / 2 + RIGHT * 0.26)
        halves = VGroup(*[
            self.math(r"\frac{L}{2}", size=30).move_to((middle + point) / 2 + DOWN * 0.36)
            for point in [a, b]
        ])
        self.play(Create(poly), run_time=1)
        self.play(Create(altitude), Create(right_angle), Write(h_label), Write(side_label), Write(halves), run_time=1)
        eq1 = self.math(r"h^2+\left(\frac{L}{2}\right)^2=L^2", size=36).move_to([2.3, 1.93, 0])
        eq2 = self.math(r"h=\frac{\sqrt{3}}{2}L", size=39).move_to([2.3, 0.80, 0])
        eq3 = self.math(r"A=\frac{L\cdot h}{2}", size=39).move_to([2.3, -0.35, 0])
        eq4 = self.math(r"A=\frac{L^2\sqrt{3}}{4}", size=44, color=TRI).move_to([2.3, -1.66, 0])
        self.play(Write(eq1), run_time=1.1)
        self.wait(1.5)
        self.play(TransformFromCopy(eq1, eq2), run_time=1)
        self.wait(1.5)
        self.caption("A área é base × altura / 2. Substituindo h, obtemos L²√3/4.")
        self.play(Write(eq3), run_time=0.9)
        self.wait(1)
        self.play(TransformFromCopy(eq3, eq4), run_time=1.2)
        self.play(Circumscribe(eq4, color=TRI, buff=0.18), run_time=1)
        self.wait(3)
        self.clear()

    def square_area(self):
        self.mark("Área do quadrado")
        self.header("02 / ÁREAS", "Quadrado: base vezes altura")
        self.caption("A base mede L e a altura também mede L. Por isso, A = L × L = L².")
        poly = self.polygon(4, 10.8, [-4, 0.2, 0], QUAD)
        labels = self.side_labels(poly, QUAD)
        note = self.text("base × altura", 30, MUTED).move_to([2.3, 1.65, 0])
        equation = self.math("A=L\\cdot L=L^2", size=48, color=QUAD).move_to([2.3, 0.1, 0])
        self.play(Create(poly), FadeIn(labels), FadeIn(note), run_time=1.2)
        self.play(Write(equation), run_time=1.8)
        self.wait(4)
        self.clear()

    def hexagon_area(self):
        self.mark("Área do hexágono")
        self.header("02 / ÁREAS", "O hexágono regular contém 6 triângulos equiláteros")
        self.caption("O ângulo central é 360°/6 = 60°. Com dois raios iguais, cada triângulo é equilátero.")
        center = np.array([-4.1, 0.25, 0])
        poly = self.polygon(6, 10.2, center, HEX)
        points = poly.get_vertices()
        triangles = VGroup(*[
            Polygon(center, points[i], points[(i + 1) % 6],
                    color=HEX, stroke_width=2.5, fill_color=HEX, fill_opacity=0.12 + i * 0.045)
            for i in range(6)
        ])
        self.play(Create(poly), run_time=0.9)
        self.play(LaggedStart(*[DrawBorderThenFill(t) for t in triangles], lag_ratio=0.2), run_time=2.1)
        angle = Angle(Line(center, points[0]), Line(center, points[1]), radius=0.42, color=INK)
        angle_label = self.math(r"60^\circ", size=24).move_to(center + np.array([0.73, 0.42, 0]))
        radial_label = self.math("L", size=27, color=HEX).move_to((center + points[0]) / 2 + DOWN * 0.2)
        edge_mid = (points[0] + points[1]) / 2
        edge_label = self.math("L", size=27, color=HEX).move_to(edge_mid + np.array([0.24, 0.13, 0]))
        self.play(Create(angle), Write(angle_label), Write(radial_label), Write(edge_label), run_time=0.8)
        six = self.text("6 áreas iguais", 26, HEX).move_to([-4.1, -2.0, 0])
        eq1 = self.math(r"A_{\mathrm{hex}}=6\,A_{\triangle}", size=39).move_to([2.4, 1.80, 0])
        eq2 = self.math(r"A_{\mathrm{hex}}=6\cdot\frac{L^2\sqrt{3}}{4}", size=41, color=HEX).move_to([2.4, 0.25, 0])
        eq3 = self.math(r"A_{\mathrm{hex}}=\frac{3\sqrt{3}}{2}L^2", size=40).move_to([2.4, -1.38, 0])
        self.play(Write(six), Write(eq1), run_time=1)
        self.play(Indicate(triangles[0], color=K_COLOR), run_time=1)
        self.wait(1)
        self.caption("Somamos seis áreas L²√3/4. Multiplicar por 6 produz a fórmula do hexágono.")
        self.play(TransformFromCopy(eq1, eq2), run_time=1.3)
        self.wait(2)
        self.play(TransformFromCopy(eq2, eq3), run_time=1.2)
        self.wait(3)
        self.clear()

    def substitute(self, n, name, color):
        self.mark("Substituição: " + name)
        self.header("03 / SUBSTITUIÇÃO", name + ": escrever a área em função de K")
        poly = self.polygon(n, 8.4, [-4.4, 0.70, 0], color)
        labels = self.side_labels(poly, color)
        side = self.math(rf"L=\frac{{K}}{{{n}}}", size=46, color=K_COLOR).move_to([-4.4, -1.50, 0])
        hint = self.text(f"Perímetro: {n}L = K", 23, MUTED).move_to([-4.4, -2.35, 0])
        divider = Line([-1.75, 2.25, 0], [-1.75, -2.65, 0], color=LINE, stroke_width=2)
        self.play(Create(poly), FadeIn(labels), Write(side), FadeIn(hint), Create(divider), run_time=1.2)
        if n == 3:
            formulas = [
                r"A=\frac{\sqrt{3}}{4}\cdot L^2",
                r"A=\frac{\sqrt{3}}{4}\cdot\left(\frac{K}{3}\right)^2",
                r"A=\frac{\sqrt{3}}{4}\cdot\frac{K^2}{9}",
                r"A=\frac{K^2\sqrt{3}}{36}",
            ]
            captions = [
                "Partimos da área do triângulo: A = L²√3/4.",
                "No lugar de L, colocamos K/3. A fração inteira está elevada ao quadrado.",
                "(K/3)² = K²/3² = K²/9. O denominador final é 4 × 9 = 36.",
                "Logo, a área do triângulo equilátero é K²√3/36.",
            ]
        elif n == 4:
            formulas = [
                r"A=L^2",
                r"A=\left(\frac{K}{4}\right)^2",
                r"A=\frac{K^2}{4^2}",
                r"A=\frac{K^2}{16}",
            ]
            captions = [
                "Partimos da área do quadrado: A = L².",
                "No lugar de L, colocamos K/4.",
                "Elevamos o numerador e o denominador ao quadrado: (K/4)² = K²/4².",
                "Como 4² = 16, a área do quadrado é K²/16.",
            ]
        else:
            formulas = [
                r"A=6\cdot\frac{\sqrt{3}}{4}\cdot L^2",
                r"A=6\cdot\frac{\sqrt{3}}{4}\cdot\left(\frac{K}{6}\right)^2",
                r"A=\frac{6K^2\sqrt{3}}{4\cdot36}",
                r"A=\frac{K^2\sqrt{3}}{24}",
            ]
            captions = [
                "Partimos de 6 vezes a área de um triângulo equilátero.",
                "No lugar de L, colocamos K/6. O fator 6 continua multiplicando.",
                "(K/6)² = K²/36. Depois, 4 × 36 = 144 e 6/144 = 1/24.",
                "Logo, a área do hexágono regular é K²√3/24.",
            ]
        rows = []
        for i, formula in enumerate(formulas):
            row = self.math(formula, size=42 if i == 3 else 38,
                            color=color if i == 3 else INK, max_width=7.6)
            row.move_to([2.63, 1.96 - i * 1.29, 0])
            self.caption(captions[i])
            if i == 0:
                self.play(Write(row), run_time=1)
            else:
                self.play(TransformFromCopy(rows[-1], row), run_time=1.1)
            rows.append(row)
            if i == 1:
                self.play(Circumscribe(side, color=K_COLOR, buff=0.15), run_time=0.7)
            if i == 3:
                self.play(Create(SurroundingRectangle(row, color=color, buff=0.19, corner_radius=0.12)), run_time=0.7)
            self.wait(2.4 if i in (1, 2) else 1.9)
        self.wait(1.5)
        self.clear()

    def compare(self):
        self.mark("Comparação das áreas")
        self.header("04 / COMPARAÇÃO", "O mesmo perímetro K produz áreas diferentes")
        self.caption("Os desenhos usam a mesma escala e o mesmo perímetro. L muda conforme a forma.")
        cards = VGroup()
        details = []
        choices = [
            (3, "Triângulo equilátero", TRI, r"A=\frac{K^2\sqrt{3}}{36}", r"\approx 0{,}0481\,K^2"),
            (4, "Quadrado", QUAD, r"A=\frac{K^2}{16}", r"=0{,}0625\,K^2"),
            (6, "Hexágono regular", HEX, r"A=\frac{K^2\sqrt{3}}{24}", r"\approx 0{,}0722\,K^2"),
        ]
        for x, (n, name, color, formula, decimal) in zip([-4.45, 0, 4.45], choices):
            background = RoundedRectangle(width=4.12, height=4.50, corner_radius=0.17,
                                          stroke_color=LINE, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to([x, 0.24, 0])
            title = self.text(name, 23, color, max_width=3.85).move_to([x, 2.09, 0])
            poly = self.polygon(n, 6.6, [x, 0.54, 0], color)
            equation = self.math(formula, size=35, color=color, max_width=3.8).move_to([x, -1.10, 0])
            coeff = self.math(decimal, size=29, color=MUTED, max_width=3.8).move_to([x, -1.75, 0])
            card = VGroup(background, title, poly, equation)
            cards.add(card)
            details.append(coeff)
        self.play(LaggedStart(*[FadeIn(card) for card in cards], lag_ratio=0.2), run_time=1.7)
        self.wait(2.5)
        self.play(*[Write(d) for d in details], run_time=1.2)
        order = self.math(r"A_{\triangle}<A_{\square}<A_{\mathrm{hex}}", size=40, max_width=11).move_to([0, -2.67, 0])
        self.play(Write(order), run_time=1.2)
        self.play(cards[2][0].animate.set_stroke(HEX, width=4), run_time=0.7)
        self.caption("Como K² é positivo e igual nas três fórmulas, basta comparar os coeficientes.")
        self.wait(5)
        self.clear()

        self.mark("Comparação exata")
        self.header("04 / COMPARAÇÃO", "O hexágono vence mesmo sem aproximações")
        self.caption("Como K > 0, podemos dividir por K². As desigualdades abaixo são exatas.")
        tri_label = self.text("Hexágono × triângulo", 27, TRI).move_to([-3.5, 2.13, 0])
        sq_label = self.text("Hexágono × quadrado", 27, QUAD).move_to([3.4, 2.13, 0])
        divider = Line([0, 2.30, 0], [0, -2.60, 0], color=LINE, stroke_width=2)
        lhs = VGroup(
            self.math(r"\frac{\sqrt{3}}{24}>\frac{\sqrt{3}}{36}", size=42, max_width=6).move_to([-3.5, 0.95, 0]),
            self.text("Mesmo numerador positivo:", 24, MUTED, max_width=6).move_to([-3.5, -0.30, 0]),
            self.text("o menor denominador dá a maior fração.", 23, MUTED, max_width=6).move_to([-3.5, -0.86, 0]),
        )
        rhs1 = self.math(r"\frac{\sqrt{3}}{24}>\frac{1}{16}", size=42, max_width=6).move_to([3.4, 0.95, 0])
        rhs2 = self.math(r"\Longleftrightarrow\ 2\sqrt{3}>3", size=39, max_width=6).move_to([3.4, -0.35, 0])
        rhs3 = self.math(r"(2\sqrt{3})^2=12>9=3^2", size=36, color=SUCCESS, max_width=6).move_to([3.4, -1.50, 0])
        self.play(FadeIn(tri_label), FadeIn(sq_label), Create(divider), Write(lhs[0]), Write(rhs1), run_time=1.3)
        self.play(FadeIn(lhs[1:]), Write(rhs2), run_time=1.2)
        self.wait(2)
        self.play(Write(rhs3), run_time=1.1)
        self.caption("2√3 e 3 são positivos. Comparar seus quadrados confirma que 2√3 > 3.")
        self.wait(4)
        self.clear()

    def answer(self):
        self.mark("Alternativa A")
        self.header("RESPOSTA", "O jardineiro deve escolher o hexágono regular")
        poly = self.polygon(6, 10.2, [-4.0, 0.28, 0], HEX)
        labels = self.side_labels(poly, HEX)
        side = self.math(r"L=\frac{K}{6}", size=38, color=K_COLOR).move_to([-4.0, -2.05, 0])
        answer = self.text("ALTERNATIVA A", 34, SUCCESS).move_to([2.3, 1.55, 0])
        formula = self.math(r"A=\frac{K^2\sqrt{3}}{24}", size=57, color=HEX).move_to([2.3, 0.12, 0])
        box = SurroundingRectangle(formula, color=HEX, buff=0.28, corner_radius=0.14)
        unit = self.text("Área em metros quadrados", 25, MUTED).move_to([2.3, -1.30, 0])
        self.play(Create(poly), FadeIn(labels), Write(side), FadeIn(answer), run_time=1.2)
        self.play(Write(formula), Create(box), FadeIn(unit), run_time=1.3)
        self.caption("Com K metros de cerca, o hexágono regular gera a maior área entre as três opções.")
        self.wait(7)
