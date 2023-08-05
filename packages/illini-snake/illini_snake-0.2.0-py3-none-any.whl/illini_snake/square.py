import numpy as np
import pygame

class Square:
    
    OFFSET = np.array([
        [-0.5, -0.5],
        [ 0.5, -0.5],
        [ 0.5,  0.5],
        [-0.5,  0.5]
    ])
    
    def __init__( self, x: int, y: int ):
        self.x = x
        self.y = y
        
    def __str__( self ):
        return str(self.x) + ' ' + str(self.y)
    
    def is_collision( self, other ) -> bool:
        """check if square is at the same location as another square"""
        return (self.x == other.x) and (self.y == other.y)

    def _get_pixel_center( self, screen ):
        """find the given pixel center of the square"""
        return np.array([
            screen.SQUARE_WIDTH * (self.x + 0.5),
            screen.SQUARE_WIDTH * (self.y + 0.5)
        ])

    @staticmethod
    def get_pixel_box( pixel_center, width ):
        """get the four coordinates for where to draw the square of given width"""

        width_offset = width * Square.OFFSET
        return pixel_center + width_offset

    def draw( self, screen, color, width ):
        """draw a square with given width/color centered in its grid location"""

        pixel_center = self._get_pixel_center( screen )
        box = Square.get_pixel_box( pixel_center, width )
           
        pygame.draw.polygon( 
            screen.pygame_screen,
            color,
            box
        )
    
    def draw_image( self, img, screen, width ):
        """draw a pre-scaled image centered a the grid location"""

        pixel_center = self._get_pixel_center( screen )
        box = Square.get_pixel_box( pixel_center, width )
        top_left = box[0]
        
        r = img.get_rect()
        h = r.height
        w = r.width

        if w<h:
            top_left[0] += (width-w)/2
        if h<w:
            top_left[1] += (width-h)/2

        screen.pygame_screen.blit( img, top_left )
