def solve(lines:list[str]):
    wires = {}
    parsing_wires = True
    gates = []
    for line in lines:
        if line == "":
            parsing_wires = False
            continue
        if parsing_wires:
            wire_name, init_val = line.split(": ")
            wires[wire_name] = int(init_val)
        else:
            wire_one, gate, wire_two, _, output_wire = line.split(" ")
            gates.append((wire_one, wire_two, output_wire, gate))
            # set up initially undetermined wires
            if wire_one not in wires.keys():
                wires[wire_one] = None
            if wire_two not in wires.keys():
                wires[wire_two] = None
            if output_wire not in wires.keys():
                wires[output_wire] = None


    made_changes_this_loop = True
    while made_changes_this_loop:
        made_changes_this_loop = False

        for wire_one, wire_two, output_wire, gate in gates:
            # two inputs available and output not currently calculated
            if wires[wire_one] != None and wires[wire_two] != None and wires[output_wire] == None:
                if gate == "AND":
                    wires[output_wire] = wires[wire_one] & wires[wire_two]
                elif gate == "OR":
                    wires[output_wire] = wires[wire_one] | wires[wire_two]
                elif gate == "XOR":
                    wires[output_wire] = wires[wire_one] ^ wires[wire_two]
                made_changes_this_loop = True
        
    zkeys = sorted([x for x in wires.keys() if x[0:1] == "z"])
    zvals = "".join(reversed([str(wires[x]) for x in zkeys]))

    print(int(zvals,2))