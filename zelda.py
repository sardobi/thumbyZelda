import time
import thumby

GAME_SPEED: int = 60
PLAYER_ATTACK_COOLDOWN: int = int(GAME_SPEED / 3)
PLAYER_BASE_HEALTH: int = 3

PROJECTILE_LIFETIME: int = GAME_SPEED * 2
SWORD_SIZE: int = 8

ENEMY_SHOOTER_TURN_RATE: int = int(GAME_SPEED / 4) * 3
ENEMY_SHOOTER_ATTACK_RATE: int = int(GAME_SPEED / 4) * 3


class SpriteBitmap:
    xDimension: int
    yDimension: int
    data: bytearray

    def __init__(self, xDimension: int, yDimension: int, data: bytearray) -> None:
        self.xDimension = xDimension
        self.yDimension = yDimension
        self.data = data

    def to_sprite(self) -> thumby.Sprite:
        return thumby.Sprite(self.xDimension, self.yDimension, self.data)


class SpriteBitmaps:
    class Link:
        Up = SpriteBitmap(8, 8, bytearray([98, 244, 138, 145, 145, 138, 244, 98]))
        Down = SpriteBitmap(8, 8, bytearray([98, 244, 142, 157, 157, 142, 244, 98]))
        Left = SpriteBitmap(8, 8, bytearray([0, 4, 238, 157, 157, 137, 247, 0]))
        Right = SpriteBitmap(8, 8, bytearray([0, 247, 137, 157, 157, 238, 4, 0]))

    class Sword:
        Up = SpriteBitmap(
            SWORD_SIZE, SWORD_SIZE, bytearray([0, 0, 0, 32, 254, 32, 0, 0])
        )
        Down = SpriteBitmap(
            SWORD_SIZE, SWORD_SIZE, bytearray([0, 0, 4, 127, 4, 0, 0, 0])
        )
        Left = SpriteBitmap(
            SWORD_SIZE, SWORD_SIZE, bytearray([0, 16, 16, 16, 16, 56, 16, 16])
        )
        Right = SpriteBitmap(
            SWORD_SIZE, SWORD_SIZE, bytearray([16, 16, 56, 16, 16, 16, 16, 0])
        )

    class EnemyShooter:
        Up = SpriteBitmap(8, 8, bytearray([0, 252, 23, 2, 2, 23, 252, 0]))
        Down = SpriteBitmap(8, 8, bytearray([0, 252, 86, 162, 162, 86, 252, 0]))
        Left = SpriteBitmap(8, 8, bytearray([40, 236, 6, 18, 18, 6, 252, 0]))
        Right = SpriteBitmap(8, 8, bytearray([0, 252, 6, 18, 18, 6, 236, 40]))

    EnemyShooterProjectile: SpriteBitmap = SpriteBitmap(2, 2, bytearray([3, 3]))


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


class Player(Drawable):
    xPos: int
    yPos: int
    facing: Direction

    health: int
    max_health: int

    _move_speed: int = 1
    _attack_cooldown: int = 0

    __directions_to_sprite__: dict[Direction, thumby.Sprite]

    def __init__(self, xPos: int, yPos: int, facing: Direction) -> None:
        self.xPos = xPos
        self.yPos = yPos
        self.facing = facing
        self.health = PLAYER_BASE_HEALTH
        self.max_health = PLAYER_BASE_HEALTH

        self.__directions_to_sprite__ = {
            Directions.Up: SpriteBitmaps.Link.Up.to_sprite(),
            Directions.Down: SpriteBitmaps.Link.Down.to_sprite(),
            Directions.Left: SpriteBitmaps.Link.Left.to_sprite(),
            Directions.Right: SpriteBitmaps.Link.Right.to_sprite(),
        }
        self._sprite = self.__directions_to_sprite__[facing]
        self._sprite.x = self.xPos
        self._sprite.y = self.yPos

    def step(self):
        if self._attack_cooldown > 0:
            self._attack_cooldown -= 1

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

    def attack(self):
        if self._attack_cooldown > 0:
            return

        # sword shoots out at full health
        lifetime = PROJECTILE_LIFETIME if self.health == self.max_health else SWORD_SIZE

        projectiles.append(Sword(self.xPos, self.yPos, self.facing, lifetime))

        self._attack_cooldown = PLAYER_ATTACK_COOLDOWN


