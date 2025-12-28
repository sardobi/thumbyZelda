import time
import thumby

GAME_SPEED: int = 60
PLAYER_ATTACK_COOLDOWN: int = int(GAME_SPEED / 3)
PROJECTILE_SWORD_LIFETIME: int = GAME_SPEED * 2
PLAYER_BASE_HEALTH: int = 3


class SpriteBitmap:
    xDimension: int
    yDimension: int
    data: bytearray

    def __init__(self, xDimension: int, yDimension: int, data: bytearray):
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
        Up = SpriteBitmap(8, 8, bytearray([0, 0, 0, 32, 254, 32, 0, 0]))
        Down = SpriteBitmap(8, 8, bytearray([0, 0, 4, 127, 4, 0, 0, 0]))
        Left = SpriteBitmap(8, 8, bytearray([0, 16, 16, 16, 16, 56, 16, 16]))
        Right = SpriteBitmap(8, 8, bytearray([16, 16, 56, 16, 16, 16, 16, 0]))


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

    def __init__(self, xPos: int, yPos: int, facing: Direction):
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

        if self.health == self.max_health:
            swords.append(
                Sword(self.xPos, self.yPos, self.facing, PROJECTILE_SWORD_LIFETIME)
            )
        else:
            swords.append(Sword(self.xPos, self.yPos, self.facing))

        self._attack_cooldown = PLAYER_ATTACK_COOLDOWN


class Sword(Drawable):
    xPos: int
    yPos: int
    facing: Direction
    lifetime: int

    _move_speed: int = 1
    _time_alive: int = 0

    __directions_to_sprite__: dict[Direction, thumby.Sprite]

    def __init__(
        self,
        xPos: int,
        yPos: int,
        facing: Direction,
        lifetime: int = 8,
    ):
        self.xPos = xPos
        self.yPos = yPos
        self.facing = facing
        self.lifetime = lifetime

        self.__directions_to_sprite__ = {
            Directions.Up: SpriteBitmaps.Sword.Up.to_sprite(),
            Directions.Down: SpriteBitmaps.Sword.Down.to_sprite(),
            Directions.Left: SpriteBitmaps.Sword.Left.to_sprite(),
            Directions.Right: SpriteBitmaps.Sword.Right.to_sprite(),
        }
        self._sprite = self.__directions_to_sprite__[facing]
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


######################### Main loop #########################
thumby.display.setFPS(GAME_SPEED)

player = Player(0, 0, Directions.Down)
start_x = int((thumby.display.width / 2) - int(player.width() / 2))
start_y = int(thumby.display.height / 2) - int(player.height() / 2)
player.xPos = start_x
player.yPos = start_y

swords: list[Sword] = []

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

    for sword in swords:
        sword.step()
        sword.draw()

        if sword.expired():
            swords.remove(sword)

    player.step()
    player.draw()
    thumby.display.update()
