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

## 🌐 Browser version

This repo is set up to also build a browser-playable version with
[pygbag](https://github.com/pygame-web/pygbag) (pygame → WebAssembly), via
[`.github/workflows/deploy-web.yml`](.github/workflows/deploy-web.yml), which
publishes to GitHub Pages on every push to `main`.

**Current status:** the build pipeline works (see below), but the actual
in-browser run currently fails to start due to an upstream version mismatch
on pygbag's own asset CDN — the `pygame-ce` wasm wheel it tries to fetch for
the bundled CPython 3.12 build doesn't exist under the filename its loader
expects (a real, verified 404 on pygame-web's CDN as of this writing, not a
bug in this repo). Once that's resolved upstream, the deployed Pages site
should work without any changes here. Track pygbag's releases/issues if you
want to know when it's fixed.

## 🛠 Development

```bash
git clone https://github.com/danilodileo/cat-invaders
cd cat-invaders
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

cat-invaders          # play
pytest                # run the (headless) test suite
```

### Building the browser version locally

```bash
pip install pygbag
pygbag src/          # serves at http://localhost:8000, builds to src/build/web
```

The GitHub Actions workflow in [`.github/workflows/deploy-web.yml`](.github/workflows/deploy-web.yml)
runs the same command and publishes `src/build/web` to GitHub Pages on every
push to `main`.

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
