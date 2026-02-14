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
with open("./imp2input.txt", "r") as file:
    i = 0
    for line in file:
        inputSeq.append(line.strip('\n').split(','))
        i += 1

# defining sequences
seq1 = "" 
seq2 = ""

# setup for tabulation
dp = [[0 for _ in range(len(seq2) + 1)] for _ in range(len(seq1) + 1)]

# 1 for align, 2 for insert, 3 for delete
flag = [[0 for _ in range(len(seq2) + 1)] for _ in range(len(seq1) + 1)]

def align_seq_tabulation():
    
    # setup base cases for deletion in table
    cost = 0
    for i in range(1, len(seq2) + 1):
        cost += cost_matrix[cost_dict[seq2[i - 1]]][0]
        dp[0][i] = cost
        flag[0][i] = 3

    # setup base cases for insertion in table
    cost = 0
    for i in range (1, len(seq1) + 1):
        cost += cost_matrix[cost_dict[seq1[i-1]]][0]
        dp[i][0] = cost
        flag[i][0] = 2

    for i in range(1, len(seq1) + 1):
        c1 = seq1[i - 1]
        for j in range(1, len(seq2) + 1):
            c2 = seq2[j - 1]

            # alignment of i and j, if they are different add the substitution cost
            align = dp[i-1][j-1] + cost_matrix[cost_dict[c1]][cost_dict[c2]]

            # insert at j, add cost of insertion to match i and decrease i since j did not move
            insert = dp[i-1][j] + cost_matrix[cost_dict[c1]][0]
            
            # delete at j, add cost of deletion to remove j and decrease j since we removed j
            delete = dp[i][j-1] + cost_matrix[cost_dict[c2]][0]

            # calculate the minimum between the 3 options, and set cost in table along with flag for string reconstruction
            if align <= insert and align <= delete:

                dp[i][j] = align
                flag[i][j] = 1

            elif insert <= align and insert <= delete:

                dp[i][j] = insert
                flag[i][j] = 2

            else:

                dp[i][j] = delete
                flag[i][j] = 3
    
    i = len(seq1)
    j = len(seq2)

    out1 = ""
    out2 = ""

    # iterate through the flags in reverse and add to string
    while i > 0 or j > 0:

        val = flag[i][j]

        # align
        if val == 1:
            out1 += seq1[i - 1]
            out2 += seq2[j - 1]
            i -= 1
            j -= 1
        # insert
        elif val == 2:
            out1 += seq1[i - 1]
            out2 += '-'
            i -= 1
        # delete
        elif val == 3:
            out1 += '-'
            out2 += seq2[j - 1]
            j -= 1

    # return the last value in the table and the reversed aligned strings
    return (dp[len(seq1)][len(seq2)], out1[::-1], out2[::-1])

with open("./imp2output.txt", "w") as file:
    for input in inputSeq:
        # reset input variables and tabulation/flags
        seq1 = input[0]
        seq2 = input[1]
        dp = [[0 for _ in range(len(seq2) + 1)] for _ in range(len(seq1) + 1)]
        flag = [[0 for _ in range(len(seq2) + 1)] for _ in range(len(seq1) + 1)]

        (cost, s1, s2) = align_seq_tabulation()
        file.write(f"{s1},{s2}:{cost}\n")