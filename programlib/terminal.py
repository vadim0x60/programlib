import pyte

class Terminal:
    def __init__(self, rows=24, cols=80):
        self.screen = pyte.Screen(cols, rows)
        self.stream = pyte.Stream(self.screen)

    def emulate(self, raw_output, clean=True):
        self.stream.feed(raw_output)

        lines = self.screen.display
        self.screen.reset()

        if clean:
            lines = [line.rstrip() for line in lines]
            lines = [line for line in lines if line]

        return lines