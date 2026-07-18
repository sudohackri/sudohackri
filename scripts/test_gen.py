"""Tests ligeros (sin pytest): ejecutar con
   ../.venv/bin/python -c "import test_gen as t; t.run()"
"""
from gen_portrait import RAMP, brightness_to_char
from gen_heatmap import count_to_level


def test_ramp_extremes():
    assert brightness_to_char(0) == RAMP[0]
    assert brightness_to_char(255) == RAMP[-1]


def test_ramp_monotonic():
    chars = [brightness_to_char(v) for v in range(0, 256, 16)]
    idxs = [RAMP.index(c) for c in chars]
    assert idxs == sorted(idxs)


def test_levels():
    assert count_to_level(0) == 0
    assert count_to_level(1) >= 1
    assert count_to_level(999) == 4


def run():
    test_ramp_extremes()
    test_ramp_monotonic()
    test_levels()
    print("ok")


if __name__ == "__main__":
    run()
