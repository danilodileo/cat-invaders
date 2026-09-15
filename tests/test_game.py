import pygame

from cat_invaders.game import Game, GameState


def test_game_starts_in_menu():
    game = Game()
    assert game.state == GameState.MENU


def test_enter_from_menu_starts_playing():
    game = Game()
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
    assert game.state == GameState.PLAYING
    assert game.score == 0


def test_shooting_adds_a_projectile():
    game = Game()
    game.start_new_game()
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    assert len(game.projectiles) == 1


def test_calming_all_aliens_ends_the_level():
    game = Game()
    game.start_new_game()
    for alien in game.swarm.aliens:
        alien.calm_down()
    game.update(2.0)  # let the calm animation finish
    assert game.state == GameState.LEVEL_CLEAR


def test_losing_all_lives_ends_the_game():
    game = Game()
    game.start_new_game()
    for _ in range(10):
        game.player.take_hit()
        game.player.invulnerable = 0
    game.update(0.016)
    assert game.state == GameState.GAME_OVER
