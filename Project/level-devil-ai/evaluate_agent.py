from stable_baselines3 import PPO
from env.level_devil_env import LevelDevilEnv
import time

env = LevelDevilEnv()
model = PPO.load("ppo_level_devil")
obs, _ = env.reset()
done = False

while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, _, _ = env.step(action)
    env.render()
    time.sleep(0.1)

print("Finished with reward:", reward)
env.close()
