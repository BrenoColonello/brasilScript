"""NFA builders for Semana 6 local folder (adapted from src)."""
from typing import Dict, Set, Any


def fresh_state(prefix="q"):
    fresh_state.counter += 1
    return f"{prefix}{fresh_state.counter}"


fresh_state.counter = 0


def make_basic_nfa_for_identifier(token_name="IDENTIFICADOR"):
    s0 = fresh_state()
    s1 = fresh_state()
    states = {s0, s1}
    alphabet = set(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"))
    delta = {s0: {}, s1: {}}
    for ch in alphabet:
        if ch.isalpha() or ch == '_':
            delta[s0].setdefault(ch, set()).add(s1)
            delta[s1].setdefault(ch, set()).add(s1)
        else:
            delta[s1].setdefault(ch, set()).add(s1)
    return {"states": states, "alphabet": alphabet, "delta": delta, "start": s0, "accepts": {s1: token_name}}


def make_basic_nfa_for_number(token_name="NUMERO_LITERAL"):
    s0 = fresh_state()
    s1 = fresh_state()
    s2 = fresh_state()
    states = {s0, s1, s2}
    alphabet = set(list("0123456789."))
    delta = {s0: {}, s1: {}, s2: {}}
    for d in "0123456789":
        delta[s0].setdefault(d, set()).add(s1)
        delta[s1].setdefault(d, set()).add(s1)
        delta[s2].setdefault(d, set()).add(s2)
    delta[s1].setdefault('.', set()).add(s2)
    return {"states": states, "alphabet": alphabet, "delta": delta, "start": s0, "accepts": {s1: token_name, s2: token_name}}


def combine_nfas(nfas):
    states = set()
    alphabet = set()
    delta = {}
    start = fresh_state("start")
    accepts = {}
    delta[start] = {None: set()}
    for nfa in nfas:
        states.update(nfa["states"]) 
        alphabet.update(nfa["alphabet"]) 
        for s, trans in nfa["delta"].items():
            delta.setdefault(s, {})
            for a, tgt in trans.items():
                delta[s].setdefault(a, set()).update(tgt)
        delta[start][None].add(nfa["start"])
        accepts.update(nfa.get("accepts", {}))
    states.add(start)
    return {"states": states, "alphabet": alphabet, "delta": delta, "start": start, "accepts": accepts}


def make_basic_nfa_for_operators(token_name="OP"):
    ops = list("+-*/%=!<>:,;().{}[]")
    s0 = fresh_state()
    s1 = fresh_state()
    states = {s0, s1}
    alphabet = set(ops)
    delta = {s0: {}, s1: {}}
    for ch in alphabet:
        delta[s0].setdefault(ch, set()).add(s1)
    return {"states": states, "alphabet": alphabet, "delta": delta, "start": s0, "accepts": {s1: token_name}}
