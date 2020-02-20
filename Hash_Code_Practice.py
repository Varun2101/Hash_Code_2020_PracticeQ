# Taking input (uncomment the one you want to test)
#with open("b_small.in", 'r') as file:
#with open("c_medium.in", 'r') as file:
#with open("d_quite_big.in", 'r') as file:
with open("e_also_big.in", 'r') as file:
    line1 = file.readline()
    line2 = file.readline()

maxSlices, num = int(line1.split()[0]), int(line1.split()[1])
sliceList = [int(n) for n in line2.split()]


# Function to get how close a list is to the target sum
# We use a bit of linear algebra for optimization - choiceList is a vector of only 0s and 1s. It's dot product
# with sliceList gives us the total number of slices chosen
def getScore(choiceList):
    totalSum = 0
    for i in range(num):
        totalSum += choiceList[i] * sliceList[i]
    score = maxSlices - totalSum
    return score


# Initializing the choice list with all 1s, ie all pizzas selected
choiceList = [1] * num
score = getScore(choiceList)
for i in range(1, num + 1):
    if sliceList[-i] <= (-score) and choiceList[-i] == 1:  # starts from the back of the list, ie the largest pizzas
        choiceList[-i] = 0  # removes a pizza as long as the score remains negative, ie sum still over the limit
        score = getScore(choiceList)

# We now have a score that is just <=0, now needs to be optimized.
bestScore = getScore(choiceList)

optimizedList = choiceList[:]  # creating a copy of the first output, which we'll further optimize
# Finds the index of the largest pizza that's still included
lastOneIndex = len(optimizedList) - 1 - optimizedList[::-1].index(1)
for k in range(lastOneIndex + 1, 0, -1):
    optimizedList[k] = 1  # includes the (originally excluded) pizza just larger than the previous largest included
    score = getScore(optimizedList)
    # Finds the most optimized list while this new large pizza is included, using the same method as before
    # except this time, we use an increasingly smaller sample space with each iteration, fine tuning further and further
    for i in range(k - 1, 0, -1):
        if sliceList[i] <= (-score) and optimizedList[i] == 1:
            optimizedList[i] = 0
            score = getScore(optimizedList)
    if score > bestScore:  # updates the new most optimized solution
        bestScore = score
        choiceList = optimizedList
        if score == 0:  # when a perfect solution is found, we break early to save unnecessary processing time
            break

# in case a perfect solution doesn't exist or hasn't been found, the score is still negative so an additional block of
# code is required to make the solution just positive. However, for the purpose of the practice problem, all input sets
# have a perfect solution so for now it is unnecessary.

print(bestScore)
print(choiceList)
list1 = []
list2 = []
for i in range(num):
    if choiceList[i] == 1:
        list1.append(sliceList[i])
        list2.append(i)
print(list1)  # printing the pizza slices chosen for reference and cross-checking
print(sum(list1))  # reconfirming that a solution is valid and optimum

print("\n\nSubmission:")  # format required for the actual submission
print(len(list1))  # number of pizzas ordered
for n in list2:
    print(n, end=' ')  # indexes of the pizzas ordered
