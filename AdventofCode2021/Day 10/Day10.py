# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 20:05:48 2021

@author: samle
"""
def get_data(file):
  with open(file, encoding='utf-8') as f:
    data = f.readlines()
  return data

data = get_data("C:/Users/samle/OneDrive/Documents/GitHub/AdventofCode/AdventofCode2021/Day 10/Day10Example.txt")

#Define bracket pairs and closing brackets
brackets = ["()", "[]", "{}", "<>"]
closing = [")", "]", "}", ">"]

#Initiatlize arrays for solution
corrupt = []
incomplete = []
result1 = []
result2 = []

#Take input and replace complete pairs of delimiters. Iterate until done.
for line in data:
  while any(x in line for x in brackets):
        for bracket in brackets:
            line = line.replace(bracket, "")
            
  #Check to see if there are closed delimiters left (if open, its just incomplete.)
  for closed in closing:
      if any(x in line for x in closing):
          corrupt.append(line)
          break
      # not needed for part 1
      if not all(x in line for x in closing):
          incomplete.append(line)
          break

for corr_line in corrupt:
    for c in corr_line:
        if c == ")":
            result1.append(3)
            break
        if c == "]":
            result1.append(57)
            break
        if c == "}":
            result1.append(1197)
            break
        if c == ">":
            result1.append(25137)
            break
            
print(sum(result1))

for incomplete_line in incomplete:
  acc = 0

  for c in incomplete_line[::-1]:
    if c == "(":
        acc = acc * 5 + 1
    elif c == "[":
        acc = acc * 5 + 2
    elif c == "{":
        acc = acc * 5 + 3
    elif c == "<":
        acc = acc * 5 + 4

  result2.append(acc) 

print(sorted(result2)[len(result2) // 2])
