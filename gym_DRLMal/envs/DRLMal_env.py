import gym
from gym import error, spaces, utils
from gym.utils import seeding
from Network import Network
import numpy as np
import pandas as pd
import os

class DRLMalEnv(gym.Env):
	metadata = {'render.modes': ['human']}
	
	def __init__(self):
		self.network = Network()
		self.network.clean_network()
		self.network.create_default_network()
		self.network.start_network()
		self.observation_space = None
		self.action_space = None
		self.csv = None
		self.state = None
		self.label = None
		self.done = False
		self.df = None
	
	def step(self, action):
		assert self.action_space is not None and self.observation_space is not None and self.csv is not None, "You have to set a features with set_csv() function"

	
	def reset(self):
		assert self.action_space is not None and self.observation_space is not None and self.csv is not None, "You have to set a features with set_csv() function"
		print("\nAmbiente resettato con file " + self.get_csv()+ "\n")
		self.df = pd.read_csv(self.get_csv())
		self.label = self.df.iloc[0, self.df.shape[1] - 1] #25 last col
		self.state = np.array(self.df.iloc[0, 0:self.df.shape[1] - 1].values)
		self.df = self.df.drop(df.index[0])
		return self.state

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

	def set_csv(self, csv_path):

		def compute_obs_and_act_space():
			if(self.observation_space is None and self.action_space is None):
				self.action_space = spaces.Discrete(2)  # {0, ..., n-1}

				df = pd.read_csv(self.get_csv())

				#Sottraggo uno per non considerare la conolla label
				min = np.zeros(df.shape[1] - 1)

				# Max val of each feature with the same order of csv
				# Max val for: Avg_syn/urg/fin/ack/psh/rst_flag and Avg_/DNS/TCP/UDP/ICMP_pkt
				maxValCol_1 = np.ones(10)

				# Max val from Duration_window_flow to StDev_delta_time
				maxValCol_2 = np.full((5,), np.finfo(np.float32).max)

				# Max val from Avg_pkts_lenght to StDev_pkts_lenght
				maxValCol_3 = np.full((4,), 65535.0)

				# Max val Avg_small_payload_pkt
				maxValCol_4 = np.array(1.0)

				# Max val from Avg_payload to StDev_payload
				maxValCol_5 = np.full((4,), 65535.0)

				# Max val Avg_DNS_over_TCP
				maxValCol_6 = np.array(1.0)

				max = np.append(maxValCol_1, maxValCol_2)
				max = np.append(max, maxValCol_3)
				max = np.append(max, maxValCol_4)
				max = np.append(max, maxValCol_5)
				max = np.append(max, maxValCol_6)

				self.observation_space = spaces.Box(min, max, dtype=np.float32)
		self.csv = csv_path
		compute_obs_and_act_space()

	def get_csv(self):
		return self.csv
