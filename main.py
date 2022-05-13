from dfa import DFA

dfa = DFA()
dfa.read("data.in")
print(dfa.transitions)
print(dfa.alphabet)
print(dfa.final_states)
print(dfa.initial_state)
dfa_minimized = dfa.minimize()
print("DFA MINIMIZAT")
print(dfa_minimized.transitions)
print(dfa_minimized.states)
print(dfa_minimized.initial_state)
print(dfa_minimized.final_states)

