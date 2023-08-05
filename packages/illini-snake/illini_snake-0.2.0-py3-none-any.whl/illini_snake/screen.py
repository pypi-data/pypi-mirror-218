from illini_snake import Base
import pygame

class Screen( Base ):
    
    def __init__( self):
        Base.__init__( self )
        
        self.pixel_length = self.LENGTH * self.SQUARE_WIDTH
        self.pixel_width = self.WIDTH * self.SQUARE_WIDTH
        
        self.pygame_screen = pygame.display.set_mode( (self.pixel_length, self.pixel_width) )
        
        self.main_menu_Font = pygame.font.SysFont( 
            self.START_MENU['FONT'],
            self.START_MENU['FONT_SIZE'] 
        )
        self.score_display_Font = pygame.font.SysFont( 
            self.SCORE_DISPLAY['FONT'],
            self.SCORE_DISPLAY['FONT_SIZE'] 
        )
        
        self.food_options = []
        for i in range(self.LENGTH):
            for j in range(self.WIDTH):
                self.food_options.append( [i,j] )
        
    def fill( self ):
        """fill the entire screen with a background color"""
        
        self.pygame_screen.fill( self.COLOR )

    def draw_loading_screen( self ):

        Surface = self.main_menu_Font.render( 
            'Snake: press enter to play', 
            None, 
            self.START_MENU['FONT_COLOR']
        )
        x_centered = (self.pixel_length - Surface.get_rect().width)/2
        self.pygame_screen.blit( Surface, ( int(x_centered), int(self.pixel_width/2) ) ) 

    def draw_score( self, game ):
        """draw the score in the top left corner of the screen"""

        Surface = self.score_display_Font.render( 'Score: ' + str(game.score), None, self.SCORE_DISPLAY['FONT_COLOR'] )
        self.pygame_screen.blit( Surface, (5,5) ) 

    def flip( self ):
        pygame.display.flip()