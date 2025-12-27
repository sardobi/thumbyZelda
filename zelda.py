import time
import thumby
import math


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


class Direction:
    __value__: int

    def __init__(self, value: int):
        self.__value__ = value


class Directions:
    Up = Direction(1)
    Down = Direction(2)
    Left = Direction(3)
    Right = Direction(4)


class Player:
    xPos: int
    yPos: int
    facing: Direction

    _moveSpeed: int = 1

    _sprite: thumby.Sprite

    __directions_to_sprite__: dict[Direction, thumby.Sprite] = {
        Directions.Up: SpriteBitmaps.Link.Up.to_sprite(),
        Directions.Down: SpriteBitmaps.Link.Down.to_sprite(),
        Directions.Left: SpriteBitmaps.Link.Left.to_sprite(),
        Directions.Right: SpriteBitmaps.Link.Right.to_sprite(),
    }

    def __init__(self, xPos: int, yPos: int, facing: Direction):
        self.xPos = xPos
        self.yPos = yPos
        self.facing = facing

        self._sprite = self.__directions_to_sprite__[facing]

    def draw(self):
        thumby.display.drawSprite(self._sprite)

    def move(self, direction: Direction):
        if direction == Directions.Up:
            self.yPos += self._moveSpeed
        elif direction == Directions.Down:
            self.yPos -= self._moveSpeed
        elif direction == Directions.Left:
            self.xPos -= self._moveSpeed
        elif direction == Directions.Right:
            self.xPos += self._moveSpeed
        else:
            raise Exception("Unknown direction")

        self._sprite = self.__directions_to_sprite__[direction]
        self._sprite.x = self.xPos
        self._sprite.y = self.yPos


if __name__ == "__main__":
    # Set the FPS (without this call, the default fps is 30)
    thumby.display.setFPS(60)

    linkSprite = SpriteBitmaps.Link.Right.to_sprite()

    while 1:
        t0 = time.ticks_ms()  # Get time (ms)
        thumby.display.fill(0)  # Fill canvas to black

        bobRate = 250  # Set arbitrary bob rate (higher is slower)
        bobRange = 5  # How many pixels to move the sprite up/down (-5px ~ 5px)

        # Calculate number of pixels to offset sprite for bob animation
        bobOffset = math.sin(t0 / bobRate) * bobRange

        # Center the sprite using screen and bitmap dimensions and apply bob offset
        linkSprite.x = int((thumby.display.width / 2) - (linkSprite.width / 2))
        linkSprite.y = int(
            round((thumby.display.height / 2) - (linkSprite.width / 2) + bobOffset)
        )

        # Display the bitmap using bitmap data, position, and bitmap dimensions
        thumby.display.drawSprite(linkSprite)
        thumby.display.update()
