from cat_invaders import sprites

ALL_BITMAPS = [
    sprites.ALIEN_CAT_A,
    sprites.ALIEN_CAT_B,
    sprites.ALIEN_CAT_CALM,
    sprites.PLAYER_CAT,
    sprites.PROJECTILE_CAT,
    sprites.HAIRBALL,
    sprites.MOTHERSHIP,
]


def test_bitmaps_are_rectangular():
    for bitmap in ALL_BITMAPS:
        widths = {len(row) for row in bitmap}
        assert len(widths) == 1, f"ragged bitmap rows: {bitmap}"


def test_bitmaps_use_known_characters():
    allowed = set(".XoH")
    for bitmap in ALL_BITMAPS:
        used = set("".join(bitmap))
        assert used <= allowed, f"unexpected characters {used - allowed} in {bitmap}"


def test_build_surface_matches_bitmap_dimensions():
    surface = sprites.build_surface(sprites.ALIEN_CAT_A, 4, (255, 0, 0))
    height = len(sprites.ALIEN_CAT_A)
    width = len(sprites.ALIEN_CAT_A[0])
    assert surface.get_size() == (width * 4, height * 4)
