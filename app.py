import os, sys, subprocess, shutil, tkinter as tk
from tkinter import scrolledtext

BASE = os.path.dirname(os.path.abspath(__file__))
STAGES = os.path.join(BASE, 'stages')
BUILD = os.path.join(BASE, 'build')
os.makedirs(BUILD, exist_ok=True)


def run_cmd(cmd, text):
    try:
        p = subprocess.run(cmd, input=text, text=True, capture_output=True, timeout=8)
        if p.returncode == 0:
            out = p.stdout.strip()
            return out if out else text
    except Exception:
        pass
    return text


def ensure_native(name, compiler, source, outname, args=None):
    args = args or []
    exe = os.path.join(BUILD, outname)
    if os.name == 'nt' and not exe.endswith('.exe'):
        exe += '.exe'
    if os.path.exists(exe):
        return exe
    if shutil.which(compiler):
        try:
            subprocess.run([compiler, source, '-O2', '-o', exe] + args, cwd=BASE, capture_output=True, timeout=30)
            if os.path.exists(exe):
                return exe
        except Exception:
            pass
    return None


def stage(name, cmd_builder, text, log):
    try:
        cmd = cmd_builder()
        if not cmd:
            log(f'[skip] {name}')
            return text
        new = run_cmd(cmd, text)
        log(f'[{name}] {new}')
        return new
    except Exception:
        log(f'[skip] {name}')
        return text


# ---------------------------------------------------------------------------
# Embedded esoteric-language interpreters.
#
# These never show up as "[skip]": they are implemented in pure Python right
# here, so they always run no matter what is (or isn't) installed on the
# machine. This is the "really embedded" part of FrankenApp.
# ---------------------------------------------------------------------------

def run_tape_vm(ops):
    """Minimal Brainfuck-style tape machine. Returns the printed output."""
    tape = [0] * 30000
    ptr = 0
    pc = 0
    out = []
    bracket = {}
    stack = []
    for i, c in enumerate(ops):
        if c == '[':
            stack.append(i)
        elif c == ']':
            j = stack.pop()
            bracket[i] = j
            bracket[j] = i
    while pc < len(ops):
        c = ops[pc]
        if c == '>':
            ptr += 1
        elif c == '<':
            ptr -= 1
        elif c == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif c == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif c == '.':
            out.append(chr(tape[ptr]))
        elif c == ',':
            pass  # no stdin reading needed for our canned programs
        elif c == '[' and tape[ptr] == 0:
            pc = bracket[pc]
        elif c == ']' and tape[ptr] != 0:
            pc = bracket[pc]
        pc += 1
    return ''.join(out)


def brainfuck(text):
    code = open(os.path.join(STAGES, 'brainfuck.bf'), encoding='utf-8').read()
    return text + run_tape_vm(code)


OOK_TO_BF = {
    'Ook. Ook?': '>',
    'Ook? Ook.': '<',
    'Ook. Ook.': '+',
    'Ook! Ook!': '-',
    'Ook! Ook.': '.',
    'Ook. Ook!': ',',
    'Ook! Ook?': '[',
    'Ook? Ook!': ']',
}


def ook(text):
    src = open(os.path.join(STAGES, 'stage.ook'), encoding='utf-8').read()
    tokens = src.split()
    ops = []
    for i in range(0, len(tokens) - 1, 2):
        pair = tokens[i] + ' ' + tokens[i + 1]
        if pair in OOK_TO_BF:
            ops.append(OOK_TO_BF[pair])
    return text + run_tape_vm(''.join(ops))


def deadfish(text):
    """Real Deadfish semantics (i/d/s/o + the -1/256 overflow quirk),
    reinterpreted as a text stage: each printed number is one character
    code of the suffix we're building."""
    src = open(os.path.join(STAGES, 'stage.df'), encoding='utf-8').read()
    acc = 0
    chars = []
    for cmd in src:
        if cmd == 'i':
            acc += 1
        elif cmd == 'd':
            acc -= 1
        elif cmd == 's':
            acc *= acc
        elif cmd == 'o':
            chars.append(chr(acc))
        if acc == -1 or acc == 256:
            acc = 0
    return text + ''.join(chars)


def whitespace(text):
    """Tiny interpreter for a subset of the real Whitespace language:
    push-number, output-character and end-program."""
    src = open(os.path.join(STAGES, 'stage.ws'), encoding='utf-8', newline='').read()
    SP, TAB, LF = ' ', '\t', '\n'
    i = 0
    n = len(src)
    stack = []
    out = []

    def imp():
        nonlocal i
        if src[i] == SP:
            i += 1
            return 'stack'
        if src[i] == TAB and i + 1 < n and src[i + 1] == LF:
            i += 2
            return 'io'
        if src[i] == LF:
            i += 1
            return 'flow'
        i += 1
        return None

    while i < n:
        kind = imp()
        if kind == 'stack':
            # only the Push command is used by our generated programs
            if i < n and src[i] == SP:
                i += 1
                sign = 1 if (i < n and src[i] == SP) else -1
                i += 1
                bits = ''
                while i < n and src[i] != LF:
                    bits += '1' if src[i] == TAB else '0'
                    i += 1
                i += 1  # consume terminating LF
                value = sign * (int(bits, 2) if bits else 0)
                stack.append(value)
        elif kind == 'io':
            if i < n and src[i] == SP and i + 1 < n and src[i + 1] == SP:
                i += 2
                out.append(chr(stack.pop()))
        elif kind == 'flow':
            if i < n and src[i] == LF:
                i += 1
                break  # end program
            i += 1
        else:
            break
    return text + ''.join(out)


