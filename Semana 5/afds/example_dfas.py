"""Example DFAs for demonstration: identifier and number.

These DFAs are simple table representations used to demonstrate minimization.
"""

# Alphabet limited for examples
ALPHA_ID = set(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"))

# Identifier DFA: states: q0 start (expects letter or _), q1 accept (rest)
states_id = {"q0", "q1"}
alphabet_id = ALPHA_ID
start_id = "q0"
accepts_id = {"q1"}

delta_id = {
    "q0": {},
    "q1": {},
}
for ch in ALPHA_ID:
    if ch.isalpha() or ch == "_":
        delta_id["q0"][ch] = "q1"
        delta_id["q1"][ch] = "q1"
    else:
        # digits from start should go to dead (absent -> rejection)
        pass

DFA_ID = {"states": states_id, "alphabet": alphabet_id, "delta": delta_id, "start": start_id, "accepts": accepts_id}

# Number DFA (simplified): integer and decimal without exponent to keep example small
states_num = {"s0", "s1", "s2"}
alphabet_num = set(list("0123456789."))
start_num = "s0"
accepts_num = {"s1", "s2"}  # s1 integer, s2 decimal

delta_num = {"s0": {}, "s1": {}, "s2": {}}
for d in "0123456789":
    delta_num["s0"][d] = "s1"
    delta_num["s1"][d] = "s1"
    delta_num["s2"][d] = "s2"
# dot
delta_num["s1"]["."] = "s2"

DFA_NUM = {"states": states_num, "alphabet": alphabet_num, "delta": delta_num, "start": start_num, "accepts": accepts_num}
