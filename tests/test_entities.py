import pygame

from cat_invaders import config
from cat_invaders.entities import AlienCat, AlienState, AlienSwarm, Hairball, Player


class FakePressed(dict):
    def __missing__(self, key):
        return False


def make_pressed(**held):
    pressed = FakePressed()
    for key, value in held.items():
        pressed[getattr(pygame, key)] = value
    return pressed


def test_player_shoot_respects_cooldown():
    player = Player(400, 560)
    first = player.try_shoot()
    assert first is not None

    immediate = player.try_shoot()
    assert immediate is None

    player.update(config.PLAYER_SHOOT_COOLDOWN + 0.01, make_pressed())
    second = player.try_shoot()
    assert second is not None


def test_player_movement_clamped_to_screen():
    player = Player(400, 560)
    player.update(10.0, make_pressed(K_LEFT=True))
    assert player.rect.left >= 10

    player.rect.x = 0
    player.update(10.0, make_pressed(K_RIGHT=True))
    assert player.rect.right <= config.SCREEN_WIDTH - 10


def test_player_invulnerability_prevents_double_hit():
    player = Player(400, 560)
    assert player.take_hit() is True
    assert player.lives == config.PLAYER_LIVES - 1
    assert player.take_hit() is False
    assert player.lives == config.PLAYER_LIVES - 1


def test_alien_calm_down_awards_points_once():
    alien = AlienCat(0, 0, 100, 100)
    points = alien.calm_down()
    assert points == config.ALIEN_ROW_POINTS[0]
    assert alien.state == AlienState.CALMING

    again = alien.calm_down()
    assert again == 0


def test_alien_becomes_gone_after_calm_duration():
    alien = AlienCat(0, 0, 100, 100)
    alien.calm_down()
    alien.update(config.ALIEN_CALM_DURATION + 0.01)
    assert alien.state == AlienState.GONE


def test_swarm_cleared_when_all_aliens_gone():
    swarm = AlienSwarm(level=1)
    assert not swarm.cleared()
    for alien in swarm.aliens:
        alien.calm_down()
        alien.update(config.ALIEN_CALM_DURATION + 0.01)
    assert swarm.cleared()


def test_swarm_reverses_direction_at_right_edge():
    swarm = AlienSwarm(level=1)
    for alien in swarm.aliens:
        alien.rect.right = config.SCREEN_WIDTH - 5
    swarm.step_timer = swarm._current_interval()
    swarm.update(0.0)
    assert swarm.direction == -1


def test_hairball_moves_down_and_detects_offscreen():
    hb = Hairball(100, 0)
    assert not hb.offscreen
    hb.update(10.0)
    assert hb.offscreen
