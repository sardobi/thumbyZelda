import thumby

GAME_SPEED: int = 60
PLAYER_ATTACK_COOLDOWN: int = int(GAME_SPEED / 3)
PLAYER_BASE_HEALTH: int = 3

PROJECTILE_LIFETIME: int = GAME_SPEED * 2
SWORD_SIZE: int = 8

# Standard width and height of a sprite
SPRITE_DIMS: int = 8

ENEMY_SHOOTER_TURN_RATE: int = int(GAME_SPEED / 4) * 3
ENEMY_SHOOTER_ATTACK_RATE: int = int(GAME_SPEED / 4) * 3


class Sprites:
    class Link:
        @classmethod
        def up(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(
                8, 8, bytearray([98, 244, 138, 145, 145, 138, 244, 98]), x, y, 0
            )

        @classmethod
        def down(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(
                8, 8, bytearray([98, 244, 142, 157, 157, 142, 244, 98]), x, y, 0
            )

        @classmethod
        def left(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(
                8, 8, bytearray([0, 4, 238, 157, 157, 137, 247, 0]), x, y, 0
            )

        @classmethod
        def right(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(
                8, 8, bytearray([0, 247, 137, 157, 157, 238, 4, 0]), x, y, 0
            )

    class Sword:
        @classmethod
        def up(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, bytearray([0, 0, 0, 32, 254, 32, 0, 0]), x, y, 0)

        @classmethod
        def down(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(8, 8, bytearray([0, 0, 4, 127, 4, 0, 0, 0]), x, y, 0)

        @classmethod
        def left(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(
                8, 8, bytearray([0, 16, 16, 16, 16, 56, 16, 16]), x, y, 0
            )

        @classmethod
        def right(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(
                8, 8, bytearray([16, 16, 56, 16, 16, 16, 16, 0]), x, y, 0
            )

    class EnemyShooter:
        @classmethod
        def up(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(
                8, 8, bytearray([0, 252, 23, 2, 2, 23, 252, 0]), x, y, 0
            )

        @classmethod
        def down(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(
                8, 8, bytearray([0, 252, 86, 162, 162, 86, 252, 0]), x, y, 0
            )

        @classmethod
        def left(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(
                8, 8, bytearray([40, 236, 6, 18, 18, 6, 252, 0]), x, y, 0
            )

        @classmethod
        def right(cls, x: int, y: int) -> thumby.Sprite:
            return thumby.Sprite(
                8, 8, bytearray([0, 252, 6, 18, 18, 6, 236, 40]), x, y, 0
            )

    @classmethod
    def enemy_shooter_projectile(cls, x: int, y: int) -> thumby.Sprite:
        return thumby.Sprite(8, 8, bytearray([0, 0, 0, 24, 24, 0, 0, 0]), x, y, 0)


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


class Hitbox:
    # inclusive limits
    x_min: int
    x_max: int
    y_min: int
    y_max: int

    def __init__(self, x_min: int, x_max: int, y_min: int, y_max: int) -> None:
        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min

        if x_max < x_min or y_max < y_min:
            raise Exception("bounds incorrect")

    def contains_point(self, x: int, y: int) -> bool:
        return x in range(self.x_min, self.x_max + 1) and y in range(
            self.y_min, self.y_max + 1
        )

    def overlaps(self, other: "Hitbox") -> bool:
        # no overlap if one of these inequalities is false
        return (
            self.x_min <= other.x_max
            and self.y_min <= other.y_max
            and self.x_max >= other.x_min
            and self.y_max >= other.y_min
        )


class Positional:
    """
    An object with position and dimensions
    """

    x_pos: int
    y_pos: int

    def __init__(self, x_pos: int, y_pos: int) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos

    def hitbox(self) -> Hitbox:
        """
        Get a Hitbox representing where collisions should be registered
        """
        raise Exception("Not implemented")


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
        Positional.__init__(self, x_pos, y_pos)

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

        game.dynamics.add(Sword(self.x_pos, self.y_pos, self.facing, lifetime))

        self._attack_cooldown = PLAYER_ATTACK_COOLDOWN

    def detect_collisions(self, game: "Game"):
        enemy_projectiles = {
            dynamic
            for dynamic in game.dynamics
            if isinstance(dynamic, EnemyShooterProjectile)
        }
        colliding_projectiles = {
            projectile
            for projectile in enemy_projectiles
            if projectile.hitbox().overlaps(self.hitbox())
        }

        for projectile in colliding_projectiles:
            projectile.expire()

    def hitbox(self) -> Hitbox:
        return Hitbox(
            self.x_pos,
            self.x_pos + self._sprite.width,
            self.y_pos,
            self.y_pos + self._sprite.height,
        )


class EnemyShooter(Drawable, Dynamic, Positional):
    x_pos: int
    y_pos: int
    facing: Direction

    _attack_cooldown: int
    _turn_cooldown: int

    __directions_to_sprite__: dict[Direction, thumby.Sprite]

    def __init__(self, x_pos: int, y_pos: int, facing: Direction) -> None:
        Dynamic.__init__(self)
        Positional.__init__(self, x_pos, y_pos)

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
        game.dynamics.add(EnemyShooterProjectile(self.x_pos, self.y_pos, self.facing))

    def turn(self):
        self.facing = Directions.rotate_cw(self.facing)
        self._sprite = self.__directions_to_sprite__[self.facing]
        self._sprite.x = self.x_pos
        self._sprite.y = self.y_pos

    def detect_collisions(self, game: "Game"):
        sword_projectiles = {
            dynamic for dynamic in game.dynamics if isinstance(dynamic, Sword)
        }

        colliding_projectiles = {
            projectile
            for projectile in sword_projectiles
            if projectile.hitbox().overlaps(self.hitbox())
        }

        for sword in colliding_projectiles:
            sword.expire()

        if len(colliding_projectiles) > 0:
            self.expire()

    def hitbox(self) -> Hitbox:
        return Hitbox(
            self.x_pos,
            self.x_pos + self._sprite.width,
            self.y_pos,
            self.y_pos + self._sprite.height,
        )


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
        facing: Direction,
        sprite: thumby.Sprite,
        lifetime: int,
    ) -> None:
        Dynamic.__init__(self)
        Positional.__init__(self, x_pos, y_pos)

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

        Projectile.__init__(self, x_pos, y_pos, facing, sprite, lifetime)

    def hitbox(self) -> Hitbox:
        return Hitbox(
            self.x_pos,
            self.x_pos + self._sprite.width,
            self.y_pos,
            self.y_pos + self._sprite.height,
        )


class EnemyShooterProjectile(Projectile):
    def __init__(
        self,
        x_pos: int,
        y_pos: int,
        facing: Direction,
    ):
        sprite = Sprites.enemy_shooter_projectile(x_pos, y_pos)
        Projectile.__init__(self, x_pos, y_pos, facing, sprite, PROJECTILE_LIFETIME)

    def hitbox(self) -> Hitbox:
        # smaller hitbox matching sprite
        return Hitbox(
            self.x_pos + 3,
            self.x_pos + 5,
            self.y_pos + 3,
            self.y_pos + 5,
        )


class Game:
    dynamics: set[Dynamic]

    def __init__(self) -> None:
        self.dynamics = set()

    def run(self):
        """
        Main entrypoint for the game
        """
        thumby.display.setFPS(GAME_SPEED)

        start_x = int((thumby.display.width / 2) - int(SPRITE_DIMS / 2))
        start_y = int(thumby.display.height / 2) - int(SPRITE_DIMS / 2)

        player = Player(start_x, start_y, Directions.Down)
        self.dynamics.add(player)

        enemy_shooter = EnemyShooter(start_x - 10, start_y, Directions.Right)
        self.dynamics.add(enemy_shooter)

        while True:
            thumby.display.fill(0)  # Fill canvas to black

            for dynamic in self.dynamics:
                if dynamic.expired():
                    self.dynamics.remove(dynamic)

                dynamic.step(self)

            thumby.display.update()


######################### Main loop #########################
game = Game()
game.run()
