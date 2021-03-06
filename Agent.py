from keras.optimizers import *
from rl.agents.dqn import DQNAgent
from rl.policy import *
from rl.memory import *
from rl.callbacks import *
from keras.callbacks import *
import os


class Agent():

    def __init__(self, env=None, model=None, num_actions=None, policy=BoltzmannQPolicy(), optimizer=Adam(lr=1e-3), metrics=['accuracy'], memory=SequentialMemory(limit=int(2e6), window_length=1), batch_size=32, save_weights=True, load_weights=True):
        self.env = env
        self.model = model
        self.nb_actions = num_actions
        self.memory = memory
        self.policy = policy
        self.optimizer = optimizer
        self.metrics = metrics
        self.save_weights = save_weights
        self.load_weights = load_weights
        self.batch_size = batch_size
        self.weights_file_name = "_malRL_weights.h5f"
        self.agent = None
        self.steps_warmup = None
        self.file_logger = None

    def create_default_dqn_agent(self, enable_dueling_network=True, enable_double_dqn=True, target_model_update=1e-2, nb_steps_warmup=10):
        self.steps_warmup = nb_steps_warmup
        self.file_logger = FileLogger("training_log_dqn.txt")
        self.weights_file_name = "dqn" + self.weights_file_name
        dqn = DQNAgent(model=self.model, policy=self.policy, memory=self.memory, batch_size=self.batch_size, nb_actions=self.nb_actions,
                       enable_dueling_network=enable_dueling_network, enable_double_dqn=enable_double_dqn,
                       target_model_update=target_model_update, nb_steps_warmup=nb_steps_warmup)
        dqn.compile(self.optimizer, self.metrics)
        self.agent = dqn
        return dqn

    def train_agent(self, steps=None, log_interval=1000, verbose=2, nb_max_episode_steps=None):
        if(steps > self.steps_warmup):
            if(self.load_weights is True):
                if(os.path.isfile(self.weights_file_name) is True):
                    try:
                        self.agent.load_weights(self.weights_file_name)
                        print("\nWeights Added\n")
                    except Exception as e:
                        print (e)
            history = self.agent.fit(self.env, nb_steps=steps, verbose=verbose, log_interval=log_interval, nb_max_episode_steps=nb_max_episode_steps, callbacks=[self.file_logger])

            if(self.save_weights is True):
                self.agent.save_weights(self.weights_file_name, overwrite=True)
            return history
        else:
            print("\nNumero di passi troppo basso.\n")

    def get_num_warmup_steps(self):
        return self.steps_warmup

