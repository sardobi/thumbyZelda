import thumby

GAME_SPEED: int = 60
PLAYER_ATTACK_COOLDOWN: int = int(GAME_SPEED / 3)
PLAYER_BASE_HEALTH: int = 3

PROJECTILE_LIFETIME: int = GAME_SPEED * 2
SWORD_SIZE: int = 8

# width and height of the player
PLAYER_SIZE: int = 8

# width and height of enemy shooters
ENEMY_SHOOTER_SIZE: int = 8
ENEMY_SHOOTER_TURN_RATE: int = int(GAME_SPEED / 4) * 3
ENEMY_SHOOTER_ATTACK_RATE: int = int(GAME_SPEED / 4) * 3

# width and height of enemy shooter projectiles
ENEMY_SHOOTER_PROJECTILE_SIZE: int = 2


class Sprites:
    class Link:
        BITMAP_UP = bytearray([98, 244, 138, 145, 145, 138, 244, 98])
        BITMAP_DOWN = bytearray([98, 244, 142, 157, 157, 142, 244, 98])
        BITMAP_LEFT = bytearray([0, 4, 238, 157, 157, 137, 247, 0])
        BITMAP_RIGHT = bytearray([0, 247, 137, 157, 157, 238, 4, 0])

        @classmethod
        def up(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, cls.BITMAP_UP, x, y, 0)

        @classmethod
        def down(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, cls.BITMAP_DOWN, x, y, 0)

        @classmethod
        def left(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, cls.BITMAP_LEFT, x, y, 0)

        @classmethod
        def right(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, cls.BITMAP_RIGHT, x, y, 0)

    class Sword:
        BITMAP_UP = bytearray([0, 0, 0, 32, 254, 32, 0, 0])
        BITMAP_DOWN = bytearray([0, 0, 4, 127, 4, 0, 0, 0])
        BITMAP_LEFT = bytearray([0, 16, 16, 16, 16, 56, 16, 16])
        BITMAP_RIGHT = bytearray([16, 16, 56, 16, 16, 16, 16, 0])

        @classmethod
        def up(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, cls.BITMAP_UP, x, y, 0)

        @classmethod
        def down(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, cls.BITMAP_DOWN, x, y, 0)

        @classmethod
        def left(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, cls.BITMAP_LEFT, x, y, 0)

        @classmethod
        def right(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, cls.BITMAP_RIGHT, x, y, 0)

    class EnemyShooter:
        BITMAP_UP = bytearray([0, 252, 23, 2, 2, 23, 252, 0])
        BITMAP_DOWN = bytearray([0, 252, 86, 162, 162, 86, 252, 0])
        BITMAP_LEFT = bytearray([40, 236, 6, 18, 18, 6, 252, 0])
        BITMAP_RIGHT = bytearray([0, 252, 6, 18, 18, 6, 236, 40])

        @classmethod
        def up(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, cls.BITMAP_UP, x, y, 0)

        @classmethod
        def down(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, cls.BITMAP_DOWN, x, y, 0)

        @classmethod
        def left(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, cls.BITMAP_LEFT, x, y, 0)

        @classmethod
        def right(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, cls.BITMAP_RIGHT, x, y, 0)

    BITMAP_ENEMY_PROJECTILE = bytearray([0, 0, 0, 24, 24, 0, 0, 0])

    @classmethod
    def enemy_shooter_projectile(cls, x: int, y: int) -> thumby.Sprite:
        return thumby.Sprite(8, 8, cls.BITMAP_ENEMY_PROJECTILE, x, y, 0)

    class UI:
        BITMAP_HEART = bytearray([9, 3, 9])

        @classmethod
        def heart(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(3, 4, cls.BITMAP_HEART, x, y)


class Direction:
    __value__: int

    def __init__(self, value: int) -> None:
        self.__value__ = value


class Directions:
    Up = Direction(1)
    Down = Direction(2)
    Left = Direction(3)
    Right = Direction(4)

    @classmethod
    def rotate_cw(cls, direction: Direction) -> Direction:
        if direction == Directions.Up:
            return Directions.Right
        if direction == Directions.Down:
            return Directions.Left
        if direction == Directions.Left:
            return Directions.Up
        if direction == Directions.Right:
            return Directions.Down

        raise Exception("Unknown direction")

    @classmethod
    def rotate_ccw(cls, direction: Direction) -> Direction:
        if direction == Directions.Up:
            return Directions.Left
        if direction == Directions.Down:
            return Directions.Right
        if direction == Directions.Left:
            return Directions.Down
        if direction == Directions.Right:
            return Directions.Up

        raise Exception("Unknown direction")


class Drawable:
    _sprite: thumby.Sprite

    def width(self) -> int:
        return self._sprite.width

    def height(self) -> int:
        return self._sprite.height

    def draw(self):
        thumby.display.drawSprite(self._sprite)


class Positional:
    """
    An object with position and dimensions
    """

    x_pos: int
    y_pos: int
    width: int
    height: int

    def __init__(self, x_pos: int, y_pos: int, width: int, height: int) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height

    def x_min(self) -> int:
        return self.x_pos

    def y_min(self) -> int:
        return self.y_pos

    def x_max(self) -> int:
        return self.x_pos + self.width

    def y_max(self) -> int:
        return self.y_pos + self.height

    def overlaps(self, other: "Positional") -> bool:
        """
        Whether two Positionals overlap
        """
        # no overlap if one of these inequalities is false
        return (
            self.x_min() <= other.x_max()
            and self.y_min() <= other.y_max()
            and self.x_max() >= other.x_min()
            and self.y_max() >= other.y_min()
        )


class Dynamic:
    _expired: bool

    def __init__(self) -> None:
        self._expired = False

    def step(self, game: "Game") -> None:
        """
        Perform per-frame processing.

        :param game: Game state
        """
        pass

    def expired(self) -> bool:
        """
        Whether this Dynamic should be cleaned up
        """
        return self._expired

    def expire(self) -> None:
        """
        Mark this Dynamic as expired
        """
        self._expired = True


class Player(Drawable, Dynamic, Positional):
    facing: Direction

    health: int
    max_health: int

    _move_speed: int = 1
    _attack_cooldown: int = 0

    __directions_to_sprite__: dict[Direction, thumby.Sprite]

    def __init__(self, x_pos: int, y_pos: int, facing: Direction) -> None:
        Dynamic.__init__(self)
        Positional.__init__(self, x_pos, y_pos, PLAYER_SIZE, PLAYER_SIZE)

        self.facing = facing
        self.health = PLAYER_BASE_HEALTH
        self.max_health = PLAYER_BASE_HEALTH

        self.__directions_to_sprite__ = {
            Directions.Up: Sprites.Link.up(x_pos, y_pos),
            Directions.Down: Sprites.Link.down(x_pos, y_pos),
            Directions.Left: Sprites.Link.left(x_pos, y_pos),
            Directions.Right: Sprites.Link.right(x_pos, y_pos),
        }
        self._sprite = self.__directions_to_sprite__[facing]
        self._sprite.x = self.x_pos
        self._sprite.y = self.y_pos

    def step(self, game: "Game"):
        if self._attack_cooldown > 0:
            self._attack_cooldown -= 1

        if thumby.buttonU.pressed():
            self.move(Directions.Up)
        if thumby.buttonD.pressed():
            self.move(Directions.Down)
        if thumby.buttonL.pressed():
            self.move(Directions.Left)
        if thumby.buttonR.pressed():
            self.move(Directions.Right)
        if thumby.buttonA.pressed():
            self.attack(game)

        self.detect_collisions(game)

        if self.health <= 0:
            self.expire()

        self.draw()

    def move(self, direction: Direction):
        if direction == Directions.Up:
            self.y_pos -= self._move_speed
        elif direction == Directions.Down:
            self.y_pos += self._move_speed
        elif direction == Directions.Left:
            self.x_pos -= self._move_speed
        elif direction == Directions.Right:
            self.x_pos += self._move_speed
        else:
            raise Exception("Unknown direction")

        self._sprite = self.__directions_to_sprite__[direction]
        self._sprite.x = self.x_pos
        self._sprite.y = self.y_pos
        self.facing = direction

    def attack(self, game: "Game"):
        if self._attack_cooldown > 0:
            return

        # sword shoots out at full health
        lifetime = PROJECTILE_LIFETIME if self.health == self.max_health else SWORD_SIZE

        game.dynamics.append(Sword(self.x_pos, self.y_pos, self.facing, lifetime))

        self._attack_cooldown = PLAYER_ATTACK_COOLDOWN

    def detect_collisions(self, game: "Game"):
        for dynamic in game.dynamics:
            if not isinstance(dynamic, EnemyShooterProjectile):
                continue

            colliding = dynamic.overlaps(self)
            if not colliding:
                continue

            # colliding with enemy projectile
            dynamic.expire()
            self.health -= 1


class EnemyShooter(Drawable, Dynamic, Positional):
    x_pos: int
    y_pos: int
    facing: Direction

    _attack_cooldown: int
    _turn_cooldown: int

    __directions_to_sprite__: dict[Direction, thumby.Sprite]

    def __init__(self, x_pos: int, y_pos: int, facing: Direction) -> None:
        Dynamic.__init__(self)
        Positional.__init__(self, x_pos, y_pos, ENEMY_SHOOTER_SIZE, ENEMY_SHOOTER_SIZE)

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.facing = facing

        self.__directions_to_sprite__ = {
            Directions.Up: Sprites.EnemyShooter.up(x_pos, y_pos),
            Directions.Down: Sprites.EnemyShooter.down(x_pos, y_pos),
            Directions.Left: Sprites.EnemyShooter.left(x_pos, y_pos),
            Directions.Right: Sprites.EnemyShooter.right(x_pos, y_pos),
        }
        self._sprite = self.__directions_to_sprite__[facing]
        self._sprite.x = self.x_pos
        self._sprite.y = self.y_pos

        self._attack_cooldown = ENEMY_SHOOTER_ATTACK_RATE
        self._turn_cooldown = int(ENEMY_SHOOTER_TURN_RATE / 2)

    def step(self, game: "Game"):
        if self._attack_cooldown > 0:
            self._attack_cooldown -= 1
        else:
            self.attack(game)
            self._attack_cooldown = ENEMY_SHOOTER_ATTACK_RATE

        if self._turn_cooldown > 0:
            self._turn_cooldown -= 1
        else:
            self.turn()
            self._turn_cooldown = ENEMY_SHOOTER_TURN_RATE

        self.detect_collisions(game)
        self.draw()

    def attack(self, game: "Game"):
        game.dynamics.append(
            EnemyShooterProjectile(self.x_pos, self.y_pos, self.facing)
        )

    def turn(self):
        self.facing = Directions.rotate_cw(self.facing)
        self._sprite = self.__directions_to_sprite__[self.facing]
        self._sprite.x = self.x_pos
        self._sprite.y = self.y_pos

    def detect_collisions(self, game: "Game"):
        for dynamic in game.dynamics:
            if not isinstance(dynamic, Sword):
                continue

            colliding = dynamic.overlaps(self)
            if not colliding:
                continue

            # colliding with sword
            dynamic.expire()
            self.expire()


class Projectile(Drawable, Dynamic, Positional):
    x_pos: int
    y_pos: int
    facing: Direction
    lifetime: int

    _move_speed: int = 1
    _time_alive: int = 0

    def __init__(
        self,
        x_pos: int,
        y_pos: int,
        width: int,
        height: int,
        facing: Direction,
        sprite: thumby.Sprite,
        lifetime: int,
    ) -> None:
        Dynamic.__init__(self)
        Positional.__init__(self, x_pos, y_pos, width, height)

        self.facing = facing
        self.lifetime = lifetime

        self._sprite = sprite
        self._sprite.x = self.x_pos
        self._sprite.y = self.y_pos

    def expired(self) -> bool:
        return Dynamic.expired(self) or self._time_alive > self.lifetime

    def step(self, game: "Game"):
        self._time_alive += 1

        if self.facing == Directions.Up:
            self.y_pos -= self._move_speed
        elif self.facing == Directions.Down:
            self.y_pos += self._move_speed
        elif self.facing == Directions.Left:
            self.x_pos -= self._move_speed
        elif self.facing == Directions.Right:
            self.x_pos += self._move_speed

        self._sprite.x = self.x_pos
        self._sprite.y = self.y_pos

        self.draw()


class Sword(Projectile):
    def __init__(
        self,
        x_pos: int,
        y_pos: int,
        facing: Direction,
        lifetime: int,
    ) -> None:
        if facing == Directions.Up:
            sprite = Sprites.Sword.up(x_pos, y_pos)
        elif facing == Directions.Down:
            sprite = Sprites.Sword.down(x_pos, y_pos)
        elif facing == Directions.Left:
            sprite = Sprites.Sword.left(x_pos, y_pos)
        elif facing == Directions.Right:
            sprite = Sprites.Sword.right(x_pos, y_pos)
        else:
            raise Exception("Unknown direction")

        Projectile.__init__(
            self, x_pos, y_pos, SWORD_SIZE, SWORD_SIZE, facing, sprite, lifetime
        )


class EnemyShooterProjectile(Projectile):
    def __init__(
        self,
        x_pos: int,
        y_pos: int,
        facing: Direction,
    ):
        sprite = Sprites.enemy_shooter_projectile(x_pos, y_pos)
        Projectile.__init__(
            self,
            x_pos,
            y_pos,
            ENEMY_SHOOTER_PROJECTILE_SIZE,
            ENEMY_SHOOTER_PROJECTILE_SIZE,
            facing,
            sprite,
            PROJECTILE_LIFETIME,
        )


class UI:
    def draw(self, player: Player) -> None:
        self._draw_base_ui()

        self._draw_hearts(player.health)

    def _draw_base_ui(self) -> None:
        # bar of height 4 at top of screen
        for y in range(0, 4):
            thumby.display.drawLine(0, y, thumby.display.width, y, 1)

        # bar of height 1 at bottom of screen
        thumby.display.drawLine(
            0,
            thumby.display.height - 1,
            thumby.display.width,
            thumby.display.height - 1,
            1,
        )

    def _draw_hearts(self, health: int) -> None:
        heart_x = 1
        heart_y = 0
        for _ in range(0, health):
            thumby.display.drawSprite(Sprites.UI.heart(heart_x, heart_y))
            heart_x += 4


class Game:
    player: Player
    dynamics: list[Dynamic]
    ui: UI

    def __init__(self) -> None:
        self.dynamics = []
        self.ui = UI()

        start_x = int((thumby.display.width / 2) - int(PLAYER_SIZE / 2))
        start_y = int(thumby.display.height / 2) - int(PLAYER_SIZE / 2)

        player = Player(start_x, start_y, Directions.Down)
        self.player = player
        self.dynamics.append(player)

        enemy_shooter = EnemyShooter(start_x - 10, start_y, Directions.Right)
        self.dynamics.append(enemy_shooter)

    def run(self):
        """
        Main entrypoint for the game
        """
        thumby.display.setFPS(GAME_SPEED)

        while True:
            thumby.display.fill(0)  # Fill canvas to black

            self.dynamics[:] = [d for d in self.dynamics if not d.expired()]

            for dynamic in self.dynamics:
                dynamic.step(self)

            # draw UI last, on top
            self.ui.draw(self.player)
            thumby.display.update()


######################### Main loop #########################
game = Game()
game.run()
