from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecTransposeImage
from env.level_devil_env import LevelDevilEnv

env = DummyVecEnv([lambda: Monitor(LevelDevilEnv())])
env = VecTransposeImage(env)

model = PPO("CnnPolicy", env, verbose=1, tensorboard_log="./ppo_logs")
model.learn(total_timesteps=20000)
model.save("ppo_level_devil")
print("✅ Training complete. Model saved.")
env.close()
