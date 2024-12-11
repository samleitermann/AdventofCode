def get_data(file):
  winning_numbers=[]
  card_numbers=[]
  with open(file, 'r') as f:
     for line in f:
         winning, card = line.split("|")
         winning = winning.split()[2:]
         winning = list(map(int,winning))
         winning_numbers.append(winning)
         card = card.split()
         card = list(map(int, card))
         card_numbers.append(card)
  return winning_numbers, card_numbers

def part_one(winning_numbers,card_numbers):

    i = 0
    answer = 0

    while i < len(card_numbers):

        matches = 0

        matches = sum(match in card_numbers[i] for match in winning_numbers[i])


        if matches != 0:
            answer += 2**(matches-1)
            i += 1
        else:
            i += 1

    return answer

wins = get_data("Day4Input.txt")[0]
cards = get_data("Day4Input.txt")[1]

print(part_one(wins,cards))

def part_two(winning_numbers,card_numbers):

    i = 0

    cards = [1 for x in range(len(card_numbers))]

    while i < len(card_numbers):

        matches = 0

        matches = sum(match in card_numbers[i] for match in winning_numbers[i])
        card_multiplier = cards[i]

        for j in range(matches):
            cards[i+j+1] += 1*card_multiplier

        i+=1

    return (sum(cards))

print(part_two(wins,cards))














