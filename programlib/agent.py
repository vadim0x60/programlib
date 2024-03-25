import gymnasium as gym
import numpy as np
from programlib.pexpectutil import pexpect_exceptions

def decode_action(action):
    try:
        try:
            x = np.array(eval(action))
        except SyntaxError:
            x = np.array(list(map(eval, action.split(r'[\p\s]+'))))

        x = x.reshape(-1)
        if x.size == 1:
            x = x[0]
        return x
    except SyntaxError as e:
        raise RuntimeError(f'{action}\nis not a valid action') from e
    
def encode_obs(obs):
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

    @pexpect_exceptions
    def act(self, input_lines):
        for line in input_lines:
            self.process.sendline(line)

        self.process.expect(self.delimiter)
        return self.process.before.decode()
    
    def predict(self, obs, deterministic=True):
        """
        Predict what the next action should be given the current observation.
        Same as act(), but designed to work with reinforcement learning envs.
        Mimics the interface of a stable-baselines model.

        The observations will be passed to stdin of the program, and the action
        will be read from stdout.

        Parameters
        ----------
        obs - the current observation
        deterministic - should always be set to True, 
        for compatibility with stable-baselines

        Returns (action, state) tuple
        -------
        action - the action to take
        state - a reference to the process to examine the execution state
        """

        assert deterministic, "Pseudo-stochastic actions not supported"

        obs_str = encode_obs(obs)
        action_str = self.act(obs_str)
        action = decode_action(action_str)

        return action, self.process
    
    def close(self):
        self.process.close()
        self.program.exitstatus = self.process.exitstatus
    
    def __del__(self):
        self.close()