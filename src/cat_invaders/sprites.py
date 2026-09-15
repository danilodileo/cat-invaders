"""Procedural pixel-art sprites.

Every sprite is defined as a small bitmap of characters so the whole game
ships with zero external image assets (no licensing worries, tiny repo,
works identically on desktop and in the browser build).

Bitmap legend:
    '.' -> transparent
    'X' -> primary color
    'o' -> secondary/eye color
    'H' -> highlight/heart color
"""

from __future__ import annotations

import pygame

Bitmap = list[str]

# Angry alien cat, two animation frames (classic invader-style leg wiggle).
ALIEN_CAT_A: Bitmap = [
    "..X.....X..",
    "...X...X...",
    "..XXXXXXX..",
    ".XXoXXXoXX.",
    "XXXXXXXXXXX",
    "X.XXXXXXX.X",
    "X.X.....X.X",
    "...XX.XX...",
]

ALIEN_CAT_B: Bitmap = [
    "..X.....X..",
    "...X...X...",
    "..XXXXXXX..",
    ".XXoXXXoXX.",
    "XXXXXXXXXXX",
    "X.XXXXXXX.X",
    ".X.X...X.X.",
    "X.X.....X.X",
]

# Calmed alien cat: soft eyes, little smile, hearts floating off - shown
# briefly before the alien drifts away and is removed from the swarm.
ALIEN_CAT_CALM: Bitmap = [
    "..X.....X..",
    "H..X...X..H",
    "..XXXXXXX..",
    ".XXHXXXHXX.",
    "XXXXXXXXXXX",
    "X.XXXXXXX.X",
    "X..XXXXX..X",
    "...X...X...",
]

# The player's cat cannon: a determined little cat lobbing kittens skyward.
PLAYER_CAT: Bitmap = [
    ".X.......X.",
    "XX..XXX..XX",
    "XoXXXXXXXoX",
    "XXXXXXXXXXX",
    "XXXX.X.XXXX",
    ".XXXXXXXXX.",
    "..X.....X..",
    ".X.......X.",
]

# Friendly projectile: a small kitten in mid-flight, thrown with love.
PROJECTILE_CAT: Bitmap = [
    ".X.X.",
    "XXXXX",
    "XoXoX",
    "XXXXX",
    ".XXX.",
]

# Enemy projectile: a rolled-up hairball.
HAIRBALL: Bitmap = [
    ".XX.",
    "XXXX",
    "XXXX",
    ".XX.",
]

# Bonus mothership: a cardboard-box UFO with a cat peeking out the top.
MOTHERSHIP: Bitmap = [
    "......XX......",
    ".....XooX.....",
    "...XXXXXXXX...",
    ".XXXXXXXXXXXX.",
    "XXXXXXXXXXXXXX",
    ".X.X.X.X.X.X.X",
]

_COLOR_KEYS = {"X": "primary", "o": "secondary", "H": "highlight"}


def build_surface(
    bitmap: Bitmap,
    pixel_size: int,
    primary: tuple[int, int, int],
    secondary: tuple[int, int, int] | None = None,
    highlight: tuple[int, int, int] | None = None,
) -> pygame.Surface:
    """Rasterize a character bitmap into a pygame Surface with alpha."""
    height = len(bitmap)
    width = len(bitmap[0])
    surface = pygame.Surface((width * pixel_size, height * pixel_size), pygame.SRCALPHA)

    colors = {
        "X": primary,
        "o": secondary or primary,
        "H": highlight or primary,
    }

    for row, line in enumerate(bitmap):
        for col, char in enumerate(line):
            if char == ".":
                continue
            color = colors.get(char, primary)
            rect = pygame.Rect(col * pixel_size, row * pixel_size, pixel_size, pixel_size)
            surface.fill(color, rect)

    return surface
