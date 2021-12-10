## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    lines = [line.strip() for line in  f.readlines()]

## Part 1
# This dict will help us do the validation
chunk_delimiters = {
    '{' : '}',
    '(' : ')',
    '[' : ']',
    '<' : '>'
}

chunk_starters = chunk_delimiters.keys()
chunk_closers = chunk_delimiters.values()

# And this one the point calculation
illegal_points = {
    ')' : 3,
    ']' : 57,
    '}' : 1197,
    '>' : 25137
}

syntax_error_score = 0
expected_closing_delimiter = []
corrupt_lines = []

for line in lines:
    for char in line:
        if char in chunk_starters:
            expected_closing_delimiter.append(chunk_delimiters[char])
        elif char in chunk_closers and char != expected_closing_delimiter[-1]:
            # This is an illegal closing delimiter
            syntax_error_score += illegal_points[char]
            # This will come in handy in Part 2
            corrupt_lines.append(line)
            break # No need to keep processing this line
        elif char in chunk_closers and char == expected_closing_delimiter[-1]:
            # If we're closing correctly, then we pop from the end to have the next 
            # valid closing delimiter at the end
            expected_closing_delimiter.pop()

print(f'The Syntax Error Score is {syntax_error_score}')

## Part 2
# Compute the incomplete lines
incomplete_lines = [line for line in lines if line not in corrupt_lines]

# Completion points
completion_points = {
    ')' : 1,
    ']' : 2,
    '}' : 3,
    '>' : 4,
}

completion_scores = []
# We can use the same approach as before
for line in incomplete_lines:
    # Start an empty list to track our missing closing delimiters
    missing_closing_delimiter = []
    for char in line:
        if char in chunk_starters:
            missing_closing_delimiter.append(chunk_delimiters[char])
        # The second check should be unnecessary but should always hold true for incomplete lines
        elif char in chunk_closers and char == missing_closing_delimiter[-1]:
            missing_closing_delimiter.pop()
    # At this point we have all the missing closing delimiters in reverse order
    completion_score = 0
    missing_closing_delimiter.reverse()
    for char in missing_closing_delimiter:
        completion_score = completion_score * 5 + completion_points[char]
    completion_scores.append(completion_score)

completion_scores = sorted(completion_scores)
print(f'The middle Completion Score is {completion_scores[len(completion_scores) // 2]}')
    