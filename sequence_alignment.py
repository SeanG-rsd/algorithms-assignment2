import sys
sys.setrecursionlimit(6000)
# defining cost matrix
cost_matrix = [[], [], [], [], []]
cost_dict = {
    '-': 0,
    'A': 1,
    'T': 2,
    'G': 3,
    'C': 4
}

# defining test input sequences
inputSeq = []

# reading input costs
with open("./imp2cost.txt", "r") as file:
    file.readline()
    idx = 0
    for line in file:
        data = line.strip('\n').split(',')
        
        for i in range(len(data)):
            if i > 0:
                cost_matrix[idx].append(int(data[i]))

        idx += 1

# reading inputs
with open("./runtime_test_input.txt", "r") as file:
    i = 0
    for line in file:
        inputSeq.append(line.strip('\n').split(','))
        i += 1

# defining sequences
seq1 = "" 
seq2 = ""

# defining memoization for dynamic programming
memo = {}


def align_seq_tabulation():
    dp = [[0 for _ in range(len(seq1) + 1)] for _ in range(len(seq2) + 1)]


    for i in range(1, len(seq1) + 1):
        c1 = seq1[i]
        for j in range(1, len(seq2) + 1):
            c2 = seq2[j]
            align_cost = dp[i-1][j-1] + cost_matrix[cost_dict[c1]][cost_dict[c2]]

            insert_cost = dp[i-1][j] + cost_matrix[cost_dict[c1]][0]
            
            delete_cost = dp[i, j-1] + cost_matrix[cost_dict[c2]][0]

            dp[i][j] = min (align_cost, insert_cost, delete_cost)


def sequence_align(i, j) -> int:
    cost = 0
    # end of both sequences
    if i == -1 and j == -1:
        return cost, "", ""
    # end of first, return cost of deletion/insertion of second
    if i == -1:
        for z in range (j, -1, -1):
            cost += cost_matrix[cost_dict[seq2[z]]][0]
        return cost, "-" * (j + 1), seq2[:(j + 1)]
    # end of second, return cost of deletion/insertion of first
    if j == -1:
        for z in range (i, -1, -1):
            cost += cost_matrix[cost_dict[seq1[z]]][0]
        return cost, seq1[:(i + 1)], "-" * (i + 1)
    
    # memoization: if we've already calculated it, return the calculation
    if (i, j) in memo:
        return memo[(i, j)]
    
    # alignment of i and j, if they are different add the substitution cost
    if seq1[i] == seq2[j]:
        align, a1, a2 = sequence_align(i - 1, j - 1)
    else:
        align, a1, a2 = sequence_align(i - 1, j - 1)
        align += cost_matrix[cost_dict[seq1[i]]][cost_dict[seq2[j]]]

    # insert at j, add cost of insertion to match i and decrease i since j did not move 
    insert, i1, i2 = sequence_align(i - 1, j) # space to i
    insert += cost_matrix[cost_dict[seq1[i]]][0]

    # delete at j, add cost of deletion to remove j and decrease j since we removed j
    deletion, d1, d2 = sequence_align(i, j - 1) # space to j
    deletion += cost_matrix[cost_dict[seq2[j]]][0]
    

    # calculate the minimum between the 3 options, and return the cost along with the calculated output strings
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

with open("./imp2output.txt", "w") as file:
    for input in inputSeq:
        # reset input variables and memoization
        seq1 = input[0]
        seq2 = input[1]
        memo = {}

        (cost, s1, s2) = sequence_align(len(seq1) - 1, len(seq2) - 1)
        file.write(f"{s1},{s2}:{cost}\n")