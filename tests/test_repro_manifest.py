import unittest

from scripts.repro_manifest import canonical_json_digest, dataset_root_digest


class ReproManifestTests(unittest.TestCase):
    def test_canonical_json_ignores_key_order(self):
        self.assertEqual(canonical_json_digest({"a": 1, "b": 2}), canonical_json_digest({"b": 2, "a": 1}))

    def test_unicode_is_stable(self):
        self.assertEqual(canonical_json_digest({"text": "语料"}), canonical_json_digest({"text": "语料"}))

    def test_dataset_digest_ignores_shard_input_order(self):
        a = {"path": "shards/a.parquet", "sha256": "a" * 64, "rows": 10}
        b = {"path": "shards/b.parquet", "sha256": "b" * 64, "rows": 20}
        self.assertEqual(dataset_root_digest([a, b]), dataset_root_digest([b, a]))

    def test_dataset_digest_changes_when_content_changes(self):
        a = {"path": "shards/a.parquet", "sha256": "a" * 64, "rows": 10}
        b = {"path": "shards/a.parquet", "sha256": "b" * 64, "rows": 10}
        self.assertNotEqual(dataset_root_digest([a]), dataset_root_digest([b]))

    def test_rejects_duplicate_and_unsafe_paths(self):
        item = {"path": "shards/a.parquet", "sha256": "a" * 64, "rows": 10}
        with self.assertRaises(ValueError):
            dataset_root_digest([item, item])
        with self.assertRaises(ValueError):
            dataset_root_digest([{**item, "path": "../outside.parquet"}])
        for unsafe_path in ("..\\outside.parquet", "shards\\part.parquet", "C:/data/part.parquet", "//server/share/part.parquet", "shards/part\x00.parquet"):
            with self.subTest(path=unsafe_path), self.assertRaises(ValueError):
                dataset_root_digest([{**item, "path": unsafe_path}])

    def test_rejects_bad_checksums_and_row_counts(self):
        item = {"path": "shards/a.parquet", "sha256": "not-a-sha", "rows": 10}
        with self.assertRaises(ValueError):
            dataset_root_digest([item])
        item = {"path": "shards/a.parquet", "sha256": "a" * 64, "rows": -1}
        with self.assertRaises(ValueError):
            dataset_root_digest([item])


if __name__ == "__main__":
    unittest.main()
