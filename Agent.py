from keras.optimizers import *
from rl.agents.dqn import DQNAgent
from rl.policy import *
from rl.memory import *
import os


class Agent():

    def __init__(self, env=None, model=None, num_actions=None, policy=BoltzmannQPolicy(), optimizer=Adam(lr=1e-3), metrics=['accuracy'], memory=SequentialMemory(limit=int(2e6), window_length=1), save_weights=True, load_weights=True):
        self.env = env
        self.model = model
        self.nb_actions = num_actions
        self.memory = memory
        self.policy = policy
        self.optimizer = optimizer
        self.metrics = metrics
        self.save_weights = save_weights
        self.load_weights = load_weights
        self.weights_file_name = "_malRL_weights.h5f"
        self.agent = None


    def create_default_dqn_agent(self, enable_dueling_network=True, target_model_update=1e-2, nb_steps_warmup=5):
        self.weights_file_name = "dqn" + self.weights_file_name
        dqn = DQNAgent(model=self.model, policy=self.policy, memory=self.memory, nb_actions=self.nb_actions,
                       enable_dueling_network=enable_dueling_network, target_model_update=target_model_update,
                       nb_steps_warmup=nb_steps_warmup)
        dqn.compile(self.optimizer, self.metrics)
        if(self.load_weights is True):
            if(os.path.isfile(self.weights_file_name) is True):
                try:
                    dqn.load_weights(self.weights_file_name)
                    print("\nWeights Added\n")
                except Exception as e:
                    print (e)
        self.agent = dqn
        return dqn

    def train_agent(self, steps=100):
        self.agent.fit(self.env, nb_steps=steps, visualize=True, verbose=2)
        if(self.save_weights is True):
            self.agent.save_weights(self.weights_file_name, overwrite=True)
        return

