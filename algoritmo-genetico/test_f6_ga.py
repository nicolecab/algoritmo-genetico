import math
import unittest

from f6_ga import (
    BITS_PER_VARIABLE,
    CHROMOSOME_BITS,
    DOMAIN_MAX,
    DOMAIN_MIN,
    decode_chromosome,
    decode_variable,
    f6,
    run_ga,
)


class F6GeneticAlgorithmTest(unittest.TestCase):
    def test_f6_has_expected_global_maximum(self):
        self.assertAlmostEqual(f6(0.0, 0.0), 1.0)
        self.assertLessEqual(f6(1.0, 1.0), 1.0)
        self.assertLessEqual(f6(100.0, 100.0), 1.0)

    def test_decode_variable_maps_binary_limits_to_domain_limits(self):
        self.assertAlmostEqual(decode_variable([0] * BITS_PER_VARIABLE), DOMAIN_MIN)
        self.assertAlmostEqual(decode_variable([1] * BITS_PER_VARIABLE), DOMAIN_MAX)

    def test_decode_chromosome_requires_44_bits(self):
        with self.assertRaises(ValueError):
            decode_chromosome(tuple([0] * (CHROMOSOME_BITS - 1)))

    def test_ga_is_reproducible_with_seed(self):
        best_a, history_a = run_ga(seed=42, generations=5)
        best_b, history_b = run_ga(seed=42, generations=5)

        self.assertEqual(best_a.chromosome, best_b.chromosome)
        self.assertEqual(
            [item.chromosome for item in history_a],
            [item.chromosome for item in history_b],
        )

    def test_ga_returns_valid_solution(self):
        best, history = run_ga(seed=7, population_size=20, generations=10)

        self.assertEqual(len(best.chromosome), CHROMOSOME_BITS)
        self.assertGreaterEqual(best.x, DOMAIN_MIN)
        self.assertLessEqual(best.x, DOMAIN_MAX)
        self.assertGreaterEqual(best.y, DOMAIN_MIN)
        self.assertLessEqual(best.y, DOMAIN_MAX)
        self.assertTrue(math.isfinite(best.fitness))
        self.assertEqual(len(history), 11)


if __name__ == "__main__":
    unittest.main()
