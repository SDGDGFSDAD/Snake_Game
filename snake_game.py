import pygame
import random
import time

# Pygame Initialization
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 660, 660
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
WHITE = (255, 255, 255)
MOVE_INTERVAL = 0.05
# FPS controller
fps = pygame.time.Clock()
# Define your desired logic updates per second and FPS
LOGIC_RATE = 10
FPS = 20
logic_timer = 0
logic_interval = 1.0 / LOGIC_RATE  # The time between logic updates

# Snake block size
BLOCK_SIZE = 20
direction_map = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_w:(0, -1),
    pygame.K_s:(0, 1),
    pygame.K_a:(-1, 0),
    pygame.K_d:(1, 0)

}

class Snake:
    def __init__(self):
        self.length = 3
        self.positions = [((WIDTH / 2)+1, (HEIGHT / 2)+1),((WIDTH / 2)+2, (HEIGHT / 2)+2),((WIDTH / 2)+3, (HEIGHT / 2)+3)]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.color = GREEN
        self.score = 0

    def head_position(self):
        return self.positions[0]

    # def turn(self, point):
    #     if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
    #         return
    #     else:
    #         self.direction = point


    def check_collision_with_boundaries(self):
        head_x, head_y = self.head_position()  # Call the method with ()
        # Adjust the condition to account for the snake's BLOCK_SIZE
        if head_x >= WIDTH-BLOCK_SIZE or head_x < 0 or head_y >= HEIGHT-BLOCK_SIZE or head_y < 0:
            return True  # Collision occurred
        return False  # No collision


    def move(self):
        cur = self.head_position()
        
        # Map the direction keys to actual (x, y) directions

        
        # Check that self.direction is in the direction_map, default to (0, 1) if not
        x, y = direction_map.get(self.direction, (0, 1))

        new = (((cur[0] + (x * BLOCK_SIZE)) % WIDTH), (cur[1] + (y * BLOCK_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        # Inside the game loop, after the snake has moved
        if self.check_collision_with_boundaries():
            # End the game or reset
            self.reset()  # For example, to reset the snake
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 3
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.score = 0
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])

    def draw(self, surface):
        for position in self.positions:
            snake_rect = pygame.Rect(position[0], position[1], BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, GREEN if position != self.head_position() else BLUE, snake_rect)
            snake_tail_rect = pygame.Rect(self.positions[-1][0], self.positions[-1][1], BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, PINK, snake_tail_rect)  # Draw the tail in PINK

            
    def handle_keys(self):
        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                print("Key pressed:", event.key)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.direction = pygame.K_UP
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.direction = pygame.K_DOWN
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.direction = pygame.K_LEFT
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.direction = pygame.K_RIGHT

    def get_score(self):
        return self.score

    def eat(self):
        self.length += 1
        self.score += 10


class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randint(0, (HEIGHT-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
        

    def draw(self, surface):
        apple_rect = pygame.Rect((self.position[0], self.position[1],BLOCK_SIZE, BLOCK_SIZE))
        # pygame.draw.rect(surface, self.color, r)
        # pygame.draw.rect(surface, BLACK, r, 1)
        pygame.draw.rect(surface, RED, apple_rect)


def draw_background(surface):
    surface.fill(BLACK)

def check_snake_colli_apply(snake_head_position,apple_position):
    snake_head_rect = pygame.Rect(snake_head_position, (BLOCK_SIZE, BLOCK_SIZE))
    apple_rect = pygame.Rect(apple_position, (BLOCK_SIZE, BLOCK_SIZE))
 
    if snake_head_rect.colliderect(apple_rect):
        return True 
    else:
        False


def main():
    snake = Snake()
    apple = Apple()

    while True:
        draw_background(screen)
        # Handle every event in the event queue
        snake.handle_keys()
        

        snake.move()
    

 
        # if snake_head_rect.colliderect(apple_rect):
        if check_snake_colli_apply(snake.head_position(),apple.position): 
            snake.eat()
            apple.randomize_position()

        snake.draw(screen)
        apple.draw(screen)

        # Display the score
        font = pygame.font.SysFont('Arial', 30)
        score_text = font.render("Score: {0}".format(snake.get_score()), True, WHITE)
        screen.blit(score_text, (5, 5))
    
        pygame.display.update()
        fps.tick(FPS)

if __name__ == "__main__":
    main()
