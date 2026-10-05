# FrankenApp 🧟

Um aplicativo **deliberadamente inútil** que pega a palavra `RAGEBAIT` e manda ela
por uma cadeia absurda de linguagens de programação, uma "costurando" o resultado
da outra — tipo o monstro do Frankenstein, só que feito de linguagens em vez de
partes de corpo.

Cada etapa (*stage*) pega o texto que recebeu, faz alguma coisinha com ele
(normalmente só concatena ` -> NomeDaLinguagem`) e passa pra frente. No final a
interface mostra o log completo de cada etapa e o resultado final.

## Como funciona

A interface é uma janela em Tkinter com um botão **"DO SOMETHING USELESS"**.
Ao clicar, o app roda um pipeline (`pipeline()` em `app.py`) que passa o texto
por todas as linguagens, na ordem, uma depois da outra.

Existem dois tipos de etapa:

### 1. Etapas embutidas (sempre rodam)

São interpretadas em Python puro, dentro do próprio `app.py`. Não dependem de
nenhum runtime, compilador ou binário externo instalado na máquina — **sempre
funcionam**, em qualquer computador com Python:

| Linguagem    | Arquivo               | Observação |
|--------------|------------------------|------------|
| Brainfuck    | `stages/brainfuck.bf`  | Máquina de fita clássica (`+ - < > . , [ ]`) |
| Ook!         | `stages/stage.ook`     | Dialeto do Brainfuck escrito só com "Ook." |
| Deadfish     | `stages/stage.df`      | Acumulador com `i`/`d`/`s`/`o` e o "bug" de overflow (-1/256 voltam a 0) |
| Whitespace   | `stages/stage.ws`      | Programa escrito só com espaços, tabs e quebras de linha |

O interpretador de Brainfuck e o de Ook! compartilham a mesma máquina de fita
(`run_tape_vm`), já que Ook! nada mais é que Brainfuck com uma sintaxe
diferente. Deadfish e Whitespace têm interpretadores próprios, bem pequenos,
mas fiéis às regras reais dessas linguagens esotéricas.

### 2. Etapas externas (opcionais)

Chamam o interpretador/compilador real da linguagem via `subprocess`. Se o
runtime não estiver instalado, a etapa é **pulada automaticamente**
(aparece como `[skip]` no log) e o texto segue pra próxima etapa sem quebrar
o app:

- JavaScript (`node`)
- Ruby (`ruby`)
- PHP (`php`)
- Perl (`perl`)
- Lua (`lua`)
- Bash (`bash`)
- PowerShell (`pwsh`)
- C (compilado com `gcc` na primeira execução e cacheado em `build/`)
- C++ (compilado com `g++`)
- Rust (compilado com `rustc`)
- Go (compilado com `go build`)
- Java (compilado com `javac` + executado com `java`)
- Swift (`swift`)
- R (`Rscript`)

No total, o pipeline passa por **19 linguagens**: Python (onde tudo começa),
4 esotéricas totalmente embutidas (Brainfuck, Ook!, Deadfish, Whitespace) e
14 externas/opcionais (JavaScript, Ruby, PHP, Perl, Lua, Bash, PowerShell, C,
C++, Rust, Go, Java, Swift, R).

## Rodar

Linux/macOS:

```bash
./run.sh
```

Windows:

```bat
run.bat
```

Também pode executar diretamente:

```bash
python3 app.py
```

> Tkinter precisa estar disponível no Python para a interface gráfica
> (no Linux, geralmente é o pacote `python3-tk`).

As etapas externas que não tiverem o runtime instalado simplesmente são
puladas — o app nunca quebra por falta de uma linguagem no sistema.

## Estrutura

```
app.py            # pipeline + interface Tkinter + interpretadores embutidos
run.sh / run.bat  # scripts de conveniência para rodar o app
stages/           # o código-fonte de cada etapa, uma linguagem por arquivo
build/            # binários/.class compilados em tempo de execução (git-ignored)
```

## Por que isso existe

Porque dava. É um exercício de "Frankenstein de linguagens": nenhuma etapa faz
nada de útil sozinha, mas juntas formam uma corrente boba que atravessa quase
20 ecossistemas de programação diferentes só para dizer `RAGEBAIT -> JS -> ...`.
