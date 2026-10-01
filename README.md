# Algoritmo genético para maximização da função F6

Implementação em Python de um algoritmo genético binário para encontrar o
máximo global da função F6 de Schaffer:

```text
F6(x, y) = 0.5 - ((sin(sqrt(x² + y²))² - 0.5) / (1 + 0.001(x² + y²))²)
```

A função possui máximo global em `F6(0, 0) = 1`.

## Como funciona

Cada solução é representada por um cromossomo binário de 44 bits: 22 bits
codificam `x` e 22 bits codificam `y`, ambos no intervalo `[-100, 100]`.

A cada geração, o algoritmo aplica:

- seleção por roleta;
- crossover de um ponto;
- mutação por inversão de bit;
- elitismo para preservar a melhor solução encontrada.

Por padrão, são utilizados 100 indivíduos durante 40 gerações, com taxa de
crossover de `0.65` e taxa de mutação de `0.008`.

## Requisitos

- Python 3.10 ou superior
- nenhuma dependência externa

## Execução

Execute com os parâmetros padrão:

```bash
python3 f6_ga.py
```

Para obter uma execução reproduzível, informe uma semente:

```bash
python3 f6_ga.py --seed 42
```

Use `--verbose` para exibir a melhor solução de cada geração:

```bash
python3 f6_ga.py --seed 42 --verbose
```

Os principais parâmetros também podem ser ajustados pela linha de comando:

```bash
python3 f6_ga.py \
  --population-size 100 \
  --generations 80 \
  --crossover-rate 0.65 \
  --mutation-rate 0.008
```

Para consultar todas as opções disponíveis:

```bash
python3 f6_ga.py --help
```
