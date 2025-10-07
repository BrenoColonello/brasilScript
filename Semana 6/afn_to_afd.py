"""Subset construction: convert AFN (NFA with epsilons) to AFD (DFA).

Same implementation as the project src version, adapted to sit inside `Semana 6`.
"""
from typing import Dict, Set, Any, Tuple, List, FrozenSet


def epsilon_closure(states: Set[Any], delta: Dict) -> Set[Any]:
    stack = list(states)
    closure = set(states)
    while stack:
        s = stack.pop()
        for nxt in delta.get(s, {}).get(None, set()):
            if nxt not in closure:
                closure.add(nxt)
                stack.append(nxt)
    return closure


def move(states: Set[Any], symbol: str, delta: Dict) -> Set[Any]:
    res = set()
    for s in states:
        for tgt in delta.get(s, {}).get(symbol, set()):
            res.add(tgt)
    return res


def nfa_to_dfa(nfa: Dict[str, Any], token_priority: List[str]) -> Dict[str, Any]:
    delta = nfa["delta"]
    alphabet = set(nfa["alphabet"]) - {None}
    start_closure = frozenset(epsilon_closure({nfa["start"]}, delta))

    unmarked = [start_closure]
    dstates: List[FrozenSet[Any]] = [start_closure]
    ddelta: Dict[FrozenSet[Any], Dict[str, FrozenSet[Any]]] = {}
    daccepts: Dict[FrozenSet[Any], str] = {}

    def choose_token(dstate: FrozenSet[Any]) -> str:
        found = []
        for s in dstate:
            if s in nfa.get("accepts", {}):
                found.append(nfa["accepts"][s])
        for t in token_priority:
            if t in found:
                return t
        return None

    while unmarked:
        T = unmarked.pop()
        ddelta[T] = {}
        tok = choose_token(T)
        if tok is not None:
            daccepts[T] = tok

        for a in alphabet:
            U = epsilon_closure(move(set(T), a, delta), delta)
            if not U:
                continue
            Uf = frozenset(U)
            ddelta[T][a] = Uf
            if Uf not in dstates:
                dstates.append(Uf)
                unmarked.append(Uf)

    state_ids = {s: f"S{idx}" for idx, s in enumerate(dstates)}
    dfa_states = set(state_ids.values())
    dfa_delta = {state_ids[s]: {a: state_ids[t] for a, t in ddelta.get(s, {}).items()} for s in dstates}
    dfa_start = state_ids[start_closure]
    dfa_accepts = {state_ids[s]: daccepts[s] for s in daccepts}

    return {
        "states": dfa_states,
        "alphabet": alphabet,
        "delta": dfa_delta,
        "start": dfa_start,
        "accepts": dfa_accepts,
        "_dfa_state_map": state_ids,
    }
