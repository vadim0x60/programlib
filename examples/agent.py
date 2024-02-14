from programlib import Program
import gymnasium as gym

mountain_car_solver = """
while True:
    position = eval(input())
    velocity = eval(input())
    if abs(velocity) < 0.01:
        print(-0.5 - position)
    else:
        print(velocity)
"""

env = gym.make('MountainCarContinuous-v0', max_episode_steps=500, render_mode='human')
program = Program(source=mountain_car_solver, language='Python')
agent = program.spawn()

obs, info = env.reset()
print(obs, info)
terminated = False
truncated = False

while not (terminated or truncated):
    action, _ = agent.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    print(obs, reward, info)