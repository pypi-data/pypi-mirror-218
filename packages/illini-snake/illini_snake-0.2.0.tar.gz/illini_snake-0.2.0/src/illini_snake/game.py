from illini_snake import Base, Food, Snake, Screen, utils, settings
import os
import pygame

class Game(Base):

    def __init__( self ):
        Base.__init__( self )

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.running = True
        self.loading_screen = True
        self.clock = pygame.time.Clock()

        self.screen = Screen()
        self._load_logo_images()

    @property
    def score( self ):
        pass

    @score.getter
    def score( self ) -> int:
        """returns the length of the snake, calling `game.score` runs this method"""
        return len(self.snake)

    def _load_logo_images( self ):
        """preload all logo iamges"""

        filenames = os.listdir( utils.get_full_path(self.LOGOS_PATH ) )
        self.logo_images = []
        for filename in filenames:
            logo_path = utils.get_full_path( os.path.join(self.LOGOS_PATH, filename) )
            self.logo_images.append(utils.load_logo_file( logo_path, settings['Food']['WIDTH'] )) 

    def _make_new_food( self ):
        """Generate a new location for the food to go"""
        self.food.get_square( self.screen, self.snake, self )

    def run( self ):

        while self.running:

            # See if user clicked "X" on the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                
            # see if the user pressed a key            
            if pygame.key.get_focused():
                keys = pygame.key.get_pressed()

                if keys[pygame.K_z]: #exit entire program
                    self.running = False

                if keys[pygame.K_r]: #restart game
                    self.loading_screen = True

                if self.loading_screen: 

                    # user wants to start the game
                    if keys[pygame.K_RETURN]:
                        self.loading_screen = False
                        self.loop_start_time = pygame.time.get_ticks()

                        # initialize a new game!
                        self.snake = Snake( self.screen )
                        self.food = Food()
                        self._make_new_food()

                if not self.loading_screen:                
                    self.snake.process_key_press( keys )
                
            self.screen.fill()

            if self.loading_screen:
                self.screen.draw_loading_screen()

            if not self.loading_screen:
                
                # if enough time has passed for the snake to move
                current_time = pygame.time.get_ticks()
                if (current_time - self.loop_start_time) > (1000/self.snake.settings['SPEED']):
                    self.loop_start_time = current_time
                
                    # move the snake
                    self.snake.move( self.food, self.screen, self )
                    if self.food.is_eaten:
                        self._make_new_food()

                self.snake.draw( self.screen )
                self.food.draw( self.screen )
                self.screen.draw_score( self )

            # update the screen's display to show the changes
            self.screen.flip()
            self.clock.tick( self.settings['FPS'] )
            
        pygame.quit()  
    
    def game_over( self ):
        self.loading_screen = True
        print ('Final score: ' + str(self.score))