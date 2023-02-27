from programlib import Program

char_counter_py = """
c = 0
while True:
    text = input()
    c += len(text)
    print(c)
"""

program = Program(source=char_counter_py, language='Python')
agent = program.spawn()
inp = 'Hello, program!'
print('> ' + inp)
output = next(agent.act([inp]))
print(output)

for _ in range(4):
    inp = f'You said {output}, right?'
    print('> ' + inp)
    output = next(agent.act([inp]))
    print(output)