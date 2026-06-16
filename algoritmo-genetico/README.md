# Algoritmo Genetico para maximizar F6

Implementacao em Python do Algoritmo Genetico pedido nos slides para maximizar a
funcao F6 de Schaffer:

```text
F6(x,y) = 0.5 - ((sin(sqrt(x^2 + y^2))^2 - 0.5) / (1 + 0.001(x^2 + y^2))^2)
```

O maximo global e `F6(0,0) = 1`.

## Configuracao usada

- Representacao binaria com 44 bits
- 22 bits para `x` e 22 bits para `y`
- Dominio de `x,y`: `[-100, 100]`
- Populacao inicial aleatoria
- Selecao por roleta
- Crossover de 1 ponto
- Mutacao por inversao de bit
- Elitismo preservando o melhor individuo
- Populacao padrao: 100 individuos
- Geracoes padrao: 40
- Taxa de crossover padrao: 0.65
- Taxa de mutacao padrao: 0.008

## Como executar

```bash
python3 f6_ga.py
```

Execucao reproduzivel com semente:

```bash
python3 f6_ga.py --seed 42
```

Mostrar o melhor individuo por geracao:

```bash
python3 f6_ga.py --seed 42 --verbose
```

Ajustar os parametros:

```bash
python3 f6_ga.py --population-size 100 --generations 80 --crossover-rate 0.65 --mutation-rate 0.008
```