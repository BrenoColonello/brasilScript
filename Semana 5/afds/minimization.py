"""DFA minimization using Hopcroft's algorithm.

DFA format used here:
 - states: set of hashable state ids
 - alphabet: set of symbols
 - delta: dict mapping state -> dict(symbol -> next_state)
 - start: start state id
 - accepts: set of accepting state ids

The minimize function returns a new DFA in the same format.
"""
from typing import Set, Dict, Any, Tuple


def simulate(dfa: Dict[str, Any], s: str, alphabet=None) -> bool:
    st = dfa["start"]
    delta = dfa["delta"]
    for ch in s:
        if alphabet is not None and ch not in alphabet:
            return False
        st = delta.get(st, {}).get(ch)
        if st is None:
            return False
    return st in dfa["accepts"]


def minimize(dfa: Dict[str, Any]) -> Dict[str, Any]:
    states: Set = set(dfa["states"])  # copy
    alphabet: Set = set(dfa["alphabet"])  # copy
    delta: Dict = dfa["delta"]
    accepts: Set = set(dfa["accepts"])  # copy

    # Initialize partition: accepting and non-accepting
    P = [accepts, states - accepts]
    # Work list
    W = [accepts.copy(), (states - accepts).copy()]

    # Precompute inverse transitions: for each symbol, map target -> set(sources)
    inv = {a: {} for a in alphabet}
    for q in states:
        for a, r in delta.get(q, {}).items():
            if a not in alphabet:
                continue
            inv[a].setdefault(r, set()).add(q)

    while W:
        A = W.pop()
        for c in list(alphabet):
            # X is set of states that transition on c into A
            X = set()
            for r in A:
                X.update(inv.get(c, {}).get(r, set()))

            if not X:
                continue

            newP = []
            for Y in P:
                inter = Y & X
                diff = Y - X
                if inter and diff:
                    newP.append(inter)
                    newP.append(diff)
                    # replace Y in W accordingly
                    if Y in W:
                        W.remove(Y)
                        W.append(inter)
                        W.append(diff)
                    else:
                        # add smaller part to W
                        if len(inter) <= len(diff):
                            W.append(inter)
                        else:
                            W.append(diff)
                else:
                    newP.append(Y)
            P = newP

    # Build new states as frozenset representatives
    repr_map = {}
    new_states = set()
    for block in P:
        rep = frozenset(block)
        new_states.add(rep)
        for s in block:
            repr_map[s] = rep

    new_delta = {}
    for rep in new_states:
        # pick any member to determine transitions
        any_q = next(iter(rep))
        new_delta[rep] = {}
        for a in alphabet:
            tgt = delta.get(any_q, {}).get(a)
            if tgt is not None:
                new_delta[rep][a] = repr_map[tgt]

    new_start = repr_map[dfa["start"]]
    new_accepts = {repr_map[q] for q in accepts}

    return {
        "states": new_states,
        "alphabet": alphabet,
        "delta": new_delta,
        "start": new_start,
        "accepts": new_accepts,
    }
