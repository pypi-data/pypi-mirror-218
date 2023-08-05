from illini_snake import Base, Square
import random

class Food(Base):
    
    def __init__( self ):
        Base.__init__( self )
        self.is_eaten = True

    def get_square( self, screen, snake, game ):
        """resets `logo_image` and `square` with randomly generated values"""

        self.is_eaten = False
        self.logo_image = random.choice( game.logo_images )

        #try randomly picking a spot the snake is not on
        for i in range(3):
            x = random.randint( 0, screen.LENGTH-1 )
            y = random.randint( 0, screen.WIDTH-1 )
            self.square = Square( x, y )

            good_food = True
            for square in snake.body:
                if self.square.is_collision( square ):
                    good_food = False
                    break

            if good_food:
                return
        
        #otherwise, try every possibility
        possibilities = screen.food_options.copy()
        for square in snake.body:
            possibilities.remove( [square.x, square.y] )
        
        if len(possibilities) > 0:
            choice = random.choice( possibilities )
            self.square = Square( choice[0], choice[1] )


    def draw( self, screen ):
        self.square.draw_image( self.logo_image, screen, self.settings['WIDTH'] )
