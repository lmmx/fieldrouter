from pytest import importorskip


def test_simple():
    importorskip("examples.simple")


def test_nested():
    importorskip("examples.nested")


def test_reference():
    importorskip("examples.reference")