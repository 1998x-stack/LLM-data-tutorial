import math
import unittest

from scripts.dedup_primitives import (
    BloomFilter,
    bloom_parameters,
    canonicalize_url,
    content_digest,
    jaccard_similarity,
    lsh_candidate_probability,
    perplexity_from_log10_score,
)


class URLCanonicalizationTests(unittest.TestCase):
    def test_host_scheme_default_port_fragment_and_tracking(self):
        self.assertEqual(
            canonicalize_url("HTTPS://EXAMPLE.COM:443/Docs?utm_source=x&id=7#top"),
            "https://example.com/Docs?id=7",
        )

    def test_path_case_is_preserved(self):
        self.assertNotEqual(
            canonicalize_url("https://example.com/Docs"),
            canonicalize_url("https://example.com/docs"),
        )

    def test_business_query_values_are_preserved(self):
        self.assertNotEqual(
            canonicalize_url("https://example.com/item?id=1"),
            canonicalize_url("https://example.com/item?id=2"),
        )

    def test_custom_tracking_parameters_are_explicit(self):
        self.assertEqual(
            canonicalize_url("https://example.com/a?ref=campaign&id=3", {"ref"}),
            "https://example.com/a?id=3",
        )

    def test_rejects_relative_urls_and_userinfo(self):
        with self.assertRaises(ValueError):
            canonicalize_url("/relative/path")
        with self.assertRaises(ValueError):
            canonicalize_url("https://user:pass@example.com/path")


class DedupMathTests(unittest.TestCase):
    def test_content_digest_is_deterministic_and_content_sensitive(self):
        self.assertEqual(content_digest("hello"), content_digest("hello"))
        self.assertNotEqual(content_digest("hello"), content_digest("hello "))

    def test_jaccard(self):
        self.assertAlmostEqual(jaccard_similarity({"a", "b", "c"}, {"b", "c", "d"}), 0.5)
        self.assertEqual(jaccard_similarity(set(), set()), 1.0)

    def test_fineweb_lsh_probabilities(self):
        self.assertAlmostEqual(lsh_candidate_probability(0.70, 14, 8), 0.56, delta=0.01)
        self.assertAlmostEqual(lsh_candidate_probability(0.75, 14, 8), 0.77, delta=0.01)
        self.assertAlmostEqual(lsh_candidate_probability(0.80, 14, 8), 0.92, delta=0.01)
        self.assertAlmostEqual(lsh_candidate_probability(0.85, 14, 8), 0.988, delta=0.002)

    def test_lsh_probability_is_monotonic(self):
        values = [lsh_candidate_probability(s, 14, 8) for s in (0.2, 0.4, 0.6, 0.8)]
        self.assertEqual(values, sorted(values))

    def test_bloom_parameters_and_no_false_negatives(self):
        bits, hashes = bloom_parameters(1000, 0.01)
        self.assertGreater(bits, 0)
        self.assertGreaterEqual(hashes, 1)
        bloom = BloomFilter(1000, 0.01)
        inserted = [f"document-{i}" for i in range(250)]
        for item in inserted:
            bloom.add(item)
        for item in inserted:
            self.assertTrue(bloom.might_contain(item))

    def test_bloom_invalid_configuration(self):
        with self.assertRaises(ValueError):
            bloom_parameters(0, 0.01)
        with self.assertRaises(ValueError):
            BloomFilter(100, 1.0)

    def test_kenlm_log10_score_to_perplexity(self):
        self.assertAlmostEqual(perplexity_from_log10_score(-6.0, 3), 100.0)
        with self.assertRaises(ValueError):
            perplexity_from_log10_score(-1.0, 0)


if __name__ == "__main__":
    unittest.main()
