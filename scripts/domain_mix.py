"""Token-exposure planning for two-source continual pretraining mixtures."""


def token_exposure(total_tokens: int, domain_share: float) -> dict[str, int | float]:
    """Split a target token budget into domain and general replay exposure."""
    if isinstance(total_tokens, bool) or not isinstance(total_tokens, int) or total_tokens < 0:
        raise ValueError("total_tokens must be a non-negative integer")
    share = float(domain_share)
    if not 0.0 <= share <= 1.0:
        raise ValueError("domain_share must be between 0 and 1")
    domain = total_tokens * share
    general = total_tokens - domain
    return {
        "total_tokens": total_tokens,
        "domain_share": share,
        "domain_tokens": domain,
        "general_tokens": general,
    }
