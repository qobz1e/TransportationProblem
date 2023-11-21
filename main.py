input_file = open("input.txt", "r")
output_file = open("output.txt", "w")

# Reading input as lines
input_list = input_file.read()
# Making integers from strings
input_list = [[int(number) for number in line.split(" ")] for line in input_list.split("\n")]

# Splitting data into separate elements
S = input_list[0]
C = input_list[1:-1]
D = input_list[-1]


# Checking if methods are applicable
if not (C and S and D) or (len(S) != len(C)) or (len(D) != len(C[0])):
	print("The methods are not applicable!")
	output_file.write("The methods are not applicable!")
	input_file.close()
	output_file.close()
	exit(1)


# Checking if problem is balanced
if sum(D) != sum(S):
	print("The problem is not balanced!")
	output_file.write("The problem is not balanced!")
	input_file.close()
	output_file.close()
	exit(1)


# Printing the input table
table = []
for i in range(len(C)):
	table.append([])
	for j in range(len(C[0])):
		table[i].append(C[i][j])
		if j == len(C[0]) - 1:
			table[i].append(S[i])
table.append(D)

print("Inputted table:")
output_file.write("Inputted table:\n")
for line in table:
	for elem in line:
		print('{:>10}'.format(elem), end="")
		output_file.write('{:>10} '.format(elem))
	print()
	output_file.write("\n")


# Copy of inputs' for Vogel's method
S_Vogel = S[:]
C_Vogel = [row[:] for row in C]
D_Vogel = D[:]
ans_Vogel = 0

# Copy of inputs' for North-West corner method
S_NW = S[:]
C_NW = [row[:] for row in C]
D_NW = D[:]
ans_NW = 0

# Copy of inputs' for Russell's method
S_R = S[:]
C_R = [row[:] for row in C]
D_R = D[:]
ans_R = 0


# North-West corner method
cur_row = 0
cur_col = 0
while cur_row != len(C_NW) and cur_col != len(C_NW[0]):
	# If supply for current North-West corner is less than demand then we delete the row for future iterations
	if S_NW[cur_row] <= D_NW[cur_col]:
		ans_NW += S_NW[cur_row] * C_NW[cur_row][cur_col]

		D_NW[cur_col] -= S_NW[cur_row]
		cur_row += 1
	# If demand is less than supply then we delete the column for future iterations
	else:
		ans_NW += D_NW[cur_col] * C_NW[cur_row][cur_col]

		S_NW[cur_row] -= D_NW[cur_col]
		cur_col += 1


# Function for finding differences in rows and columns for Vogel's method
def find_differences(grid):
	row_differences = []
	col_differences = []

	cols = []
	for columns in range(len(grid[0])):
		cols.append([])

	for row in grid:
		row_copy = row[:]
		row_copy.sort()
		row_differences.append(row_copy[1] - row_copy[0])
		for col in range(len(row)):
			cols[col].append(row[col])

	for col in cols:
		col_copy = col[:]
		col_copy.sort()
		col_differences.append(col_copy[1] - col_copy[0])

	return row_differences, col_differences


# Vogel's method
while max(D_Vogel) != 0 or max(S_Vogel) != 0:
	rows_d, cols_d = find_differences(C_Vogel)

	rows_max = max(rows_d)
	cols_max = max(cols_d)

	if rows_max >= cols_max:
		# Finding index of row that has maximal difference
		index_row = rows_d.index(rows_max)
		# Finding the least element in the row
		min_elem = min(C_Vogel[index_row])
		# Finding the column index of the least element
		index_col = C_Vogel[index_row].index(min_elem)

		# Finding minimal of supply and demand for the element found earlier
		min_sd = min(S_Vogel[index_row], D_Vogel[index_col])

		# Updating answer, supply and demand
		ans_Vogel += min_sd * min_elem
		S_Vogel[index_row] -= min_sd
		D_Vogel[index_col] -= min_sd

		# Updating the grid for future iterations
		if D_Vogel[index_col] == 0:
			for i in range(len(C_Vogel)):
				C_Vogel[i][index_col] = 10**10
		else:
			C_Vogel[index_row] = [10**10 for x in C_Vogel[index_row]]
	else:
		# Finding index of col that has maximal difference
		index_col = cols_d.index(cols_max)
		# Finding the least element in the column
		min_elem = min([row[index_col] for row in C_Vogel])
		# Finding the row index of the least element
		index_row = [row[index_col] for row in C_Vogel].index(min_elem)

		# Finding minimal of supply and demand for the element found earlier
		min_sd = min(S_Vogel[index_row], D_Vogel[index_col])

		# Updating answer, supply and demand
		ans_Vogel += min_sd * min_elem
		S_Vogel[index_row] -= min_sd
		D_Vogel[index_col] -= min_sd

		# Updating the grid for future iterations
		if D_Vogel[index_col] == 0:
			for i in range(len(C_Vogel)):
				C_Vogel[i][index_col] = 10**10
		else:
			C_Vogel[index_row] = [10**10 for x in C_Vogel[index_row]]


# Function for finding maximums in rows and columns for Russell's method
def find_maximums(grid):
	row_maximums = []
	col_maximums = []

	cols = []
	for columns in range(len(grid[0])):
		cols.append([])

	for row in grid:
		row_copy = row[:]
		row_copy.sort()
		row_maximums.append(row_copy[-1])
		for col in range(len(row)):
			cols[col].append(row[col])

	for col in cols:
		col_copy = col[:]
		col_copy.sort()
		col_maximums.append(col_copy[-1])

	return row_maximums, col_maximums


# Russell's method
while max(D_R) != 0 or max(S_R) != 0:
	rows_m, cols_m = find_maximums(C_R)
	# Subtracting maximal elements of rows and columns from elements of grid
	for row_i in range(len(C_R)):
		for col_i in range(len(C_R[0])):
			C_R[row_i][col_i] -= (rows_m[row_i] + cols_m[col_i])

	# Finding the least negative in grid
	least_negative = 1
	for row_i in range(len(C_R)):
		for col_i in range(len(C_R[0])):
			if C_R[row_i][col_i] != -10**10 and C_R[row_i][col_i] < least_negative:
				least_negative = C_R[row_i][col_i]

	# Updating answer using the least negatives in grid
	for row_i in range(len(C_R)):
		for col_i in range(len(C_R[0])):
			if C_R[row_i][col_i] == least_negative:
				min_sd = min(S_R[row_i], D_R[col_i])

				# Updating answer, supply and demand
				ans_R += min_sd * C[row_i][col_i]
				S_R[row_i] -= min_sd
				D_R[col_i] -= min_sd

				# Updating the grid for future iterations
				if D_R[col_i] == 0:
					for i in range(len(C_R)):
						C_R[i][col_i] = -10**10
				else:
					C_R[row_i] = [-10**10 for x in C_R[row_i]]


# Outputting answers
print(f"Answers:\n{ans_NW}\n{ans_Vogel}\n{ans_R}")
output_file.write(f"Answer of North-West corner method: {ans_NW}\n")
output_file.write(f"Answer of Vogel's approximation method: {ans_Vogel}\n")
output_file.write(f"Answer of Russell's approximation method: {ans_R}")

input_file.close()
output_file.close()
