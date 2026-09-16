# 🐱 Cat Invaders: Operation Chill Out

A Space-Invaders-style arcade game with a twist: the "invaders" are grumpy
alien cats, and instead of blasting them, you launch cuddly cats at them to
**calm them down and send them home**. No violence, just vibes.

Built in Python with [pygame-ce](https://pyga.me/). Zero external art or
audio assets — every sprite is procedurally drawn pixel art, defined right
in the code.

## ▶️ Play it now

**From the terminal, in one line** (requires [uv](https://docs.astral.sh/uv/) or `pipx`):

```bash
uvx --from git+https://github.com/danilodileo/cat-invaders cat-invaders
```

```bash
pipx run --spec git+https://github.com/danilodileo/cat-invaders cat-invaders
```

**Or install it properly:**

```bash
pip install git+https://github.com/danilodileo/cat-invaders
cat-invaders
```

## 🎮 How to play

- **Move:** Left/Right arrows or `A` / `D`
- **Shoot a calming cat:** Space
- **Quit:** Esc

Grumpy alien cats march back and forth and creep closer with every level.
Hit one with a thrown cat to calm it down — it gets happy, floats away, and
you score points (aliens further back are worth more, just like classic
Space Invaders). Watch out for hairballs they cough up at you, and grab the
bonus cardboard-box mothership for extra points when it drifts by. Clear the
whole swarm to advance a level; let them reach the bottom, or run out of
lives, and it's game over.

## 🛠 Development

```bash
git clone https://github.com/danilodileo/cat-invaders
cd cat-invaders
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

cat-invaders          # play
pytest                # run the (headless) test suite
```

### Browser build (experimental, not yet playable)

There's a [`.github/workflows/deploy-web.yml`](.github/workflows/deploy-web.yml)
workflow that builds a WebAssembly version with
[pygbag](https://github.com/pygame-web/pygbag) and publishes it to GitHub
Pages on every push to `main`. It currently fails to run in the browser due
to an upstream version mismatch on pygbag's own asset CDN (the `pygame-ce`
wasm wheel it fetches doesn't exist under the filename its loader expects —
not a bug in this repo). Not linked from here until it actually works; build
it locally with `pip install pygbag && pygbag src/` if you want to check on it.

## 📁 Project structure

```
src/
  main.py                 # pygbag web entry point (thin wrapper)
  cat_invaders/
    main.py                # async game loop (desktop + web share this)
    game.py                 # state machine: menu / playing / game over
    entities.py              # Player, AlienCat, AlienSwarm, projectiles
    sprites.py                # procedural pixel-art sprites, zero image assets
    config.py                  # all the tunable numbers in one place
tests/                          # headless pytest suite (SDL dummy driver)
```

## License

MIT — see [LICENSE](LICENSE).
