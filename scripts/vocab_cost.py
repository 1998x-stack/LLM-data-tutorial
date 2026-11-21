"""Vocabulary-matrix parameter and weight-memory estimates."""
from __future__ import annotations


def vocabulary_parameter_count(vocab_size: int, hidden_size: int, tied_embeddings: bool) -> int:
    if isinstance(vocab_size, bool) or not isinstance(vocab_size, int) or vocab_size <= 0:
        raise ValueError("vocab_size must be a positive integer")
    if isinstance(hidden_size, bool) or not isinstance(hidden_size, int) or hidden_size <= 0:
        raise ValueError("hidden_size must be a positive integer")
    # Input embedding always contributes V*d; an untied output head adds V*d.
    return vocab_size * hidden_size * (1 if tied_embeddings else 2)


def vocabulary_weight_bytes(
    vocab_size: int,
    hidden_size: int,
    bytes_per_parameter: int,
    tied_embeddings: bool,
) -> int:
    if isinstance(bytes_per_parameter, bool) or not isinstance(bytes_per_parameter, int) or bytes_per_parameter <= 0:
        raise ValueError("bytes_per_parameter must be a positive integer")
    return vocabulary_parameter_count(vocab_size, hidden_size, tied_embeddings) * bytes_per_parameter


def logits_elements(batch_size: int, sequence_length: int, vocab_size: int) -> int:
    for name, value in (("batch_size", batch_size), ("sequence_length", sequence_length), ("vocab_size", vocab_size)):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer")
    return batch_size * sequence_length * vocab_size
