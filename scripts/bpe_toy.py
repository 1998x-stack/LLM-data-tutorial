"""Deterministic character-BPE teaching implementation.

This is deliberately not GPT-2/tiktoken: it omits byte mapping, regex
pre-tokenization, Unicode normalization, special-token handling and optimized
rank-based encoding. It demonstrates weighted pair counting and merge order.
"""
from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

END_OF_WORD = "</w>"
Pair = tuple[str, str]


def merge_pair(tokens: tuple[str, ...], pair: Pair) -> tuple[str, ...]:
    merged: list[str] = []
    index = 0
    while index < len(tokens):
        if index + 1 < len(tokens) and (tokens[index], tokens[index + 1]) == pair:
            merged.append(tokens[index] + tokens[index + 1])
            index += 2
        else:
            merged.append(tokens[index])
            index += 1
    return tuple(merged)


def train_bpe(words: Iterable[str], num_merges: int) -> list[Pair]:
    if isinstance(num_merges, bool) or not isinstance(num_merges, int) or num_merges < 0:
        raise ValueError("num_merges must be a non-negative integer")
    word_list = list(words)
    if any(not isinstance(word, str) or not word for word in word_list):
        raise ValueError("words must be non-empty strings")
    vocab = Counter(tuple(list(word) + [END_OF_WORD]) for word in word_list)
    merges: list[Pair] = []
    for _ in range(num_merges):
        pair_counts: Counter[Pair] = Counter()
        for tokens, frequency in vocab.items():
            for pair in zip(tokens, tokens[1:]):
                pair_counts[pair] += frequency
        if not pair_counts:
            break
        best_pair = max(pair_counts, key=lambda pair: (pair_counts[pair], pair))
        merges.append(best_pair)
        updated: Counter[tuple[str, ...]] = Counter()
        for tokens, frequency in vocab.items():
            updated[merge_pair(tokens, best_pair)] += frequency
        vocab = updated
    return merges


def encode_word(word: str, merges: Iterable[Pair]) -> tuple[str, ...]:
    if not isinstance(word, str) or not word:
        raise ValueError("word must be a non-empty string")
    tokens = tuple(list(word) + [END_OF_WORD])
    for pair in merges:
        tokens = merge_pair(tokens, pair)
    return tokens
