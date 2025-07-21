import sys, os, pygame
sys.path.append(os.path.join(os.path.dirname(__file__), 'env'))
from level_devil_env import LevelDevilEnv

def manual_play():
    env = LevelDevilEnv()
    obs, _ = env.reset()
    done = False
    print("Control: ← → ↑ or ESC to quit")
    while not done:
        action = 3
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: action = 0
                elif event.key == pygame.K_RIGHT: action = 1
                elif event.key == pygame.K_UP: action = 2
        obs, reward, done, _, _ = env.step(action)
        env.render()
        pygame.time.wait(100)
    print(f"Episode finished with reward: {reward}")
    env.close()

if __name__ == "__main__":
    manual_play()
