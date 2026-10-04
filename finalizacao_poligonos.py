"""Finalização: mais lados, maior área, com perímetro fixo.

Renderização:
    uv run manim -pqh --fps 120 finalizacao_poligonos.py MaisLadosMaiorArea

Vídeo em português, sem narração. Requer Manim Community e LaTeX.
Inclui uma demonstração geral com a fórmula do polígono e uma derivada.
Todas as figuras da primeira cena são regulares e têm o mesmo perímetro.
As trocas usam fades: não se interpolam polígonos irregulares entre os casos.
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
MINT = "#54D4BC"
PURPLE = "#AC9BFA"
GOLD = "#FFE28B"
SUCCESS = "#72E0AA"
FONT = next((name for name in ("DejaVu Sans", "Arial", "Liberation Sans") if name in list_fonts()), "")
PERIMETRO_EXEMPLO = 12.0


class MaisLadosMaiorArea(Scene):
    def text(self, value, size=28, color=INK, max_width=12.6):
        mob = Text(value, font=FONT, font_size=size, color=color)
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        return mob

    def math(self, *values, size=40, color=INK, max_width=7.4):
        mob = MathTex(*values, font_size=size, color=color)
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        return mob

    def mark(self, name):
        self.timeline.append({"name": name, "time": float(self.renderer.time)})

    def header(self, step, title):
        label = self.text(step, 16, MUTED).move_to([-6.4, 3.7, 0], aligned_edge=LEFT)
        title_mob = self.text(title, 33).move_to([0, 3.18, 0])
        line = Line([-6.4, 2.78, 0], [6.4, 2.78, 0], color=LINE, stroke_width=2)
        self.add(label, title_mob, line)

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
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.clear()
        self.caption_mob = None

    def polygon(self, n, perimeter, center, color=MINT):
        radius = perimeter / (2 * n * np.sin(PI / n))
        start = PI / 2 if n == 3 else PI / 4 if n == 4 else 0
        points = [np.array(center) + radius * np.array([
            np.cos(start + i * TAU / n), np.sin(start + i * TAU / n), 0
        ]) for i in range(n)]
        return Polygon(*points, color=color, stroke_width=4,
                       fill_color=color, fill_opacity=0.18)

    @staticmethod
    def area(n, perimeter=PERIMETRO_EXEMPLO):
        return perimeter ** 2 / (4 * n * np.tan(PI / n))

    def construct(self):
        self.camera.background_color = BG
        self.caption_mob = None
        self.timeline = []
        self.visual_sequence()
        self.general_formula()
        self.monotonicity()
        self.conclusion()
        self.circle_limit()
        self.mark("Fim")
        timeline_path = os.environ.get("MANIM_TIMELINE")
        if timeline_path:
            Path(timeline_path).write_text(json.dumps(self.timeline, ensure_ascii=False, indent=2), encoding="utf-8")

    def visual_sequence(self):
        self.mark("Mesmo perímetro, mais lados")
        self.header("FINALIZAÇÃO / POLÍGONOS REGULARES CONVEXOS", "Mais lados. Mesma cerca. Maior área.")
        center = np.array([-3.95, 0.25, 0])
        world_perimeter = 10.2
        reference = DashedVMobject(Circle(radius=world_perimeter / TAU, color=PURPLE,
                                         stroke_width=2).move_to(center), num_dashes=70)
        reference_label = self.text("Círculo de mesmo perímetro", 22, PURPLE,
                                    max_width=4.7).move_to([-3.95, -2.06, 0])
        bg = RoundedRectangle(width=6.25, height=4.5, corner_radius=0.16,
                              stroke_color=LINE, fill_color=PANEL, fill_opacity=1).move_to([2.5, -0.08, 0])
        fixed = self.math(r"K=12\ \mathrm{m}\quad\text{(sempre)}", size=33, color=GOLD).move_to([2.5, 2.37, 0])
        area_label = self.text("Área do polígono", 25, MUTED).move_to([2.5, 0.65, 0])
        bar_bg = RoundedRectangle(width=5.1, height=0.19, corner_radius=0.06,
                                  stroke_width=0, fill_color=LINE, fill_opacity=1).move_to([2.5, -1.2, 0])
        self.add(bg, fixed, area_label, bar_bg, reference, reference_label)
        self.caption("Cada figura tem exatamente 12 m de perímetro.",
                     "Os números ilustram o padrão. Em seguida, vamos demonstrá-lo para todo n ≥ 3.")

        def metrics(n):
            area = self.area(n)
            fraction = PI / (n * np.tan(PI / n))
            count = self.math(rf"n={n}\ \text{{lados}}", size=42, color=MINT).move_to([2.5, 1.52, 0])
            number = self.math(rf"A\approx{area:.4f}\ \mathrm{{m}}^2".replace('.', '{,}'),
                               size=44, color=MINT, max_width=5.7).move_to([2.5, -0.26, 0])
            percentage = self.text(f"{100 * fraction:.2f}% da área do círculo".replace('.', ','),
                                   24, MUTED, max_width=5.7).move_to([2.5, -1.84, 0])
            bar = RoundedRectangle(width=5.1 * fraction, height=0.19, corner_radius=0.06,
                                   stroke_width=0, fill_color=MINT, fill_opacity=1)
            bar.move_to(bar_bg.get_left(), aligned_edge=LEFT)
            return VGroup(count, number, percentage), bar

        poly = self.polygon(3, world_perimeter, center)
        info, bar = metrics(3)
        self.play(Create(poly), FadeIn(info), FadeIn(bar), run_time=1.1)
        self.wait(2.1)
        for n in [4, 5, 6, 8, 12, 24, 48, 96]:
            new_poly = self.polygon(n, world_perimeter, center)
            new_info, new_bar = metrics(n)
            self.play(FadeOut(poly), FadeIn(new_poly), FadeOut(info), FadeIn(new_info),
                      Transform(bar, new_bar), run_time=0.7)
            poly, info = new_poly, new_info
            self.wait(1.5 if n in (4, 6, 96) else 0.8)
        self.wait(1.4)
        self.wipe()

    def general_formula(self):
        self.mark("Fórmula geral da área")
        self.header("01 / GEOMETRIA", "Dividimos o polígono em n triângulos iguais")
        center = np.array([-4.05, 0.18, 0])
        poly = self.polygon(8, 9.8, center)
        vertices = poly.get_vertices()
        mid = (vertices[0] + vertices[1]) / 2
        rays = VGroup(*[Line(center, vertex, color=LINE, stroke_width=2) for vertex in vertices])
        chosen = Polygon(center, vertices[0], vertices[1], color=MINT,
                         fill_color=MINT, fill_opacity=0.28, stroke_width=3)
        apothem = DashedLine(center, mid, color=GOLD, stroke_width=3, dash_length=0.07)
        right = RightAngle(Line(mid, center), Line(mid, vertices[0]), length=0.16, color=INK)
        angle = Angle(Line(center, vertices[0]), Line(center, mid), radius=0.50, color=INK)
        theta = self.math(r"\theta", size=27).move_to(center + np.array([0.74, 0.15, 0]))
        height = self.math(r"a_n", size=28, color=GOLD).move_to((center + mid) / 2 + np.array([-0.18, 0.22, 0]))
        half = self.math(r"\frac{L}{2}", size=26).move_to((mid + vertices[0]) / 2 + RIGHT * 0.25)
        theta_eq = self.math(r"\theta=\frac{\pi}{n}", size=35, color=GOLD).move_to([-4.05, -2.06, 0])
        note = self.text("aₙ é o apótema: a altura do triângulo", 21, MUTED,
                         max_width=4.9).move_to([-4.05, -2.68, 0])
        divider = Line([-1.45, 2.35, 0], [-1.45, -2.77, 0], color=LINE, stroke_width=2)
        self.caption("Cada triângulo tem base L e altura aₙ.",
                     "Metade do ângulo central mede π/n, em radianos.")
        self.play(Create(poly), Create(rays), FadeIn(chosen), Create(divider), run_time=1.1)
        self.play(Create(apothem), Create(right), Create(angle), Write(theta), Write(height),
                  Write(half), Write(theta_eq), FadeIn(note), run_time=1.2)
        values = [r"L=\frac{K}{n}",
                  r"A_n=n\,\frac{L\,a_n}{2}=\frac{K\,a_n}{2}",
                  r"\tan\!\left(\frac{\pi}{n}\right)=\frac{L}{2a_n}",
                  r"a_n=\frac{K}{2n\tan(\pi/n)}",
                  r"A_n=\frac{K^2}{4n\tan(\pi/n)}"]
        for i, value in enumerate(values):
            eq = self.math(value, size=40 if i == 4 else 35,
                           color=MINT if i == 4 else INK, max_width=7.4).move_to([2.63, 2.20 - 1.09 * i, 0])
            self.play(Write(eq), run_time=1)
            if i == 4:
                self.play(Create(SurroundingRectangle(eq, color=MINT, buff=0.16,
                                                      corner_radius=0.10)), run_time=0.7)
            self.wait(3 if i == 4 else 1.7)
        self.wipe()

    def monotonicity(self):
        self.mark("Demonstração geral com derivada")
        self.header("02 / DEMONSTRAÇÃO GERAL — DERIVADA", "Por que a área aumenta para todo n ≥ 3?")
        x = self.math(r"x=\frac{\pi}{n},\qquad 0<x\leq\frac{\pi}{3}", size=38,
                      max_width=11.8).move_to([0, 2.10, 0])
        area = self.math(r"A_n=", r"\frac{K^2}{4\pi}\cdot", r"\frac{x}{\tan x}",
                         size=45, max_width=11.8).move_to([0, 0.89, 0])
        area[1].set_color(GOLD)
        f = self.math(r"f(x)=\frac{x}{\tan x}", size=39, color=MINT).move_to([0, -0.37, 0])
        derivative = self.math(r"f'(x)=\frac{\sin x\cos x-x}{\sin^2x}<0", size=39,
                               color=SUCCESS, max_width=11.8).move_to([0, -1.69, 0])
        reason = self.math(r"\sin x\cos x=\frac{\sin(2x)}{2}<x", size=31,
                           color=MUTED, max_width=11.8).move_to([0, -2.72, 0])
        self.caption("Substituímos π/n por x. O fator K²/(4π) é constante e positivo.")
        self.play(Write(x), run_time=1)
        self.play(Write(area), run_time=1.1)
        self.wait(3)
        self.play(Write(f), run_time=1)
        self.wait(2)
        self.play(Write(derivative), run_time=1.2)
        self.caption("A derivada negativa indica que f diminui quando x aumenta.")
        self.wait(3)
        self.play(Write(reason), run_time=1.2)
        self.caption("Usamos sin(t) < t para t > 0, com o ângulo em radianos.",
                     "Assim, o numerador da derivada é negativo e o denominador é positivo.")
        self.wait(4)
        self.wipe()

    def conclusion(self):
        self.mark("Mais lados implica maior área")
        self.header("03 / CONCLUSÃO", "Quando n aumenta, x diminui e a área cresce")
        first = self.math(r"n\uparrow\quad\Longrightarrow\quad x=\frac{\pi}{n}\downarrow",
                          size=49, color=GOLD, max_width=11.8).move_to([0, 1.75, 0])
        second = self.math(r"x\downarrow\quad\Longrightarrow\quad f(x)=\frac{x}{\tan x}\uparrow",
                           size=45, color=MINT, max_width=11.8).move_to([0, 0.10, 0])
        third = self.math(r"\boxed{A_{n+1}>A_n\quad(n\geq3)}", size=49,
                          color=SUCCESS, max_width=11.8).move_to([0, -1.70, 0])
        self.caption("Como f é decrescente, diminuir x faz f aumentar.",
                     "Multiplicar por K²/(4π), que é positivo, preserva esse aumento.")
        self.play(Write(first), run_time=1.1)
        self.wait(1.5)
        self.play(Write(second), run_time=1.1)
        self.wait(2)
        self.play(Write(third), run_time=1.3)
        self.wait(4)
        self.wipe()

    def circle_limit(self):
        self.mark("Limite: o círculo")
        self.header("04 / LIMITE", "A área se aproxima da área do círculo")
        center = np.array([-4.0, 0.30, 0])
        radius = 10.2 / TAU
        poly = self.polygon(96, 10.2, center)
        circle = Circle(radius=radius, color=PURPLE, fill_color=PURPLE,
                        fill_opacity=0.18, stroke_width=4).move_to(center)
        label = self.text("Mesmo perímetro K", 27, GOLD).move_to([-4.0, -1.91, 0])
        self.add(poly, label)
        self.caption("O número de lados cresce sem limite. Nenhum polígono finito é um círculo.")
        eq1 = self.math(r"n\to\infty\quad\Longrightarrow\quad x=\frac{\pi}{n}\to0",
                        size=37, max_width=7.7).move_to([2.44, 1.80, 0])
        eq2 = self.math(r"\frac{x}{\tan x}\to1", size=43).move_to([2.44, 0.39, 0])
        eq3 = self.math(r"A_n\longrightarrow\frac{K^2}{4\pi}=A_{\mathrm{c\acute irculo}}",
                        size=40, color=PURPLE, max_width=7.7).move_to([2.44, -1.07, 0])
        example = self.math(r"K=12\ \mathrm{m}\quad\Rightarrow\quad A\approx11{,}4592\ \mathrm{m}^2",
                            size=29, color=MUTED, max_width=7.7).move_to([2.44, -2.34, 0])
        self.play(Write(eq1), run_time=1.1)
        self.play(FadeOut(poly), FadeIn(circle), Write(eq2), run_time=1.3)
        self.wait(2)
        self.play(Write(eq3), run_time=1.2)
        self.play(Write(example), run_time=1)
        self.caption("A quantidade de cerca não mudou. A forma foi se aproximando de um círculo.",
                     "Perímetro fixo + mais lados, em polígonos regulares, significa maior área.")
        self.wait(6)
