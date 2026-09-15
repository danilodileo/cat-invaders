"""Top-level game state machine: menu, playing, level-clear, game over."""

from __future__ import annotations

import json
import random
from enum import Enum, auto
from pathlib import Path

import pygame

from . import config
from .entities import AlienSwarm, Mothership, Player, ProjectileCat


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    LEVEL_CLEAR = auto()
    GAME_OVER = auto()


def _high_score_path() -> Path:
    return Path.home() / ".cat_invaders" / config.HIGH_SCORE_FILE


def load_high_score() -> int:
    try:
        data = json.loads(_high_score_path().read_text())
        return int(data.get("high_score", 0))
    except Exception:
        return 0


def save_high_score(value: int) -> None:
    try:
        path = _high_score_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"high_score": value}))
    except Exception:
        pass  # persistence is a nice-to-have (e.g. unavailable in the browser)


class Game:
    def __init__(self) -> None:
        self.font_big = pygame.font.Font(None, 64)
        self.font_med = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 22)

        self.state = GameState.MENU
        self.level = 1
        self.score = 0
        self.high_score = load_high_score()
        self.message_timer = 0.0

        self.player = Player(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT - 30)
        self.swarm = AlienSwarm(self.level)
        self.projectiles: list[ProjectileCat] = []
        self.hairballs = []
        self.mothership: Mothership | None = None
        self.mothership_timer = random.uniform(
            config.MOTHERSHIP_MIN_DELAY, config.MOTHERSHIP_MAX_DELAY
        )
        self.stars = [
            (
                random.randint(0, config.SCREEN_WIDTH),
                random.randint(0, config.SCREEN_HEIGHT),
                random.choice((1, 1, 2)),
            )
            for _ in range(80)
        ]

    # -- setup ------------------------------------------------------------
    def _start_level(self, level: int) -> None:
        self.level = level
        self.swarm = AlienSwarm(level)
        self.projectiles.clear()
        self.hairballs.clear()
        self.mothership = None
        self.mothership_timer = random.uniform(
            config.MOTHERSHIP_MIN_DELAY, config.MOTHERSHIP_MAX_DELAY
        )

    def start_new_game(self) -> None:
        self.score = 0
        self.player = Player(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT - 30)
        self._start_level(1)
        self.state = GameState.PLAYING

    # -- input --------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if self.state in (GameState.MENU, GameState.GAME_OVER):
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.start_new_game()
        elif self.state == GameState.PLAYING:
            if event.key == pygame.K_SPACE:
                shot = self.player.try_shoot()
                if shot:
                    self.projectiles.append(shot)
        elif self.state == GameState.LEVEL_CLEAR:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._start_level(self.level + 1)
                self.state = GameState.PLAYING

    # -- update ---------------------------------------------------------------
    def update(self, dt: float) -> None:
        if self.state != GameState.PLAYING:
            return

        pressed = pygame.key.get_pressed()
        self.player.update(dt, pressed)
        self.swarm.update(dt)

        for shot in self.projectiles:
            shot.update(dt)
        self.projectiles = [p for p in self.projectiles if not p.offscreen]

        for hb in self.hairballs:
            hb.update(dt)
        self.hairballs = [h for h in self.hairballs if not h.offscreen]

        new_hairball = self.swarm.maybe_fire()
        if new_hairball:
            self.hairballs.append(new_hairball)

        self._update_mothership(dt)
        self._resolve_collisions()

        if self.swarm.reached_danger_line() or not self.player.alive:
            self._end_game()
        elif self.swarm.cleared():
            self.state = GameState.LEVEL_CLEAR

    def _update_mothership(self, dt: float) -> None:
        if self.mothership is None:
            self.mothership_timer -= dt
            if self.mothership_timer <= 0:
                self.mothership = Mothership()
            return
        self.mothership.update(dt)
        if self.mothership.offscreen:
            self.mothership = None
            self.mothership_timer = random.uniform(
                config.MOTHERSHIP_MIN_DELAY, config.MOTHERSHIP_MAX_DELAY
            )

    def _resolve_collisions(self) -> None:
        for shot in list(self.projectiles):
            for alien in self.swarm.marching:
                if shot.rect.colliderect(alien.rect):
                    self.score += alien.calm_down()
                    if shot in self.projectiles:
                        self.projectiles.remove(shot)
                    break
            else:
                if self.mothership and shot.rect.colliderect(self.mothership.rect):
                    self.score += config.MOTHERSHIP_POINTS
                    self.mothership = None
                    if shot in self.projectiles:
                        self.projectiles.remove(shot)

        for hb in list(self.hairballs):
            if hb.rect.colliderect(self.player.rect):
                if self.player.take_hit():
                    self.hairballs.remove(hb)

    def _end_game(self) -> None:
        self.state = GameState.GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)

    # -- drawing --------------------------------------------------------------
    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(config.BG_COLOR)
        for x, y, size in self.stars:
            pygame.draw.rect(surface, config.STAR_COLOR, (x, y, size, size))

        if self.state == GameState.MENU:
            self._draw_menu(surface)
            return

        self.swarm.draw(surface)
        if self.mothership:
            self.mothership.draw(surface)
        for shot in self.projectiles:
            shot.draw(surface)
        for hb in self.hairballs:
            hb.draw(surface)
        self.player.draw(surface)
        self._draw_hud(surface)

        if self.state == GameState.LEVEL_CLEAR:
            self._draw_center_message(
                surface, f"Level {self.level} calmed!", "Press ENTER for the next level"
            )
        elif self.state == GameState.GAME_OVER:
            self._draw_center_message(
                surface,
                "Game Over",
                f"Score: {self.score}   High score: {self.high_score}   Press ENTER to retry",
            )

    def _draw_hud(self, surface: pygame.Surface) -> None:
        score_surf = self.font_med.render(f"Score: {self.score}", True, config.TEXT_COLOR)
        surface.blit(score_surf, (16, 12))

        level_surf = self.font_med.render(f"Level {self.level}", True, config.TEXT_COLOR)
        rect = level_surf.get_rect(midtop=(config.SCREEN_WIDTH / 2, 12))
        surface.blit(level_surf, rect)

        for i in range(self.player.lives):
            pygame.draw.circle(
                surface,
                config.ACCENT_COLOR,
                (config.SCREEN_WIDTH - 24 - i * 28, 26),
                10,
            )

    def _draw_center_message(self, surface: pygame.Surface, title: str, subtitle: str) -> None:
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 8, 20, 190))
        surface.blit(overlay, (0, 0))

        title_surf = self.font_big.render(title, True, config.SUCCESS_COLOR)
        title_rect = title_surf.get_rect(
            center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 - 20)
        )
        surface.blit(title_surf, title_rect)

        subtitle_surf = self.font_small.render(subtitle, True, config.TEXT_COLOR)
        subtitle_rect = subtitle_surf.get_rect(
            center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 + 30)
        )
        surface.blit(subtitle_surf, subtitle_rect)

    def _draw_menu(self, surface: pygame.Surface) -> None:
        title_surf = self.font_big.render("CAT INVADERS", True, config.ACCENT_COLOR)
        title_rect = title_surf.get_rect(center=(config.SCREEN_WIDTH / 2, 170))
        surface.blit(title_surf, title_rect)

        subtitle_surf = self.font_med.render(
            "Operation Chill Out", True, config.TEXT_COLOR
        )
        subtitle_rect = subtitle_surf.get_rect(center=(config.SCREEN_WIDTH / 2, 220))
        surface.blit(subtitle_surf, subtitle_rect)

        lines = [
            "Grumpy alien cats have invaded! Throw cuddly cats at them",
            "to calm them down and send them back home - no violence needed.",
            "",
            "Move: Left/Right or A/D      Shoot: Space",
            "",
            f"High score: {self.high_score}",
            "",
            "Press ENTER or SPACE to start",
        ]
        for i, line in enumerate(lines):
            surf = self.font_small.render(line, True, config.TEXT_COLOR)
            rect = surf.get_rect(center=(config.SCREEN_WIDTH / 2, 290 + i * 26))
            surface.blit(surf, rect)
