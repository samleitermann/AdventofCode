#First, split off the bingo numbers from the boards.
numbers,*boards=open('Day4Data.txt').read().split('\n\n')
#Next, take each board to a array of arrays, each having 5 lines for the board. 
boards = [[[*map(int,r.split())] for r in b.split('\n')] for b in boards]

#Create empty set of winning boards
won = set()

#Iterate over Bingo Numbers
for num in map(int,numbers.split(',')):
  #Iterate over boards, checking for answers in every board
  for b,r,c in ((b,r,c) for b in set(range(len(boards)))-won for r in range(5) for c in range(5) if boards[b][r][c] == num):
    #When a chosen number is found, set it to -1
    boards[b][r][c] = -1
    #Check to see if a board has won
    if sum(boards[b][r]) == -5 or sum(row[c] for row in boards[b])== -5:
      #Add winning board to set
      won.add(b)
      #Check to see if conditions are met and print answer.
      if len(won)==1 or len(won) == len(boards):
        print('winner', sum(sum(c for c in row if c>0) for row in boards[b])*num)
