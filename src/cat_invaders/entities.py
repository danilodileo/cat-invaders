"""Game entities: the player, alien cats, projectiles and the mothership."""

from __future__ import annotations

import random
from enum import Enum, auto

import pygame

from . import config, sprites


class AlienState(Enum):
    MARCHING = auto()
    CALMING = auto()
    GONE = auto()


class Player:
    def __init__(self, x: float, y: float) -> None:
        self.image = sprites.build_surface(
            sprites.PLAYER_CAT,
            config.PLAYER_PIXEL_SIZE,
            config.PLAYER_COLOR,
            secondary=config.PLAYER_EYE_COLOR,
        )
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.lives = config.PLAYER_LIVES
        self.cooldown = 0.0
        self.invulnerable = 0.0

    @property
    def alive(self) -> bool:
        return self.lives > 0

    def update(self, dt: float, pressed) -> None:
        dx = 0
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            dx -= 1
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            dx += 1
        self.rect.x += int(dx * config.PLAYER_SPEED * dt)
        self.rect.x = max(10, min(config.SCREEN_WIDTH - self.rect.width - 10, self.rect.x))

        if self.cooldown > 0:
            self.cooldown -= dt
        if self.invulnerable > 0:
            self.invulnerable -= dt

    def try_shoot(self) -> "ProjectileCat | None":
        if self.cooldown > 0:
            return None
        self.cooldown = config.PLAYER_SHOOT_COOLDOWN
        return ProjectileCat(self.rect.centerx, self.rect.top)

    def take_hit(self) -> bool:
        """Register a hit; returns True if it actually cost a life."""
        if self.invulnerable > 0:
            return False
        self.lives -= 1
        self.invulnerable = config.PLAYER_INVULNERABLE_TIME
        return True

    def draw(self, surface: pygame.Surface) -> None:
        if self.invulnerable > 0 and int(self.invulnerable * 12) % 2 == 0:
            return  # brief flicker while invulnerable
        surface.blit(self.image, self.rect)


class ProjectileCat:
    def __init__(self, x: float, y: float) -> None:
        self.image = sprites.build_surface(
            sprites.PROJECTILE_CAT,
            config.PROJECTILE_PIXEL_SIZE,
            config.PROJECTILE_COLOR,
            secondary=config.PLAYER_EYE_COLOR,
        )
        self.rect = self.image.get_rect(midbottom=(x, y))

    def update(self, dt: float) -> None:
        self.rect.y -= int(config.PROJECTILE_SPEED * dt)

    @property
    def offscreen(self) -> bool:
        return self.rect.bottom < 0

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)


class Hairball:
    def __init__(self, x: float, y: float) -> None:
        self.image = sprites.build_surface(
            sprites.HAIRBALL, config.HAIRBALL_PIXEL_SIZE, config.HAIRBALL_COLOR
        )
        self.rect = self.image.get_rect(midtop=(x, y))

    def update(self, dt: float) -> None:
        self.rect.y += int(config.HAIRBALL_SPEED * dt)

    @property
    def offscreen(self) -> bool:
        return self.rect.top > config.SCREEN_HEIGHT

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)


class AlienCat:
    def __init__(self, col: int, row: int, x: float, y: float) -> None:
        self.col = col
        self.row = row
        self.points = config.ALIEN_ROW_POINTS[min(row, len(config.ALIEN_ROW_POINTS) - 1)]
        color = config.ALIEN_COLORS[min(row, len(config.ALIEN_COLORS) - 1)]

        self.frame_a = sprites.build_surface(
            sprites.ALIEN_CAT_A, config.ALIEN_PIXEL_SIZE, color, secondary=(20, 15, 15)
        )
        self.frame_b = sprites.build_surface(
            sprites.ALIEN_CAT_B, config.ALIEN_PIXEL_SIZE, color, secondary=(20, 15, 15)
        )
        self.calm_frame = sprites.build_surface(
            sprites.ALIEN_CAT_CALM,
            config.ALIEN_PIXEL_SIZE,
            config.ALIEN_CALM_COLOR,
            highlight=(255, 120, 170),
        )

        self.rect = self.frame_a.get_rect(topleft=(x, y))
        self.state = AlienState.MARCHING
        self.calm_timer = 0.0
        self.anim_toggle = False

    @property
    def image(self) -> pygame.Surface:
        if self.state == AlienState.CALMING:
            return self.calm_frame
        return self.frame_a if self.anim_toggle else self.frame_b

    def calm_down(self) -> int:
        """Start the calm-and-send-home sequence; returns points earned."""
        if self.state != AlienState.MARCHING:
            return 0
        self.state = AlienState.CALMING
        self.calm_timer = config.ALIEN_CALM_DURATION
        return self.points

    def update(self, dt: float) -> None:
        if self.state == AlienState.CALMING:
            self.calm_timer -= dt
            self.rect.y -= int(140 * dt)
            if self.calm_timer <= 0:
                self.state = AlienState.GONE

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)


