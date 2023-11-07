from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.monitor import Monitor
from cnn_env import SnakeEnv
NUM_ENV=6
# Create and wrap the environment
#env = DummyVecEnv([SnakeEnv() for i in range(NUM_ENV)])
env=SnakeEnv(render_mode='human')
# Instantiate the agent with a tensorboard log
model = PPO('CnnPolicy', env, verbose=1, tensorboard_log="./ppo_snake_tensorboard/",n_steps=1024,batch_size=64)

# Set up a checkpoint save after a certain number of timesteps
checkpoint_interval = 10000  # This should be adjusted based on your training regime
for checkpoint in range(1, 50):  # Example: save 10 checkpoints
    model.learn(total_timesteps=checkpoint_interval, reset_num_timesteps=False)
    model.save(f"models/ppo_snake_checkpoint_{checkpoint}")

# Close the environment
env.close()

