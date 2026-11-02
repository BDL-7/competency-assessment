"""Deterministic integrity metadata for content-free synthetic artifacts."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping


def synthetic_artifact_hash(metadata: Mapping[str, object]) -> str:
    """Hash canonical public-safe metadata without creating artifact bytes."""

    encoded = json.dumps(
        dict(metadata), sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