class AlienSwarm:
    """Manages the grid of alien cats with classic step-and-drop movement."""

    def __init__(self, level: int = 1) -> None:
        self.level = level
        self.direction = 1
        self.step_timer = 0.0
        self.aliens: list[AlienCat] = []
        rows = min(config.ALIEN_ROWS + (level - 1) // 2, len(config.ALIEN_ROW_POINTS))
        cols = config.ALIEN_COLS
        for row in range(rows):
            for col in range(cols):
                x = config.ALIEN_SIDE_MARGIN + col * config.ALIEN_H_SPACING
                y = config.ALIEN_TOP_MARGIN + row * config.ALIEN_V_SPACING
                self.aliens.append(AlienCat(col, row, x, y))
        self._total = len(self.aliens)

    @property
    def active(self) -> list[AlienCat]:
        return [a for a in self.aliens if a.state != AlienState.GONE]

    @property
    def marching(self) -> list[AlienCat]:
        return [a for a in self.aliens if a.state == AlienState.MARCHING]

    def cleared(self) -> bool:
        return len(self.active) == 0

    def reached_danger_line(self) -> bool:
        return any(a.rect.bottom >= config.DANGER_LINE_Y for a in self.marching)

    def _current_interval(self) -> float:
        remaining = len(self.marching)
        if remaining == 0 or self._total == 0:
            return config.ALIEN_BASE_INTERVAL
        ratio = remaining / self._total
        interval = config.ALIEN_MIN_INTERVAL + (
            config.ALIEN_BASE_INTERVAL - config.ALIEN_MIN_INTERVAL
        ) * ratio
        # Gently speed the swarm up on higher levels too.
        interval *= max(0.5, 1.0 - 0.05 * (self.level - 1))
        return max(config.ALIEN_MIN_INTERVAL, interval)

    def update(self, dt: float) -> None:
        for alien in self.aliens:
            alien.update(dt)

        marching = self.marching
        if not marching:
            return

        self.step_timer += dt
        interval = self._current_interval()
        if self.step_timer < interval:
            return
        self.step_timer = 0.0

        toggle_target = not marching[0].anim_toggle
        hits_edge = any(
            (a.rect.right >= config.SCREEN_WIDTH - 10 and self.direction > 0)
            or (a.rect.left <= 10 and self.direction < 0)
            for a in marching
        )

        if hits_edge:
            self.direction *= -1
            for alien in marching:
                alien.rect.y += config.ALIEN_STEP_DOWN
                alien.anim_toggle = toggle_target
        else:
            step = 10 + 2 * (self.level - 1)
            for alien in marching:
                alien.rect.x += step * self.direction
                alien.anim_toggle = toggle_target

    def maybe_fire(self) -> "Hairball | None":
        marching = self.marching
        if not marching:
            return None
        chance = config.ENEMY_FIRE_BASE_CHANCE + config.ENEMY_FIRE_LEVEL_SCALING * (
            self.level - 1
        )
        if random.random() > chance:
            return None

        # Pick the front-most (largest y) alien in a random column so shots
        # always originate from the swarm's leading edge.
        by_col: dict[int, AlienCat] = {}
        for alien in marching:
            current = by_col.get(alien.col)
            if current is None or alien.rect.y > current.rect.y:
                by_col[alien.col] = alien
        if not by_col:
            return None
        shooter = random.choice(list(by_col.values()))
        return Hairball(shooter.rect.centerx, shooter.rect.bottom)

    def draw(self, surface: pygame.Surface) -> None:
        for alien in self.active:
            alien.draw(surface)


class Mothership:
    def __init__(self) -> None:
        self.image = sprites.build_surface(
            sprites.MOTHERSHIP,
            config.ALIEN_PIXEL_SIZE,
            config.MOTHERSHIP_COLOR,
            secondary=(255, 220, 150),
        )
        self.direction = random.choice((-1, 1))
        start_x = -self.image.get_width() if self.direction > 0 else config.SCREEN_WIDTH
        self.rect = self.image.get_rect(topleft=(start_x, 40))

    def update(self, dt: float) -> None:
        self.rect.x += int(config.MOTHERSHIP_SPEED * dt * self.direction)

    @property
    def offscreen(self) -> bool:
        return self.rect.right < -10 or self.rect.left > config.SCREEN_WIDTH + 10

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
