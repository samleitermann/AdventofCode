def get_data(file):
    data=[]

    with open(file, 'r') as f:
        for line in f:
            data.append(line.rstrip())

    return data



rawdata=get_data("Day1Input.txt")


def solution(data):

    list_one = []
    list_two = []

    distances = []
    similarity_score = 0

    for line in data:
        temp_data = line.split("   ")
        list_one.append(int(temp_data[0]))
        list_two.append(int(temp_data[1]))

    list_one.sort()
    list_two.sort()

    for i in range(len(list_one)):
        distances.append(abs(list_one[i] - list_two[i]))
        similarity_score += list_two.count(list_one[i]) * list_one[i]


    return sum(distances), similarity_score

print(solution(rawdata))









