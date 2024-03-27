from programlib import Program
import gymnasium as gym

mountain_car_solver = """
for _ in range(10):
    position, velocity = map(float, input().split())
    print(1)

while True:
    position, velocity = map(float, input().split())
    if abs(velocity) < 0.01:
        print(0)
    elif velocity < 0:
        print(-1)
    else:
        print(1)
"""

env = gym.make('MountainCarContinuous-v0', max_episode_steps=500, render_mode='human')
program = Program(source=mountain_car_solver, language='Python')
agent = program.spawn(action_mode='continuous')

obs, info = env.reset()
print(obs, info)
terminated = False
truncated = False

while not (terminated or truncated):
    action, _ = agent.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    print(obs, reward, info)