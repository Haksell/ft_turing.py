from collections import deque
import json
import sys

DEBUG = False
MAX_STEPS = 10**4


def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def stringify_tape(tape, pos, blank, *, return_start=False):
    cells = deque(sorted(tape.items()))
    while cells and cells[0][1] == blank:
        cells.popleft()
    while cells and cells[-1][1] == blank:
        cells.pop()
    res = f"[{''.join(f'<{v}>' if k == pos else v for k, v in cells)}]"
    if return_start:
        return res, cells[0][0] if cells else None
    else:
        return res


def main():
    dprint("*" * 80)
    dprint("*" + " " * 78 + "*")
    dprint("*" + sys.argv[1][:-5].center(78) + "*")
    dprint("*" + " " * 78 + "*")
    dprint("*" * 80)
    machine = json.load(open(sys.argv[1]))
    blank = machine["blank"]
    transitions = {
        state: {t.pop("read"): t for t in ts}
        for state, ts in machine["transitions"].items()
    }
    dprint(f"Alphabet: [ {', '.join(machine['alphabet'])} ]")
    dprint(f"States: [ {', '.join(machine['states'])} ]")
    dprint(f"Initial: {machine['initial']}")
    dprint(f"Finals: [ {', '.join(machine['finals'])} ]")
    for from_state, ts in transitions.items():
        for char, t in ts.items():
            dprint(
                f"({from_state}, {char}) -> ({t['to_state']}, {t['write']}, {t['action']})"
            )
    pos = 0
    state = machine["initial"]
    tape = dict(enumerate(sys.argv[2]))
    dprint("*" * 80)
    seen = set()
    for _ in range(MAX_STEPS):
        if state in machine["finals"]:
            print(stringify_tape(tape, pos, blank), "Final state:", state)
            break
        str_tape, start = stringify_tape(tape, pos, blank, return_start=True)
        complete_state = (state, str_tape, pos - start if start else None)
        if complete_state in seen:
            print(stringify_tape(tape, pos, blank), "Infinite loop detected")
            break
        seen.add(complete_state)
        if pos not in tape:
            tape[pos] = blank
        step = transitions[state].get(tape[pos])
        if step is None:
            print(
                stringify_tape(tape, pos, blank),
                f"Unexpected transition: ({state}, {tape[pos]})",
            )
            break
        dprint(
            stringify_tape(tape, pos, blank),
            f"({state}, {tape[pos]})",
            "->",
            f"({step['to_state']}, {step['write']}, {step['action']})",
        )
        tape[pos] = step["write"]
        pos += -1 if step["action"] == "LEFT" else 1
        state = step["to_state"]
    else:
        print(
            stringify_tape(tape, pos, blank),
            f"No final state found after {MAX_STEPS} steps",
        )


if __name__ == "__main__":
    main()
