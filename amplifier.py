from intcode_computer import IntCodeComputer

class Amplifier:

    def __init__(self, stream):
        self.computer = IntCodeComputer(stream)

    def output(self):
        return self.computer.output

    def run(self, input_queue):
        self.computer.input_queue += input_queue
        self.computer.run()

    def reset(self):
        self.computer.reset()
