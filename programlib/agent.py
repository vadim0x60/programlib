import gymnasium as gym
import numpy as np

def decode_action(action_space, action):
    try:
        a = eval(action)

        if not isinstance(action_space, gym.spaces.Discrete):
            return [a]
    except SyntaxError:
        return list(map(eval, action.split(r'[\p\s]+')))
    
def encode_obs(obs_space, obs):
    try:
        obs = obs.tolist()
    except AttributeError:
        pass

    if len(obs) == 1:
        obs = obs[0]

    return [str(o) for o in obs]

class Agent():
    """
    Agent: represents a running program that can be interacted with
    """

    def __init__(self, program, process, delimiter='\n'):
        self.program = program
        self.process = process
        self.delimiter = delimiter
        
        self.program.stdout = ''

    def act(self, input_lines):
        for line in input_lines:
            self.process.sendline(line)

        self.process.expect(self.delimiter)
        return self.process.before.decode()

    def rl(self, action_space, obs_space):
        return RLAgent(self, action_space, obs_space)
    
    def close(self):
        self.process.close()
        self.program.exitstatus = self.process.exitstatus
    
    def __del__(self):
        self.close()

class RLAgent():
    """
    Reinforcement Learning Agent: represents a running program for control in
    an OpenAI gym environment. Mimics the interface of a stable-baselines model.
    """

    def __init__(self, agent, action_space, obs_space) -> None:
        self.agent = agent
        self.action_space = action_space
        self.obs_space = obs_space

    def predict(self, obs, deterministic=True):
        """
        Predict what the next action should be given the current observation

        The observations will be passed to stdin of the program, and the action
        will be read from stdout.

        Parameters
        ----------
        obs - the current observation
        deterministic - whether to return the action or a pseudo-stochastic
        vector of action probabilities (one-hot)

        Returns (action, state) tuple
        -------
        action - the action to take
        state - a reference to the process to examine the execution state
        """

        obs_str = encode_obs(self.obs_space, obs)
        action_str = self.agent.act(obs_str)
        action = decode_action(self.action_space, action_str)

        if not deterministic:
            actions_probs = np.zeros(self.action_space.n)
            actions_probs[action] = 1.0

        return action, self.agent.process