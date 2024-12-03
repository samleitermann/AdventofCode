def get_data(file):
  data=[]
  with open(file, 'r') as f:
     for line in f:
       data.append(line.rstrip())
  return data




def partone(file):

	part_list = []

	data = get_data(file)

	for line_id, line in enumerate(data):
		l = 0
		r = len(line) - 1

		while l < len(line):
			#find number, then set the right boundary to the end of the number.
			if line[l].isnumeric():
				r = l+1

				while line[l:r].isnumeric() and r < len(line) + 1:
					r +=1

				#pull right boundary back one when we hit the non-numeric value

				r -= 1
				#now we check adjacency

				valid_number = False
				left = (l >0)
				right = (r < len(line) - 1)
				top = (line_id > 0)

				top_left = top and left
				top_right = top and right

				bot = (line_id < len(data) - 1)

				bot_left = bot and left
				bot_right = bot and right

				#set adjacency rules

				rules_list = [{"name": "left", "criteria": left and (line[l-1] != ".")},{"name": "right", "criteria": right and (line[r] != ".")},{"name": "top", "criteria": top and ((data[line_id - 1][l:r]).replace(".", "") != "")},{"name": "top_left", "criteria": top and left and ((data[line_id - 1][l-1]) != ".")},{"name": "top_right", "criteria": top and right and ((data[line_id - 1][r]) != ".")},{"name": "bot", "criteria": bot and ((data[line_id + 1][l:r]).replace(".", "") != "")},{"name": "bot_left", "criteria": bot and left and ((data[line_id + 1][l-1]) != ".")},{"name": "bot_right", "criteria": bot and right and ((data[line_id + 1][r]) != ".")}]

				for rule in rules_list:
					if rule["criteria"]:
						valid_number = True
						rule_name = rule["name"]
						break
					else:
						rule_name = ""

				part_list.append({
					"line": line_id,
					"number": line[l:r],
					"idx": [l,r],
					"valid_number": valid_number
					})
				#jump l to r
				l = r

			#continue
			l+=1


	total = 0
	for row in part_list:
		if row["valid_number"]:
			total += int(row["number"])

	return(total)

print(partone("Day3Data.txt"))

import math as m, re

def part_two():

	board = list(open('Day3Data.txt'))
	chars = {(r, c): [] for r in range(140) for c in range(140)
						if board[r][c] not in '01234566789.'}

	for r, row in enumerate(board):
		for n in re.finditer(r'\d+', row):
			edge = {(r, c) for r in (r-1, r, r+1)
						   for c in range(n.start()-1, n.end()+1)}

			for o in edge & chars.keys():
				chars[o].append(int(n.group()))

	print(sum(sum(p)    for p in chars.values()),
		  sum(m.prod(p) for p in chars.values() if len(p)==2))

part_two()




