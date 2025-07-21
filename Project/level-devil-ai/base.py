import gym
from gym import spaces
import numpy as np
import pygame

class LevelDevilEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(LevelDevilEnv, self).__init__()
        
        # Game screen size
        self.width = 640
        self.height = 480

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Level Devil")

        # Define observation space (RGB image from game)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.height, self.width, 3), dtype=np.uint8)

        # Define action space (e.g., left, right, jump, do nothing)
        self.action_space = spaces.Discrete(4)  # 0: left, 1: right, 2: jump, 3: stay

        self.clock = pygame.time.Clock()
        self.done = False

        # Game variables (position, traps, etc.)
        self.reset()

    def reset(self):
        # Reset level, player, traps
        self.player_x = 100
        self.player_y = 300
        self.done = False
        observation = self._get_obs()
        return observation

    def step(self, action):
        reward = 0

        # Move player
        if action == 0: self.player_x -= 5  # left
        elif action == 1: self.player_x += 5  # right
        elif action == 2: self.player_y -= 5  # jump (fake physics)
        elif action == 3: pass  # do nothing

        # Fake gravity
        self.player_y += 3

        # Check for trap (e.g., fake floor)
        if self._hit_trap():
            reward = -1
            self.done = True
        elif self._reached_goal():
            reward = 1
            self.done = True

        observation = self._get_obs()
        info = {}

        return observation, reward, self.done, info

    def render(self, mode='human'):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.player_x, self.player_y, 30, 30))  # player
        pygame.draw.line(self.screen, (255, 255, 255), (0, 400), (640, 400), 5)  # floor
        pygame.display.flip()
        self.clock.tick(30)

    def _get_obs(self):
        return pygame.surfarray.array3d(pygame.display.get_surface())

    def _hit_trap(self):
        # Example: fall below screen
        return self.player_y > self.height

    def _reached_goal(self):
        # Example: reach far-right side
        return self.player_x >= self.width - 50

    def close(self):
        pygame.quit()
