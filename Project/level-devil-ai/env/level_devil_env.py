import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame

class LevelDevilEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(LevelDevilEnv, self).__init__()
        self.width = 640
        self.height = 480

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Level Devil")

        self.observation_space = spaces.Box(low=0, high=255, shape=(self.height, self.width, 3), dtype=np.uint8)
        self.action_space = spaces.Discrete(4)

        self.clock = pygame.time.Clock()
        self.done = False

        self.spikes = [(200, 400), (350, 400)]
        self.fake_floors = [(500, 400, 50)]
        self.moving_platform = [250, 350, 60, 1]
        self.disappearing_tile = [400, 400, 50]
        self.tile_visible = True
        self.tile_timer = 0

        self.reset()

    def _update_moving_platform(self):
        x, y, width, direction = self.moving_platform
        x += direction * 2
        if x <= 100 or x + width >= self.width - 100:
            direction *= -1
        self.moving_platform = [x, y, width, direction]

    def _get_obs(self):
        return pygame.surfarray.array3d(pygame.display.get_surface()).transpose(1, 0, 2)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.player_x = 100
        self.player_y = 350  # Positioned just above the ground
        self.done = False
        return self._get_obs(), {}

    def step(self, action):
        reward = 0.0
        if action == 0: self.player_x -= 5
        elif action == 1: self.player_x += 5
        elif action == 2: self.player_y -= 10

        self.player_y += 3

        mp_x, mp_y, mp_w, mp_dir = self.moving_platform
        if mp_x <= self.player_x <= mp_x + mp_w and abs(self.player_y - mp_y) < 10:
            self.player_x += mp_dir * 2

        self._update_moving_platform()

        self.tile_timer += 1
        if self.tile_timer >= 30:
            self.tile_visible = not self.tile_visible
            self.tile_timer = 0

        if self._hit_trap():
            reward = -1
            self.done = True
        elif self._reached_goal():
            reward = 1
            self.done = True
        else:
            reward = 0.01 + (self.player_x / self.width) * 0.05

        return self._get_obs(), reward, self.done, False, {}

    def render(self, mode='human'):
        self.screen.fill((0, 0, 0))
        pygame.draw.line(self.screen, (255, 255, 255), (0, 400), (self.width, 400), 5)
        pygame.draw.rect(self.screen, (0, 255, 0), (self.player_x, self.player_y, 30, 30))

        for fx, fy, fw in self.fake_floors:
            pygame.draw.line(self.screen, (150, 150, 150), (fx, fy), (fx + fw, fy), 5)

        if self.tile_visible:
            tx, ty, tw = self.disappearing_tile
            pygame.draw.line(self.screen, (255, 255, 0), (tx, ty), (tx + tw, ty), 5)

        mp_x, mp_y, mp_w, _ = self.moving_platform
        pygame.draw.rect(self.screen, (0, 0, 255), (mp_x, mp_y, mp_w, 10))

        for sx, sy in self.spikes:
            pygame.draw.circle(self.screen, (255, 0, 0), (sx, sy), 5)

        pygame.display.flip()
        self.clock.tick(30)

    def _hit_trap(self):
        if self.player_y > self.height:
            return True
        for spike_x, spike_y in self.spikes:
            if abs(self.player_x - spike_x) < 20 and self.player_y >= spike_y - 30:
                return True
        for fx, fy, fw in self.fake_floors:
            if fx <= self.player_x <= fx + fw and abs(self.player_y - fy) < 10:
                return True
        if not self.tile_visible:
            tx, ty, tw = self.disappearing_tile
            if tx <= self.player_x <= tx + tw and abs(self.player_y - ty) < 10:
                return True
        return False

    def _reached_goal(self):
        return self.player_x >= self.width - 50

    def close(self):
        pygame.quit()
