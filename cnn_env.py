import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import random
from snake_game import Snake, Apple, WIDTH, HEIGHT, BLOCK_SIZE,direction_map,screen ,draw_background,FPS # Import relevant components from your game
import time
class SnakeEnv(gym.Env):
    #metadata = {'render.modes': ['human', 'rgb_array'], 'video.frames_per_second': 50}

    def __init__(self,render_mode=None):
        super(SnakeEnv, self).__init__()
        self.render_mode = render_mode
        self.fps = pygame.time.Clock().tick(FPS)
        self.snake = Snake()
        self.apple = Apple()
        self.game_over = False
        self.total_reward=0
        self.clock=pygame.time.Clock()
        self.episode_counter=0
        # Define action and observation space
        # They must be gym.spaces objects
        self.action_space = spaces.Discrete(4)  # Example for four directions
        # Example for observation space, which might be the raw pixels
        self.observation_space = spaces.Box(low=0, high=255, shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.map_area=WIDTH*HEIGHT

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randint(0, (HEIGHT-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
        return self.position
    def get_observation(self):
        
        draw_background(screen)
        self.snake.draw(screen)
        self.apple.draw(screen)
        pygame.display.update()

        pixel_array = pygame.surfarray.array3d(pygame.display.get_surface())
        pixel_array = pixel_array.transpose([1, 0, 2])
        pixel_array = pixel_array / 255.0
        return pixel_array.astype(np.uint8)
    
    def reset(self,seed=None):

        self.episode_counter+=1
        self.total_reward = 0
        self.snake.length = 3
        # Reset snake to the center, with each segment behind the head
        # assuming the game starts with the snake moving to the right
        self.snake.positions = [((WIDTH // 2 - i * BLOCK_SIZE), HEIGHT // 2) for i in range(self.snake.length)]
        self.score = 0
        self.apple.position = self.randomize_position()
        self.direction = pygame.K_RIGHT  # Start with the snake moving right
        self.game_over = False

        # Calculate the initial distance between the snake head and the apple
        head_x, head_y = self.snake.head_position()
      
        apple_x, apple_y = self.apple.position
        self.previous_distance = np.sqrt((head_x - apple_x) ** 2 + (head_y - apple_y) ** 2)

        observation = self.get_observation()
        info = {'total_reward': self.total_reward, 'previous_distance': self.previous_distance}
        return observation, info  # return observation and info

    

    
    def step(self, action):
        assert self.action_space.contains(action), f"{action} is an invalid action"

        # Map the action to a direction
        # Assuming that 0: Up, 1: Down, 2: Left, 3: Right
        action_map = {
            0: pygame.K_UP,
            1: pygame.K_DOWN,
            2: pygame.K_LEFT,
            3: pygame.K_RIGHT
        }
        truncated=False
        self.direction = action_map[action]

        # Now, move the snake using the updated direction
        cur = self.snake.head_position()
        x, y = direction_map.get(self.direction, (0, 1))
        new_head_pos = (((cur[0] + (x * BLOCK_SIZE)) % WIDTH), (cur[1] + (y * BLOCK_SIZE)) % HEIGHT)

        # Insert the new position
        self.snake.positions.insert(0, new_head_pos)
        # Compute the distance to the apple
        apple_x, apple_y = self.apple.position
        head_x, head_y = self.snake.head_position()
        current_distance = np.sqrt((head_x - apple_x) ** 2 + (head_y - apple_y) ** 2)

        # Check for collision with self or walls
        if  head_x >= WIDTH-BLOCK_SIZE or head_x < 0 or head_y >= HEIGHT-BLOCK_SIZE or head_y < 0\
            or ( len(self.snake.positions) > 2 and (head_x, head_y) in self.snake.positions[2:]):
            self.game_over = True
            reward = -10
            self.total_reward += reward
            print('Collision Reward: ', reward,' Total Rewards: ',self.total_reward)
            
            abs=self.get_observation()
            return abs, reward, self.game_over, truncated ,{'total_reward': self.total_reward}



        # Check if the snake got the apple
        if current_distance == 0:
        
            (head_x, head_y) = (apple_x, apple_y)
            self.score += 1
            reward = 10
            self.total_reward += reward  # Update total reward
            print('Eat Apple Reward: ', reward,' Total Rewards: ',self.total_reward)
        else:
            # Remove the last segment of the snake if not growing, this moves the snake forward.
            self.snake.positions.pop()

            # Calculate the difference in distance
            diff_distance = current_distance - self.previous_distance

            # Reward or penalty based on the change in distance to the apple
            reward = -diff_distance / 2
            self.total_reward += reward
            self.previous_distance = current_distance  # Update the previous distance
            print('not eat or die reward: ', reward,' Total Rewards: ',self.total_reward)
        info = {'total_reward': self.total_reward, 'previous_distance': self.previous_distance}

        #self.render()

        return self.get_observation(), self.total_reward, self.game_over,truncated, info




    def render(self, mode='human'):
        # Add a sleep in the render method to slow down the rendering
        if self.render_mode == 'human':
            time.sleep(0.1) 

    
    def close(self):
         pygame.quit()

# Add additional necessary methods and class definitions if neededd
