import gym
import pexpect

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

    return [str(obs)]

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

    def test(self, rl_env, act_decoder=decode_action, obs_encoder=encode_obs, render=False):
        obs, info = rl_env.reset()
        terminated = False
        truncated = False
        r = 0
        total_r = 0

        rollout = []

        while not (terminated or truncated):
            obs_str = obs_encoder(rl_env.observation_space, obs)
            act_str = self.act(obs_str)
            try:
                action = act_decoder(rl_env.action_space, act_str)
            except SyntaxError:
                try:
                    self.process.expect(pexpect.EOF)
                except pexpect.TIMEOUT:
                    pass
                raise ValueError(act_str + self.process.before.decode())
            rollout.append((obs, r, info, action))
            obs, r, terminated, truncated, info = rl_env.step(action)
            total_r += r
            if render:
                rl_env.render()

        rollout.append((obs, r, info, None))

        self.close()
        self.program.avg_score = total_r

        return rollout
    
    def close(self):
        self.process.close()
        self.program.exitstatus = self.process.exitstatus
    
    def __del__(self):
        self.close()