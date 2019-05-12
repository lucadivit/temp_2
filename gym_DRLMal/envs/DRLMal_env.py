import gym
from gym import error, spaces, utils
from gym.utils import seeding
from Network import Network

class DRLMalEnv(gym.Env):
	metadata = {'render.modes': ['human']}
	
	def __init__(self):
		self.network = Network()
		self.network.clean_network()
		self.network.create_default_network()
		self.network.start_network()
		self.action_space = None
		self.observation_space = None
	
	def step(self, action):
		pass
	
	def reset(self):
		pass

	def render(self, mode='human', close=False):
		pass

	def close(self):
		pass

	def get_network(self):
		return self.network

	def close_all(self):
		self.get_network().stop_network()

	def get_action_space(self):
		return self.action_space

	def get_observation_space(self):
		return self.observation_space