from programlib import Program
import gym

mountain_car_solver = """
while True:
    obs = eval(input())
    position, velocity = obs
    if abs(velocity) < 0.01:
        print(-0.5 - position)
    else:
        print(velocity)
"""

env = gym.make('MountainCarContinuous-v0', max_episode_steps=500, render_mode='human')
program = Program(source=mountain_car_solver, language='Python')
print(program.spawn().test(env, render=True))