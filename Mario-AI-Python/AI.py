import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT

#some more wrappers
from gym.wrappers import GrayScaleObservation
from numpy import record
from stable_baselines3.common.vec_env import VecFrameStack, DummyVecEnv
from matplotlib import pyplot as plt

import os
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback

#Create a base environment
env = gym_super_mario_bros.make('SuperMarioBros-v0')
#Simplifies the controlls
env = JoypadSpace(env, SIMPLE_MOVEMENT) 
#Grayscale
env = GrayScaleObservation(env, keep_dim=True)
#Wrap in side the dummy
env = DummyVecEnv([lambda: env])
#Stack the frame
env = VecFrameStack(env, 4, channels_order='last')

#For saving model and logging
class TrainAndLoggingCallback(BaseCallback):

    def __init__(self, check_freq, save_path, verbose=1):
        super(TrainAndLoggingCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.save_path = save_path

    def _init_callback(self):
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self):
        if self.n_calls % self.check_freq == 0:
            model_path = os.path.join(self.save_path, 'best_model_{}'.format(self.n_calls))
            self.model.save(model_path)

        return True

CHECKPOINT_DIR = './train/'
LOG_DIR = './logs/'
callback = TrainAndLoggingCallback(check_freq=1000, save_path=CHECKPOINT_DIR)
#AI training settings
model = PPO('CnnPolicy', env, verbose=1, tensorboard_log=LOG_DIR, learning_rate=0.000001, n_steps=512)

#Train
model.learn(total_timesteps=1000, callback = callback)

model.save('TestModel')
