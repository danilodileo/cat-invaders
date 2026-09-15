"""Async entry point, compatible with both a normal desktop run and a
pygbag/WASM browser build (pygbag requires the main loop to periodically
``await asyncio.sleep(0)`` so the browser can breathe between frames).
"""

from __future__ import annotations

import asyncio

import pygame

from . import config
from .game import Game


async def main() -> None:
    pygame.init()
    pygame.display.set_caption(config.CAPTION)
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = Game()
    running = True

    while running:
        dt = clock.tick(config.FPS) / 1000.0
        dt = min(dt, 0.05)  # avoid huge steps after a stall/tab switch

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            else:
                game.handle_event(event)

        game.update(dt)
        game.draw(screen)
        pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()


def run() -> None:
    """Console-script entry point (``cat-invaders``)."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