def pipeline(log):
    text = 'RAGEBAIT'
    log('[Python] ' + text)

    specs = [
        ('JavaScript', lambda: [shutil.which('node'), os.path.join(STAGES, 'stage.js')] if shutil.which('node') else None),
        ('Ruby', lambda: [shutil.which('ruby'), os.path.join(STAGES, 'stage.rb')] if shutil.which('ruby') else None),
        ('PHP', lambda: [shutil.which('php'), os.path.join(STAGES, 'stage.php')] if shutil.which('php') else None),
        ('Perl', lambda: [shutil.which('perl'), os.path.join(STAGES, 'stage.pl')] if shutil.which('perl') else None),
        ('Lua', lambda: [shutil.which('lua'), os.path.join(STAGES, 'stage.lua')] if shutil.which('lua') else None),
        ('Bash', lambda: [shutil.which('bash'), os.path.join(STAGES, 'stage.sh')] if shutil.which('bash') else None),
        ('PowerShell', lambda: [shutil.which('pwsh'), '-File', os.path.join(STAGES, 'stage.ps1')] if shutil.which('pwsh') else None),
    ]

    for name, cb in specs:
        text = stage(name, cb, text, log)

    # --- embedded stages: no external runtime required, never skipped ---
    text = brainfuck(text)
    log('[Brainfuck] ' + text)

    text = ook(text)
    log('[Ook!] ' + text)

    text = deadfish(text)
    log('[Deadfish] ' + text)

    text = whitespace(text)
    log('[Whitespace] ' + text)
    # ----------------------------------------------------------------------

    cexe = ensure_native('C', 'gcc', os.path.join(STAGES, 'stage.c'), 'stage_c')
    text = stage('C', lambda: [cexe] if cexe else None, text, log)

    cppexe = ensure_native('C++', 'g++', os.path.join(STAGES, 'stage.cpp'), 'stage_cpp')
    text = stage('C++', lambda: [cppexe] if cppexe else None, text, log)

    rustexe = ensure_native('Rust', 'rustc', os.path.join(STAGES, 'stage.rs'), 'stage_rust')
    text = stage('Rust', lambda: [rustexe] if rustexe else None, text, log)

    goexe = None
    if shutil.which('go'):
        goexe = os.path.join(BUILD, 'stage_go.exe' if os.name == 'nt' else 'stage_go')
        if not os.path.exists(goexe):
            try:
                subprocess.run(['go', 'build', '-o', goexe, os.path.join(STAGES, 'stage.go')], capture_output=True, timeout=30)
            except Exception:
                pass
    text = stage('Go', lambda: [goexe] if goexe and os.path.exists(goexe) else None, text, log)

    if shutil.which('javac') and shutil.which('java'):
        cls = os.path.join(BUILD, 'Stage.class')
        if not os.path.exists(cls):
            try:
                subprocess.run(['javac', '-d', BUILD, os.path.join(STAGES, 'Stage.java')], capture_output=True, timeout=30)
            except Exception:
                pass
        text = stage('Java', lambda: [shutil.which('java'), '-cp', BUILD, 'Stage'] if os.path.exists(cls) else None, text, log)
    else:
        log('[skip] Java')

    if shutil.which('swift'):
        text = stage('Swift', lambda: [shutil.which('swift'), os.path.join(STAGES, 'stage.swift')], text, log)
    else:
        log('[skip] Swift')

    if shutil.which('Rscript'):
        text = stage('R', lambda: [shutil.which('Rscript'), os.path.join(STAGES, 'stage.R')], text, log)
    else:
        log('[skip] R')

    log('\nFINAL: ' + text)
    return text


def main():
    root = tk.Tk()
    root.title('FrankenApp')
    root.geometry('760x560')
    root.resizable(False, False)

    title = tk.Label(root, text='RAGEBAIT', font=('Arial', 28, 'bold'))
    title.pack(pady=(20, 8))
    sub = tk.Label(root, text='A completely useless multi-language application', font=('Arial', 11))
    sub.pack()

    output = scrolledtext.ScrolledText(root, width=88, height=22, font=('Courier New', 10), state='disabled')
    output.pack(padx=18, pady=18)

    def log(msg):
        output.configure(state='normal')
        output.insert('end', msg + '\n')
        output.see('end')
        output.configure(state='disabled')
        root.update_idletasks()

    def go():
        output.configure(state='normal'); output.delete('1.0', 'end'); output.configure(state='disabled')
        btn.config(state='disabled', text='Doing absolutely nothing useful...')
        pipeline(log)
        btn.config(state='normal', text='DO SOMETHING USELESS')

    btn = tk.Button(root, text='DO SOMETHING USELESS', command=go, width=34, height=2, font=('Arial', 11, 'bold'))
    btn.pack(pady=(0, 10))
    tk.Label(root, text='Embedded stages always run. Missing external runtimes are skipped automatically.', font=('Arial', 9)).pack()
    root.mainloop()


if __name__ == '__main__':
    main()
