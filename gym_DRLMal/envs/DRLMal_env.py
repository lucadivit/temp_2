import gym
from gym import error, spaces, utils
from gym.utils import seeding
from Network import Network
import numpy as np
import pandas as pd
import os, time

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
		self.df = None

		self.action_space = spaces.Discrete(2)  # {0, ..., n-1}

		# Sottraggo uno per non considerare la conolla label
		min = np.zeros(25) #self.df.shape[1] - 1

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
	
	def step(self, action):
		assert self.df is not None, "You have to set a features with set_csv() function"
		done = False
		actual_state = self.state
		actual_label = self.label
		reward = None
		if(float(action) == float(actual_label)):
			reward = 1
		else:
			reward = 0

		row = self.df.loc[0].to_numpy()
		self.label = row[self.df.shape[1] - 1]
		self.state = row[0:self.df.shape[1] - 1]
		self.df = self.df.drop(self.df.index[0]).reset_index(drop=True)
		return self.state, reward, done, {}

	def reset(self):
		assert self.df is not None, "You have to set a features with set_csv() function"
		row = self.df.loc[0].to_numpy()
		self.label = row[self.df.shape[1] - 1]
		self.state = row[0:self.df.shape[1] - 1]
		self.df = self.df.drop(self.df.index[0]).reset_index(drop=True)
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
		self.csv = csv_path
		print("\nNuovo file: " + self.get_csv() + "\n")
		try:
			self.df = pd.read_csv(self.get_csv())
		except Exception as e:
			print("\nErrore nell'apertura del file csv.\n")
			print(e)

	def get_csv(self):
		return self.csv
