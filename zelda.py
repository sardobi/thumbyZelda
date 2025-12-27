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
        Up = SpriteBitmap(8, 8, bytearray([98,244,138,145,145,138,244,98]))
        Down = SpriteBitmap(8, 8, bytearray([98,244,142,157,157,142,244,98]))
        Left = SpriteBitmap(8, 8, bytearray([0,4,238,157,157,137,247,0]))
        Right = SpriteBitmap(8, 8, bytearray([0,247,137,157,157,238,4,0]))

# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(60)

linkSprite = SpriteBitmaps.Link.Right.to_sprite()

while(1):
    t0 = time.ticks_ms()   # Get time (ms)
    thumby.display.fill(0) # Fill canvas to black

    bobRate = 250 # Set arbitrary bob rate (higher is slower)
    bobRange = 5  # How many pixels to move the sprite up/down (-5px ~ 5px)

    # Calculate number of pixels to offset sprite for bob animation
    bobOffset = math.sin(t0 / bobRate) * bobRange

    # Center the sprite using screen and bitmap dimensions and apply bob offset
    linkSprite.x = int((thumby.display.width/2) - (linkSprite.width/2))
    linkSprite.y = int(round((thumby.display.height/2) - (linkSprite.width/2) + bobOffset))

    # Display the bitmap using bitmap data, position, and bitmap dimensions
    thumby.display.drawSprite(linkSprite)
    thumby.display.update()
