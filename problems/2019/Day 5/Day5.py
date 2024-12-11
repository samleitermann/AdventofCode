def get_data(file):
    with open(file, 'r') as f:
        data = list(map(int, f.read().split(",")))
    return data

data = get_data("Day5Input.txt")

pointerjump = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 99: 0}

def opcodecomp(instrs,UserInput):

  instr = list.copy(instrs)
  position = 0

  while True:
    pointerChanged = False
    rawopcode = instr[position]
    opcode = rawopcode
    parameterMode = False #0 = position mode
    if rawopcode > 100:
      parameterMode = True #We now have to determine parameters
      opcode= int(str(rawopcode)[-2:]) #slices off the last 2 digits to tell us the operation
      c = int(str(rawopcode)[-3:-2] if len(str(rawopcode)) >= 3 else 0)
      b = int(str(rawopcode)[-4:-3] if len(str(rawopcode)) >= 4 else 0)
      a = int(str(rawopcode)[-5:-4] if len(str(rawopcode)) >= 5 else 0)

    pointer = pointerjump[opcode]

    if opcode not in [99]:
      input1Pos = position + 1 if parameterMode and c==1 else instr[position+1]
      if opcode in [1,2,3,5,6,7,8]:
        input2Pos = position + 2 if parameterMode and b==1 else instr[position+2]
      if opcode in [1,2,7,8]:
        outputPos = instr[position+3]

    if opcode == 1:
      #add
      instr[outputPos] = instr[input1Pos]+instr[input2Pos]
    if opcode == 2:
      #multiply
      instr[outputPos] = instr[input1Pos]*instr[input2Pos]
    if opcode == 3:
      #put input in position
      instr[instr[position+1]] = UserInput
    if opcode == 4:
      #output
      if instr[input1Pos] != 0:
        return instr[input1Pos]
    if opcode == 5:
      #jump if true
      if instr[input1Pos] != 0:
        pointerChanged = True
        position = instr[input2Pos]
    if opcode == 6:
      #jump if false
      if instr[input1Pos] == 0:
        pointerChanged = True
        position = instr[input2Pos]
    if opcode == 7:
      #less than
      instr[outputPos]=1 if instr[input1Pos]<instr[input2Pos] else 0
    if opcode == 8:
      #equals
      instr[outputPos]=1 if instr[input1Pos]==instr[input2Pos] else 0
    if opcode == 99:
      #halt
      break

    if not pointerChanged:
      position = position + pointer


print("Solution1:",opcodecomp(data,1))
print("Solution2:",opcodecomp(data,5))
