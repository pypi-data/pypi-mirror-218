from illini_snake import DIR
import pygame
import os

def get_full_path( rel_path ):
    """given a relative path, join it with the illini_snake DIR"""

    return os.path.join( DIR, rel_path )

def load_logo_file( filepath, width ):
    """load an image from a given filepath, proportionally scale it to a given width"""

    img = pygame.image.load( filepath )
    r = img.get_rect()
    h = r.height
    w = r.width

    # Scale
    scaling = width/max(h,w)
    return pygame.transform.smoothscale_by( img, scaling )
