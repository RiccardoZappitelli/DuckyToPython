def toducky(payload, execute=False) -> str:
    lines = [l.strip() for l in payload.splitlines() if l.strip()]
    out = []
    default_delay = 0.0
    last_stmt = None

    KEYMAP = {
        "GUI": "win",
        "WINDOWS": "win",
        "CTRL": "ctrl",
        "CONTROL": "ctrl",
        "ALT": "alt",
        "SHIFT": "shift",
        "ENTER": "enter",
        "TAB": "tab",
        "ESC": "esc",
        "ESCAPE": "esc",
        "SPACE": "space",
        "UP": "up",
        "DOWN": "down",
        "LEFT": "left",
        "RIGHT": "right",
        "DELETE": "delete",
        "DEL": "delete",
        "BACKSPACE": "backspace",
        "HOME": "home",
        "END": "end",
        "PAGEUP": "pageup",
        "PAGEDOWN": "pagedown",
        "PRINTSCREEN": "printscreen",
        "CAPSLOCK": "capslock",
        "NUMLOCK": "numlock",
    }

    def emit(stmt: str):
        nonlocal last_stmt
        out.append(stmt)
        last_stmt = stmt

    for line in lines:
        if line.startswith(("REM", "#")):
            continue

        tokens = line.split()

        cmd = tokens[0]

        if cmd == "DEFAULT_DELAY":
            default_delay = float(tokens[1]) / 1000.0
            continue

        if cmd == "DELAY":
            emit(f"sleep({float(tokens[1]) / 1000.0})")
            continue

        if cmd == "STRING":
            text = line[len("STRING "):]
            emit(f"pg.write({text!r}, interval=0.01)")

        elif cmd == "STRINGLN":
            text = line[len("STRINGLN "):]
            emit(f"pg.write({text!r}, interval=0.01); pg.press('enter')")

        elif cmd == "REPEAT":
            if last_stmt is None:
                continue
            count = int(tokens[1]) - 1
            for _ in range(count):
                out.append(last_stmt)

        else:
            keys = []
            for t in tokens:
                t = t.upper()
                if t in KEYMAP:
                    keys.append(KEYMAP[t])
                elif len(t) == 1:
                    keys.append(t.lower())
            if keys:
                emit(f"pg.hotkey({', '.join(repr(k) for k in keys)})")

        if default_delay > 0:
            out.append(f"sleep({default_delay})")

    final = "\n".join(out)

    if execute:
        exec("import time\nimport pyautogui as pg\n" + final)

    return final
