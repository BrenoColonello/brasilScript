"""Tests for DFA minimization using example DFAs."""
from afds.minimization import minimize, simulate
from afds.example_dfas import DFA_ID, DFA_NUM


def enumerate_samples_id():
    return ["a", "abc", "a1_2", "1abc", "_"]


def enumerate_samples_num():
    return ["0", "123", "3.14", "12.", ".5"]


def test_minimize_id_preserves():
    m = minimize(DFA_ID)
    for s in enumerate_samples_id():
        assert simulate(DFA_ID, s) == simulate(m, s)


def test_minimize_num_preserves():
    m = minimize(DFA_NUM)
    for s in enumerate_samples_num():
        assert simulate(DFA_NUM, s) == simulate(m, s)


def test_minimization_reduces_states():
    m = minimize(DFA_NUM)
    assert len(m["states"]) <= len(DFA_NUM["states"])


if __name__ == '__main__':
    test_minimize_id_preserves()
    test_minimize_num_preserves()
    test_minimization_reduces_states()
    print('Minimization tests passed')
