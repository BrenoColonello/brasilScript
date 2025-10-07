"""DFA-based lexer for Semana 6 folder (local, standalone)."""
from afn_to_afd import nfa_to_dfa
from nfas import make_basic_nfa_for_identifier, make_basic_nfa_for_number, combine_nfas, make_basic_nfa_for_operators


def build_lexer_dfa():
    nfa_id = make_basic_nfa_for_identifier()
    nfa_num = make_basic_nfa_for_number()
    nfa_op = make_basic_nfa_for_operators()
    combined = combine_nfas([nfa_num, nfa_id, nfa_op])
    dfa = nfa_to_dfa(combined, token_priority=["NUMERO_LITERAL", "IDENTIFICADOR", "OP"])
    return dfa


def tokenize_with_dfa(dfa, text: str):
    pos = 0
    n = len(text)
    tokens = []
    while pos < n:
        state = dfa["start"]
        last_accept = None
        last_pos = pos
        cur = pos
        while cur < n:
            ch = text[cur]
            trans = dfa["delta"].get(state, {})
            ns = trans.get(ch)
            if ns is None:
                break
            state = ns
            cur += 1
            if state in dfa.get("accepts", {}):
                last_accept = dfa["accepts"][state]
                last_pos = cur

        if last_accept is None:
            if text[pos].isspace():
                pos += 1
                continue
            raise ValueError(f"Unexpected char at {pos}: {text[pos]!r}")

        tokens.append((last_accept, text[pos:last_pos]))
        pos = last_pos

    return tokens


if __name__ == '__main__':
    dfa = build_lexer_dfa()
    print(tokenize_with_dfa(dfa, 'a = 123 b = abc'))