class EnemyShooter(Drawable):
    xPos: int
    yPos: int
    facing: Direction

    _attack_cooldown: int
    _turn_cooldown: int

    __directions_to_sprite__: dict[Direction, thumby.Sprite]

    def __init__(self, xPos: int, yPos: int, facing: Direction) -> None:
        self.xPos = xPos
        self.yPos = yPos
        self.facing = facing

        self.__directions_to_sprite__ = {
            Directions.Up: SpriteBitmaps.EnemyShooter.Up.to_sprite(),
            Directions.Down: SpriteBitmaps.EnemyShooter.Down.to_sprite(),
            Directions.Left: SpriteBitmaps.EnemyShooter.Left.to_sprite(),
            Directions.Right: SpriteBitmaps.EnemyShooter.Right.to_sprite(),
        }
        self._sprite = self.__directions_to_sprite__[facing]
        self._sprite.x = self.xPos
        self._sprite.y = self.yPos

        self._attack_cooldown = ENEMY_SHOOTER_ATTACK_RATE
        self._turn_cooldown = int(ENEMY_SHOOTER_TURN_RATE / 2)

    def step(self):
        if self._attack_cooldown > 0:
            self._attack_cooldown -= 1
        else:
            self.attack()
            self._attack_cooldown = ENEMY_SHOOTER_ATTACK_RATE

        if self._turn_cooldown > 0:
            self._turn_cooldown -= 1
        else:
            self.turn()
            self._turn_cooldown = ENEMY_SHOOTER_TURN_RATE

    def attack(self):
        projectiles.append(EnemyShooterProjectile(self.xPos, self.yPos, self.facing))

    def turn(self):
        self.facing = Directions.rotate_cw(self.facing)
        self._sprite = self.__directions_to_sprite__[self.facing]
        self._sprite.x = self.xPos
        self._sprite.y = self.yPos


class Projectile(Drawable):
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
        self.xPos = xPos
        self.yPos = yPos
        self.facing = facing
        self.lifetime = lifetime

        self._sprite = sprite
        self._sprite.x = self.xPos
        self._sprite.y = self.yPos

    def expired(self) -> bool:
        return self._time_alive > self.lifetime

    def step(self):
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


class Sword(Projectile):
    def __init__(
        self,
        xPos: int,
        yPos: int,
        facing: Direction,
        lifetime: int,
    ) -> None:
        if facing == Directions.Up:
            sprite = SpriteBitmaps.Sword.Up.to_sprite()
        elif facing == Directions.Down:
            sprite = SpriteBitmaps.Sword.Down.to_sprite()
        elif facing == Directions.Left:
            sprite = SpriteBitmaps.Sword.Left.to_sprite()
        elif facing == Directions.Right:
            sprite = SpriteBitmaps.Sword.Right.to_sprite()
        else:
            raise Exception("Unknown direction")

        super(Sword, self).__init__(xPos, yPos, facing, sprite, lifetime)


class EnemyShooterProjectile(Projectile):
    def __init__(
        self,
        xPos: int,
        yPos: int,
        facing: Direction,
    ):
        sprite = SpriteBitmaps.EnemyShooterProjectile.to_sprite()
        super(EnemyShooterProjectile, self).__init__(
            xPos, yPos, facing, sprite, PROJECTILE_LIFETIME
        )


######################### Main loop #########################
thumby.display.setFPS(GAME_SPEED)

player = Player(0, 0, Directions.Down)
start_x = int((thumby.display.width / 2) - int(player.width() / 2))
start_y = int(thumby.display.height / 2) - int(player.height() / 2)
player.xPos = start_x
player.yPos = start_y

enemy_shooter = EnemyShooter(start_x - 10, start_y, Directions.Right)

projectiles: list[Projectile] = []

while True:
    t0 = time.ticks_ms()  # Get time (ms)
    thumby.display.fill(0)  # Fill canvas to black

    if thumby.buttonU.pressed():
        player.move(Directions.Up)
    if thumby.buttonD.pressed():
        player.move(Directions.Down)
    if thumby.buttonL.pressed():
        player.move(Directions.Left)
    if thumby.buttonR.pressed():
        player.move(Directions.Right)
    if thumby.buttonA.pressed():
        player.attack()

    for projectile in projectiles:
        projectile.step()
        projectile.draw()

        if projectile.expired():
            projectiles.remove(projectile)

    enemy_shooter.step()
    enemy_shooter.draw()

    player.step()
    player.draw()
    thumby.display.update()
