
cost_matrix = [[], [], [], [], []]
cost_dict = {
    '-': 0,
    'A': 1,
    'T': 2,
    'G': 3,
    'C': 4
}
inputSeq = []

with open("./imp2cost.txt", "r") as file:
    file.readline()
    idx = 0
    for line in file:
        data = line.strip('\n').split(',')
        
        for i in range(len(data)):
            if i > 0:
                cost_matrix[idx].append(int(data[i]))

        idx += 1




with open("./imp2input.txt", "r") as file:
    i = 0
    for line in file:
        inputSeq.append(line.strip('\n').split(','))
        i += 1

seq1 = "AAATGTGTGTGTTCCCCAACGATGTCTCTAGAAGACGAACATCCC" 
seq2 = "ATGGAAACGTGAACCTAACTAACACATATGGATCCGACTGACGTTCTCTGATGTAGCCT"
memo = {}
def sequence_align(i, j) -> int:
    cost = 0
    if i == -1 and j == -1:
        return cost, "", ""
    if i == -1:
        #calc
        for z in range (j, -1, -1):
            cost += cost_matrix[cost_dict[seq2[z]]][0]
        return cost, "-" * (j + 1), seq2[:(j + 1)]
    if j == -1:
        #calc
        for z in range (i, -1, -1):
            cost += cost_matrix[cost_dict[seq1[z]]][0]
        return cost, seq1[:(i + 1)], "-" * (i + 1)
    
    if (i, j) in memo:
        return memo[(i, j)]
    
    
    if seq1[i] == seq2[j]:
        align, a1, a2 = sequence_align(i - 1, j - 1)
    else:
        align, a1, a2 = sequence_align(i - 1, j - 1)
        align += cost_matrix[cost_dict[seq1[i]]][cost_dict[seq2[j]]]

    insert, i1, i2 = sequence_align(i - 1, j) # space to i
    insert += cost_matrix[cost_dict[seq1[i]]][0]
    deletion, d1, d2 = sequence_align(i, j - 1) # space to j
    deletion += cost_matrix[cost_dict[seq2[j]]][0]

    # print(f"{i}, {j}: align: {align}, insert: {insert}, delete: {deletion}")

    # cost = min(min(align, insert), deletion)
    # memo[(i, j)] = cost
    
    if align <= insert and align <= deletion:

        memo[(i, j)] = (align, a1 + seq1[i], a2 + seq2[j])
        return (align, a1 + seq1[i], a2 + seq2[j])
    
    elif insert <= align and insert <= deletion:

        memo[(i, j)] = (insert, i1 + seq1[i], i2 + '-')
        return (insert, i1 + seq1[i], i2 + '-')
    
    elif deletion <= align and deletion <= insert:

        memo[(i, j)] = (deletion, d1 + '-', d2 + seq2[j])
        return (deletion, d1 + '-', d2 + seq2[j])

    return cost

(cost, s1, s2) = sequence_align(len(seq1) - 1, len(seq2) - 1)
print(cost)
print(s1)
print(s2)