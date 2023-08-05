from illini_snake import Base, Square, utils
import pygame

class Snake( Base ):

    KEY_DIRECTIONS = {
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right",
        pygame.K_UP: "up",
        pygame.K_DOWN: "down"
    }

    OPPOSITE_DIRECTIONS = {
        "left":"right",
        "right":"left",
        "up":"down",
        "down":"up"
    }
    
    def __init__( self, screen ):
        Base.__init__( self )

        # initialize the snake body list with one square
        self.body = [ Square( int(screen.LENGTH/2), int(screen.WIDTH/2) ) ]
        
        self.logo_image = utils.load_logo_file( utils.get_full_path(self.HEAD_PATH), self.WIDTH )
        self.eating_Sound = pygame.mixer.Sound( utils.get_full_path(self.EATING_SOUND_PATH) )

        self.nourishment_left = 0
        self.direction = None

    def __len__( self ):
        """overrides len() operator"""
        return len(self.body)

    def process_key_press( self, keys ):
        """process the keys pressed"""

        for key in Snake.KEY_DIRECTIONS:
            if keys[ key ]:
                direction = Snake.KEY_DIRECTIONS[ key ]
                opposite_direction = Snake.OPPOSITE_DIRECTIONS[ direction ]
                
                # change the snakes direction, as long it isn't trying to turn itself around 180 degrees
                if opposite_direction != self.momentum_direction:
                    self.direction = direction

    def move( self, food, screen, game ):
        
        # momentum direction can only be changed once per round, prevents snake from changing multiple times per loop
        self.momentum_direction = self.direction
        
        self._add_to_head()
        self._check_ate_food( food )
        self._check_remove_tail()

        if self._hit_boundaries( screen ):
            game.game_over()
            return
        if self._hit_self():
            game.game_over()
            return

    def _add_to_head( self ):

        """add another point to body in whatever direction snake is facing"""
        head = self.body[0]

        if self.direction == 'right':
            new_Sqaure = Square( head.x+1, head.y )
        elif self.direction == 'left':
            new_Sqaure = Square( head.x-1, head.y )
        elif self.direction == 'up':
            new_Sqaure = Square( head.x, head.y-1 ) #y-axis points down
        elif self.direction == 'down':
            new_Sqaure = Square( head.x, head.y+1 )
        else:
            new_Sqaure = Square( head.x, head.y )

        self.body.insert( 0, new_Sqaure )

    def _hit_boundaries( self, screen ) -> bool:

        """check if snake head hits the boundaries"""
        
        head = self.body[0]
        if head.x < 0: 
            print ('You hit the left side!')
            return True
        elif head.x >= screen.LENGTH: 
            print ('You hit the right side!')
            return True
        if head.y < 0: 
            print ('You hit the top!')
            return True
        elif head.y >= screen.WIDTH:
            print ('You hit the bottom!')
            return True
        return False

    def _hit_self( self ) -> bool:

        """check if snake head hits another part of the body"""
        for i in range(1, len(self.body)):
            if self.body[0].is_collision( self.body[i] ):
                print ('You hit yourself!')
                return True            
            
        return False

    def _check_ate_food( self, food ):

        if self.body[0].is_collision( food.square ):
            food.is_eaten = True
            self.nourishment_left += food.NOURISHMENT

            print ('nom nom nom')
            pygame.mixer.Sound.play( self.eating_Sound )

    def _check_remove_tail( self ):
        
        if self.nourishment_left > 0:
            self.nourishment_left -= 1            
        else:
            del self.body[-1]

    def draw( self, screen ):

        for square in self.body:
            square.draw( screen, self.COLOR, self.WIDTH )

        self.body[0].draw_image( self.logo_image, screen, self.WIDTH )
