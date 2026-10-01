#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import random
from typing import Iterable
from dataclasses import dataclass


BITS_PER_VARIABLE = 22
CHROMOSOME_BITS = BITS_PER_VARIABLE * 2
DOMAIN_MIN = -100.0
DOMAIN_MAX = 100.0


@dataclass(frozen=True)
class Individual:
    chromosome: tuple[int, ...]
    x: float
    y: float
    fitness: float


def f6(x: float, y: float) -> float:
    radius = math.sqrt((x * x) + (y * y))
    numerator = (math.sin(radius) ** 2) - 0.5
    denominator = (1.0 + (0.001 * ((x * x) + (y * y)))) ** 2
    return 0.5 - (numerator / denominator)


def bits_to_int(bits: Iterable[int]) -> int:
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def decode_variable(bits: Iterable[int]) -> float:
    integer_value = bits_to_int(bits)
    max_integer = (2**BITS_PER_VARIABLE) - 1
    return DOMAIN_MIN + (integer_value * (DOMAIN_MAX - DOMAIN_MIN) / max_integer)


def decode_chromosome(chromosome: tuple[int, ...]) -> tuple[float, float]:
    if len(chromosome) != CHROMOSOME_BITS:
        raise ValueError(f"Chromossomo deve ter {CHROMOSOME_BITS} bits.")
    x_bits = chromosome[:BITS_PER_VARIABLE]
    y_bits = chromosome[BITS_PER_VARIABLE:]
    return decode_variable(x_bits), decode_variable(y_bits)


def evaluate(chromosome: tuple[int, ...]) -> Individual:
    x, y = decode_chromosome(chromosome)
    return Individual(chromosome=chromosome, x=x, y=y, fitness=f6(x, y))


def random_chromosome(rng: random.Random) -> tuple[int, ...]:
    return tuple(rng.randint(0, 1) for _ in range(CHROMOSOME_BITS))


def initial_population(size: int, rng: random.Random) -> list[Individual]:
    return [evaluate(random_chromosome(rng)) for _ in range(size)]


def roulette_selection(population: list[Individual], rng: random.Random) -> Individual:
    total_fitness = sum(individual.fitness for individual in population)
    if total_fitness <= 0:
        return rng.choice(population)
    target = rng.uniform(0.0, total_fitness)
    accumulated = 0.0
    for individual in population:
        accumulated += individual.fitness
        if accumulated >= target:
            return individual
    return population[-1]


def crossover(
    parent_a: tuple[int, ...],
    parent_b: tuple[int, ...],
    crossover_rate: float,
    rng: random.Random,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if rng.random() > crossover_rate:
        return parent_a, parent_b
    cut = rng.randint(1, CHROMOSOME_BITS - 1)
    child_a = parent_a[:cut] + parent_b[cut:]
    child_b = parent_b[:cut] + parent_a[cut:]
    return child_a, child_b


def mutate(
    chromosome: tuple[int, ...],
    mutation_rate: float,
    rng: random.Random,
) -> tuple[int, ...]:
    return tuple(1 - bit if rng.random() < mutation_rate else bit for bit in chromosome)


def next_generation(
    population: list[Individual],
    crossover_rate: float,
    mutation_rate: float,
    rng: random.Random,
    elitism: bool,
) -> list[Individual]:
    new_population: list[Individual] = []
    if elitism:
        new_population.append(max(population, key=lambda individual: individual.fitness))
    while len(new_population) < len(population):
        parent_a = roulette_selection(population, rng)
        parent_b = roulette_selection(population, rng)
        child_a, child_b = crossover(
            parent_a.chromosome,
            parent_b.chromosome,
            crossover_rate,
            rng,
        )
        new_population.append(evaluate(mutate(child_a, mutation_rate, rng)))
        if len(new_population) < len(population):
            new_population.append(evaluate(mutate(child_b, mutation_rate, rng)))
    return new_population


def run_ga(
    population_size: int = 100,
    generations: int = 40,
    crossover_rate: float = 0.65,
    mutation_rate: float = 0.008,
    seed: int | None = None,
    elitism: bool = True,
) -> tuple[Individual, list[Individual]]:
    if population_size < 2:
        raise ValueError("O tamanho da populacao deve ser pelo menos 2.")
    if generations < 1:
        raise ValueError("O numero de geracoes deve ser pelo menos 1.")
    if not 0 <= crossover_rate <= 1:
        raise ValueError("A taxa de crossover deve estar entre 0 e 1.")
    if not 0 <= mutation_rate <= 1:
        raise ValueError("A taxa de mutacao deve estar entre 0 e 1.")
    rng = random.Random(seed)
    population = initial_population(population_size, rng)
    history = [max(population, key=lambda individual: individual.fitness)]
    for _ in range(generations):
        population = next_generation(
            population,
            crossover_rate=crossover_rate,
            mutation_rate=mutation_rate,
            rng=rng,
            elitism=elitism,
        )
        history.append(max(population, key=lambda individual: individual.fitness))
    return max(history, key=lambda individual: individual.fitness), history


def chromosome_as_string(chromosome: tuple[int, ...]) -> str:
    return "".join(str(bit) for bit in chromosome)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Maximiza a funcao F6 com algoritmo genetico binario.",
    )
    parser.add_argument("--population-size", type=int, default=100)
    parser.add_argument("--generations", type=int, default=40)
    parser.add_argument("--crossover-rate", type=float, default=0.65)
    parser.add_argument("--mutation-rate", type=float, default=0.008)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--no-elitism", action="store_true")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Mostra o melhor individuo a cada geracao.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    best, history = run_ga(
        population_size=args.population_size,
        generations=args.generations,
        crossover_rate=args.crossover_rate,
        mutation_rate=args.mutation_rate,
        seed=args.seed,
        elitism=not args.no_elitism,
    )
    if args.verbose:
        for generation, individual in enumerate(history):
            print(
                f"geracao={generation:03d} "
                f"fitness={individual.fitness:.8f} "
                f"x={individual.x:.8f} "
                f"y={individual.y:.8f} "
                f"cromossomo={chromosome_as_string(individual.chromosome)}"
            )
    print("Melhor solucao encontrada")
    print(f"F6(x, y): {best.fitness:.10f}")
    print(f"x: {best.x:.10f}")
    print(f"y: {best.y:.10f}")
    print(f"cromossomo: {chromosome_as_string(best.chromosome)}")


if __name__ == "__main__":
    main()
