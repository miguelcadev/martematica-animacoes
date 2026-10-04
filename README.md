# Martematica — Animações matemáticas

Animações que usei para produzir um vídeo de geometria para o meu canal no YouTube, **Martematica**.

## Sobre o vídeo

O vídeo começa com uma questão: qual jardim tem a maior área com o mesmo perímetro — um triângulo equilátero, um quadrado ou um hexágono regular?

Além de resolver a questão, exploro como a área de um polígono regular aumenta quando acrescentamos lados, mantendo o perímetro fixo, e se aproxima da área do círculo de mesmo perímetro.

## Tecnologias utilizadas

- **Python:** linguagem utilizada nos códigos.
- **Manim Community:** biblioteca para criar as animações e exibir as fórmulas.
- **LaTeX:** renderização das expressões matemáticas.
- **uv:** gerenciamento das dependências e execução do projeto.
- **Git e GitHub:** versionamento e compartilhamento dos arquivos.
  
Os clipes foram renderizados em **1920 × 1080, a 120 fps**.

## Principais arquivos

| Arquivo | Conteúdo |
| --- | --- |
| `perimetro_jardim.py` | Resolução da questão e comparação das áreas. |
| `areas_aproximadas.py` | Comparação usando aproximações numéricas. |
| `finalizacao_poligonos.py` | Aumento do número de lados, demonstração geral e limite do círculo. |

## Como executar

É necessário ter o uv instalado e as dependências do Manim configuradas, incluindo uma instalação de LaTeX compatível com `MathTex`.

Na pasta do projeto, instale as dependências:

```bash
uv sync
```

Depois, execute o comando do clipe que deseja gerar:

```bash
uv run manim -pqh --fps 120 perimetro_jardim.py JardimPerimetro
```

```bash
uv run manim -pqh --fps 120 areas_aproximadas.py AreasAproximadas
```

```bash
uv run manim -pqh --fps 120 finalizacao_poligonos.py MaisLadosMaiorArea
```

Os vídeos gerados ficam na pasta `media/`.

## Como o projeto foi desenvolvido


Este repositório registra esse processo e faz parte do meu aprendizado de matemática, programação e produção de vídeos.

## Observação matemática

A comparação considera polígonos regulares convexos com **o mesmo perímetro**. Essa condição é essencial para o resultado apresentado.

A finalização utiliza trigonometria, derivada e limite para demonstrar o crescimento da área e sua aproximação à área do círculo.
