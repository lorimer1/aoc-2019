import aoc_download
from intcode_computer import IntCodeComputer
from custom_enums import Opcode
from amplifier import Amplifier
YEAR = 2019
DAY = 7

puzzle_input = aoc_download.read_input_file(YEAR, DAY)

amp_a = Amplifier(puzzle_input)
amp_b = Amplifier(puzzle_input)
amp_c = Amplifier(puzzle_input)
amp_d = Amplifier(puzzle_input)
amp_e = Amplifier(puzzle_input)

max_output = 0

for phase_a in range(5):

    for phase_b in range(5):
        if phase_b in [phase_a]:
            continue

        for phase_c in range(5):
            if phase_c in [phase_a, phase_b]:
                continue

            for phase_d in range(5):
                if phase_d in [phase_a, phase_b, phase_c]:
                    continue

                for phase_e in range(5):
                    if phase_e in [phase_a, phase_b, phase_c, phase_d]:
                        continue

                    amp_a.reset()
                    amp_b.reset()
                    amp_c.reset()
                    amp_d.reset()
                    amp_e.reset()

                    amp_a.run([phase_a, 0])
                    amp_b.run([phase_b, amp_a.output()])
                    amp_c.run([phase_c, amp_b.output()])
                    amp_d.run([phase_d, amp_c.output()])
                    amp_e.run([phase_e, amp_d.output()])

                    if amp_e.output() > max_output:
                        max_output = amp_e.output()

print("Part 1:", max_output)

max_output = 0

for phase_a in range(5, 10):

    for phase_b in range(5, 10):
        if phase_b in [phase_a]:
            continue

        for phase_c in range(5, 10):
            if phase_c in [phase_a, phase_b]:
                continue

            for phase_d in range(5, 10):
                if phase_d in [phase_a, phase_b, phase_c]:
                    continue

                for phase_e in range(5, 10):
                    if phase_e in [phase_a, phase_b, phase_c, phase_d]:
                        continue

                    amp_a.reset()
                    amp_b.reset()
                    amp_c.reset()
                    amp_d.reset()
                    amp_e.reset()

                    amp_a.run([phase_a, 0])
                    amp_b.run([phase_b, amp_a.output()])
                    amp_c.run([phase_c, amp_b.output()])
                    amp_d.run([phase_d, amp_c.output()])
                    amp_e.run([phase_e, amp_d.output()])

                    while amp_e.computer.opcode != Opcode.HALT:
                        amp_a.run([amp_e.output()])
                        amp_b.run([amp_a.output()])
                        amp_c.run([amp_b.output()])
                        amp_d.run([amp_c.output()])
                        amp_e.run([amp_d.output()])

                    if amp_e.output() > max_output:
                        max_output = amp_e.output()

print("Part 2:", max_output)
