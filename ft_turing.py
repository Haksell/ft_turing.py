import json
import sys

MAX_STEPS = 10**3


print("*" * 80)
print("*" + " " * 78 + "*")
print("*" + sys.argv[1][:-5].center(78) + "*")
print("*" + " " * 78 + "*")
print("*" * 80)
machine = json.load(open(sys.argv[1]))
transitions = {
    state: {t.pop("read"): t for t in ts}
    for state, ts in machine["transitions"].items()
}
print(f"Alphabet: [ {', '.join(machine['alphabet'])} ]")
print(f"States: [ {', '.join(machine['states'])} ]")
print(f"Initial: {machine['initial']}")
print(f"Finals: [ {', '.join(machine['finals'])} ]")
for from_state, ts in transitions.items():
    for char, t in ts.items():
        print(
            f"({from_state}, {char}) -> ({t['to_state']}, {t['write']}, {t['action']})"
        )
pos = 0
state = machine["initial"]
tape = dict(enumerate(sys.argv[2]))
print("*" * 80)
for _ in range(MAX_STEPS):
    if state in machine["finals"]:
        break
    if pos not in tape:
        tape[pos] = machine["blank"]
    step = transitions[state].get(tape[pos])
    print(
        f"[{''.join(f'<{v}>' if k == pos else v for k,v in sorted(tape.items()))}]",
        f"({state}, {tape[pos]})",
        "->",
        f"({step['to_state']}, {step['write']}, {step['action']})",
    )
    tape[pos] = step["write"]
    pos += -1 if step["action"] == "LEFT" else +1
    state = step["to_state"]
