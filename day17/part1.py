class Computer:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.ip = 0
        self.output = []

    def _combo_operand_value(self, operand):
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        if operand == 7:
            raise ValueError("Operand of 7 not allowed")
        else:
            return operand

    def execute_program(self, program: list[int]):
        while self.ip < len(program) - 1:
            operator = program[self.ip]
            operand = program[self.ip + 1]

            if operator == 0:   # adv: a = a / (2 ^ combo(operand))
                self.a = int(self.a / pow(2,self._combo_operand_value(operand)))
            elif operator == 1: # bxl: b = b XOR operand
                self.b = self.b ^ operand
            elif operator == 2: # bst: b = combo(operand) % 8. Set b to bottom 3 bits of combo operand
                self.b = self._combo_operand_value(operand) % 8
            elif operator == 3: # jnz: if a != 0 -> jump to operand. dont increment ip.
                if self.a != 0:
                    self.ip = operand
                    continue
            elif operator == 4: # bxc: b = b XOR C. Ignore operand.
                self.b = self.b ^ self.c
            elif operator == 5: # out: out << ( combo(operand) % 8 ). write bottom 3 bits of combo operand
                self.output.append(str(self._combo_operand_value(operand) % 8))
            elif operator == 6: # bdv: b = a / (2 ^ combo(operand))
                self.b = int(self.a / pow(2,self._combo_operand_value(operand)))
            elif operator == 7: # cdv: c = a / (2 ^ combo(operand))
                self.c = int(self.a / pow(2,self._combo_operand_value(operand)))

            self.ip += 2


def solve(lines:list[str]):
    a_reg_init = int(lines[0].split(": ")[1])
    program = [int(x) for x in lines[4].split(": ")[1].split(",")]
    computer = Computer()
    computer.a = a_reg_init
    computer.execute_program(program)

    print(",".join(computer.output))