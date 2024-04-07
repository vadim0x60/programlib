import gymnasium as gym
import numpy as np
from programlib.pexpectutil import pexpect_exceptions
import pexpect

def decode_action(action, mode='auto'):
    if mode == 'discrete':
        return int(action)
    elif mode == 'continuous':
        try:
            x = np.array(eval(action))
        except SyntaxError:
            x = np.array(list(map(eval, action.split(r'[\p\s]+'))))

        x = x.reshape(-1)
        return x
    elif mode == 'auto':
        try:
            return decode_action(action, 'discrete')
        except ValueError:
            return decode_action(action, 'continuous')
    else:
        raise ValueError(f'Invalid mode: {mode}')
        
def encode_obs(obs):
    if type(obs) == int:
        return str(obs)

    try:
        obs = obs.tolist()
    except AttributeError:
        pass

    if len(obs) == 1:
        obs = obs[0]

    return ' '.join(str(o) for o in obs)

class Agent():
    """
    Agent: represents a running program that can be interacted with
    """

    def __init__(self, program, process, delimiter='\n', action_mode='auto'):
        self.program = program
        self.process = process
        self.delimiter = delimiter
        self.action_mode = action_mode
        
        self.program.stdout = ''
    
    @pexpect_exceptions
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

        self.process.sendline(encode_obs(obs))
 
        try:
            # All valid actions are one-liners, 
            # so we start decoding as soon as there is a newline
            self.process.expect(self.delimiter)
            action_str = self.process.before.decode()
            action = decode_action(action_str, mode=self.action_mode)
        except SyntaxError as e:
            # But if decoding fails, it's useful to record the full output
            # (often a traceback or error message)
            self.process.expect([pexpect.EOF, pexpect.TIMEOUT])
            action_str = self.process.before.decode()
            
            raise RuntimeError(f'{action_str}\nis not a valid action') from e

        return action, self.process
    
    def close(self):
        self.process.close()
        self.program.exitstatus = self.process.exitstatus
    
    def __del__(self):
        self.close()