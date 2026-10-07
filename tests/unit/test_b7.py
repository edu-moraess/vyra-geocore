"""Unit tests for GATE 2 deterministic B7 sampling."""

from vyra_geocore.datasets.b7 import (
    B7_DEFAULT_PER_CLASS,
    B7_SEED,
    B7_SPECIAL_CLASS_ID,
    B7_SPECIAL_SAMPLES,
    B7_TOTAL,
    sample_b7,
    target_count,
)


def test_seed_constant():
    assert B7_SEED == 17082026


def test_total_constant():
    assert B7_TOTAL == 600


def test_target_class_22():
    assert target_count(22) == 40
    assert target_count(B7_SPECIAL_CLASS_ID) == B7_SPECIAL_SAMPLES


def test_target_other_classes():
    for cid in range(1, 30):
        if cid == 22:
            continue
        assert target_count(cid) == B7_DEFAULT_PER_CLASS


def _fake_universe(n_per_class: int = 50):
    by_class = {}
    for cid in range(1, 30):
        rows = []
        for i in range(n_per_class):
            rows.append({
                "class_id": str(cid),
                "class_short_name": f"C{cid}",
                "image_id": str(i),
                "pixel_purity_value": "90",
                "ghm_value": "1",
                "latitude": str(cid + i * 0.001),
                "longitude": str(i * 0.001),
                "country_code": "XX",
                "admin_level1": "",
                "admin_level2": "",
                "locality": "L",
                "number_of_s2_images": "1",
            })
        by_class[cid] = rows
    return by_class


def test_sample_size_and_distribution():
    from collections import Counter
    selected = sample_b7(_fake_universe(50), seed=B7_SEED)
    assert len(selected) == 600
    counts = Counter(int(float(r["class_id"])) for r in selected)
    assert counts[22] == 40
    for cid in range(1, 30):
        if cid != 22:
            assert counts[cid] == 20


def test_no_duplicates():
    selected = sample_b7(_fake_universe(50), seed=B7_SEED)
    keys = [(r["class_id"], r["image_id"], r["latitude"], r["longitude"]) for r in selected]
    assert len(keys) == len(set(keys))


def test_determinism():
    by_class = _fake_universe(50)
    assert sample_b7(by_class, seed=B7_SEED) == sample_b7(by_class, seed=B7_SEED)


def test_canonical_ordering():
    selected = sample_b7(_fake_universe(50), seed=B7_SEED)
    keys = [(int(float(r["class_id"])), r["image_id"], r["latitude"], r["longitude"]) for r in selected]
    assert keys == sorted(keys)


def test_without_replacement_raises_if_insufficient():
    try:
        sample_b7(_fake_universe(10), seed=B7_SEED)
        assert False, "should have raised"
    except ValueError:
        pass
