# FrankenApp 🧟

A deliberately useless app that takes the word `RAGEBAIT` and drags it through
an absurd chain of programming languages — one language stitching its bit
onto whatever the last one left behind, Frankenstein's-monster style, except
the spare parts here are languages instead of limbs.

Hit the one button. Watch the log scroll through two dozen languages. Get a
final string that means nothing. That's the whole app.

## What it actually does

It's a small Tkinter window with a single button: **"DO SOMETHING USELESS"**.
Click it, and the `pipeline()` function in `app.py` runs the string through
every stage, in order, each one appending ` -> WhateverLanguage` to whatever
it was handed.

There are two very different kinds of stage:

### Embedded stages (always run, no dependencies)

These are interpreted in pure Python, right inside `app.py`. No interpreter,
no compiler, no runtime to install — they work on literally any machine that
can run Python, which is the whole point of calling this version "really
embedded":

| Language   | Source file            | What's going on |
|------------|-------------------------|------------------|
| Brainfuck  | `stages/brainfuck.bf`   | The classic tape machine (`+ - < > . , [ ]`) |
| Ook!       | `stages/stage.ook`      | Brainfuck wearing a trenchcoat made of "Ook." |
| Deadfish   | `stages/stage.df`       | A single accumulator, `i`/`d`/`s`/`o`, with the real -1/256 overflow quirk |
| Whitespace | `stages/stage.ws`       | A program made only of spaces, tabs and line breaks |
| Unary      | `stages/stage.unary`    | A Brainfuck program re-encoded as nothing but runs of zeroes |
| Befunge-93 | `stages/stage.bf93`     | Stack-based: push digits, `+`/`*` to build numbers, `,` to print |

Brainfuck, Ook! and Unary all share one tiny tape-machine implementation
(`run_tape_vm`) — Ook! is just Brainfuck with different spelling, and Unary
is just Brainfuck with the instructions written as tally marks. Deadfish,
Whitespace and Befunge-93 each get their own small, spec-faithful
interpreter.

### External stages (optional, skipped if missing)

These shell out to the real interpreter/compiler for the language. If it
isn't installed, the stage logs `[skip]` and the text moves on untouched —
nothing ever breaks just because your machine doesn't have, say, Zig on it:

- JavaScript (`node`)
- TypeScript (`deno`)
- Ruby (`ruby`)
- PHP (`php`)
- Perl (`perl`)
- Lua (`lua`)
- Bash (`bash`)
- PowerShell (`pwsh`)
- Kotlin (`kotlin`)
- Haskell (`runghc`)
- Elixir (`elixir`)
- Dart (`dart`)
- Nim (`nim`)
- Julia (`julia`)
- Crystal (`crystal`)
- Erlang (`escript`)
- Zig (`zig`)
- C (compiled once with `gcc`, cached in `build/`)
- C++ (compiled once with `g++`)
- Rust (compiled once with `rustc`)
- Go (compiled once with `go build`)
- Java (compiled with `javac`, run with `java`)
- Swift (`swift`)
- R (`Rscript`)

Add it all up and the pipeline touches **31 languages**: Python (where the
string is born), 6 fully embedded esolangs, and 24 external ones that run if
they're available and quietly step aside if they're not.

## Running it

Linux/macOS:

```bash
./run.sh
```

Windows:

```bat
run.bat
```

Or directly:

```bash
python3 app.py
```

> Needs Tkinter available in your Python (on Linux that's usually the
> `python3-tk` package).

### Standalone executables

If you don't want to deal with Python at all, grab a prebuilt executable
instead:

- **Linux** — a single-file binary built with PyInstaller. Download it,
  `chmod +x FrankenApp`, run it.
- **Windows** — built the same way, as a `.exe`, via the GitHub Actions
  workflow in `.github/workflows/build.yml`. It builds on real Windows and
  Linux runners (no cross-compiling nonsense), and every run's artifacts are
  the downloadable executables.

You can build either one yourself locally too:

```bash
./build.sh      # Linux/macOS -> dist/FrankenApp
build.bat       # Windows     -> dist\FrankenApp.exe
```

Both just wrap `pyinstaller --onefile --windowed --add-data ... app.py` with
the right path separator for the platform.

## Layout

```
app.py            # pipeline + Tkinter UI + the embedded interpreters
run.sh / run.bat  # convenience launchers
stages/           # one source file per language stage
build/            # compiled binaries/.class files, created at runtime (git-ignored)
```

## Why this exists

Because it was funny to build. No single stage does anything useful on its
own — they just form a dumb chain that wanders through 20+ programming
ecosystems to eventually produce `RAGEBAIT -> JS -> Ruby -> ... -> Befunge`.
That's the joke. That's always been the joke.
