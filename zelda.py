import thumby

import sys

# necessary to allow other files to be imported when executed by Thumby
sys.path.append("/Games/Zelda")
import sprites

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


class Player(Drawable, Dynamic):
    xPos: int
    yPos: int
    facing: Direction

    health: int
    max_health: int

    _move_speed: int = 1
    _attack_cooldown: int = 0

    __directions_to_sprite__: dict[Direction, thumby.Sprite]

    def __init__(self, xPos: int, yPos: int, facing: Direction) -> None:
        Dynamic.__init__(self)

        self.xPos = xPos
        self.yPos = yPos
        self.facing = facing
        self.health = PLAYER_BASE_HEALTH
        self.max_health = PLAYER_BASE_HEALTH

        self.__directions_to_sprite__ = {
            Directions.Up: Sprites.Link.up(xPos, yPos),
            Directions.Down: Sprites.Link.down(xPos, yPos),
            Directions.Left: Sprites.Link.left(xPos, yPos),
            Directions.Right: Sprites.Link.right(xPos, yPos),
        }
        self._sprite = self.__directions_to_sprite__[facing]
        self._sprite.x = self.xPos
        self._sprite.y = self.yPos

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

        enemy_projectiles = {
            dynamic
            for dynamic in game.dynamics
            if isinstance(dynamic, EnemyShooterProjectile)
        }
        colliding_projectiles = {
            projectile
            for projectile in enemy_projectiles
            if projectile._sprite.x
            in range(self._sprite.x, self._sprite.x + self._sprite.width)
            and projectile._sprite.y
            in range(self._sprite.y, self._sprite.y + self._sprite.height)
        }
        for projectile in colliding_projectiles:
            projectile.expire()

        self.draw()

    def move(self, direction: Direction):
        if direction == Directions.Up:
            self.yPos -= self._move_speed
        elif direction == Directions.Down:
            self.yPos += self._move_speed
        elif direction == Directions.Left:
            self.xPos -= self._move_speed
        elif direction == Directions.Right:
            self.xPos += self._move_speed
        else:
            raise Exception("Unknown direction")

        self._sprite = self.__directions_to_sprite__[direction]
        self._sprite.x = self.xPos
        self._sprite.y = self.yPos
        self.facing = direction

    def attack(self, game: "Game"):
        if self._attack_cooldown > 0:
            return

        # sword shoots out at full health
        lifetime = PROJECTILE_LIFETIME if self.health == self.max_health else SWORD_SIZE

        game.dynamics.add(Sword(self.xPos, self.yPos, self.facing, lifetime))

        self._attack_cooldown = PLAYER_ATTACK_COOLDOWN


class EnemyShooter(Drawable, Dynamic):
    xPos: int
    yPos: int
    facing: Direction

    _attack_cooldown: int
    _turn_cooldown: int

    __directions_to_sprite__: dict[Direction, thumby.Sprite]

    def __init__(self, xPos: int, yPos: int, facing: Direction) -> None:
        Dynamic.__init__(self)

        self.xPos = xPos
        self.yPos = yPos
        self.facing = facing

        self.__directions_to_sprite__ = {
            Directions.Up: Sprites.EnemyShooter.up(xPos, yPos),
            Directions.Down: Sprites.EnemyShooter.down(xPos, yPos),
            Directions.Left: Sprites.EnemyShooter.left(xPos, yPos),
            Directions.Right: Sprites.EnemyShooter.right(xPos, yPos),
        }
        self._sprite = self.__directions_to_sprite__[facing]
        self._sprite.x = self.xPos
        self._sprite.y = self.yPos

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

        self.draw()

    def attack(self, game: "Game"):
        game.dynamics.add(EnemyShooterProjectile(self.xPos, self.yPos, self.facing))

    def turn(self):
        self.facing = Directions.rotate_cw(self.facing)
        self._sprite = self.__directions_to_sprite__[self.facing]
        self._sprite.x = self.xPos
        self._sprite.y = self.yPos


class Projectile(Drawable, Dynamic):
    xPos: int
    yPos: int
    facing: Direction
    lifetime: int

    _move_speed: int = 1
    _time_alive: int = 0

    def __init__(
        self,
        xPos: int,
        yPos: int,
        facing: Direction,
        sprite: thumby.Sprite,
        lifetime: int,
    ) -> None:
        Dynamic.__init__(self)

        self.xPos = xPos
        self.yPos = yPos
        self.facing = facing
        self.lifetime = lifetime

        self._sprite = sprite
        self._sprite.x = self.xPos
        self._sprite.y = self.yPos

    def expired(self) -> bool:
        return Dynamic.expired(self) or self._time_alive > self.lifetime

    def step(self, game: "Game"):
        self._time_alive += 1

        if self.facing == Directions.Up:
            self.yPos -= self._move_speed
        elif self.facing == Directions.Down:
            self.yPos += self._move_speed
        elif self.facing == Directions.Left:
            self.xPos -= self._move_speed
        elif self.facing == Directions.Right:
            self.xPos += self._move_speed

        self._sprite.x = self.xPos
        self._sprite.y = self.yPos

        self.draw()


class Sword(Projectile):
    def __init__(
        self,
        xPos: int,
        yPos: int,
        facing: Direction,
        lifetime: int,
    ) -> None:
        if facing == Directions.Up:
            sprite = Sprites.Sword.up(xPos, yPos)
        elif facing == Directions.Down:
            sprite = Sprites.Sword.down(xPos, yPos)
        elif facing == Directions.Left:
            sprite = Sprites.Sword.left(xPos, yPos)
        elif facing == Directions.Right:
            sprite = Sprites.Sword.right(xPos, yPos)
        else:
            raise Exception("Unknown direction")

        Projectile.__init__(self, xPos, yPos, facing, sprite, lifetime)


class EnemyShooterProjectile(Projectile):
    def __init__(
        self,
        xPos: int,
        yPos: int,
        facing: Direction,
    ):
        sprite = Sprites.enemy_shooter_projectile(xPos, yPos)
        Projectile.__init__(self, xPos, yPos, facing, sprite, PROJECTILE_LIFETIME)


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
