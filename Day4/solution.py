## General
class Board:
    '''A class to represent and manage the Bingo board.'''

    def __init__(self, board):
        self.board = board
        # Initialize a matrix with same dimensions to track marked numbers
        self.marks = [[False for _ in row] for row in board]

    def __repr__(self):
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.board)

    def marked(self):
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.marks)

    def mark(self, number):
        # Iterate to see if we find the number and mark it
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == number:
                    self.marks[i][j] = True
    
    def has_complete_row(self):
        for row in self.marks:
            if all(row):
                return True
        return False

    def has_complete_column(self):
        # We transpose our board to have a list of columns instead of rows
        transposed_board = list(zip(*self.marks))
        # Then we do the same check as before
        for col in transposed_board:
            if all(col):
                return True
        return False

    def has_won(self):
        return self.has_complete_column() or self.has_complete_row()

    def unmarked_sum(self):
        '''Sum all unmarked numbers in each row, and then sum all of those sums to get the sum of all unmarked numbers'''
        return sum(sum([int(cell) for j, cell in enumerate(row) if not self.marks[i][j]]) for i, row in enumerate(self.board))
    
    @classmethod
    def from_string(cls, board_string):
        """Create a matrix from the string and pass it to our regular constructor"""
        board = [[cell.strip() for cell in row.split(' ') if cell != ''] for row in board_string.split('\n')]
        return cls(board)


# # Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    numbers = f.readline().strip().split(',')
    raw_boards = [raw_board.strip() for raw_board in f.read().split('\n\n')]

boards = [Board.from_string(raw_board) for raw_board in raw_boards]

## Part 1

def find_first_winning_board_score():
    for number in numbers:
        for board in boards:
            board.mark(number)
            if board.has_won():
                return board.unmarked_sum() * int(number)

print(f'The score of the first winning board is {find_first_winning_board_score()}')


## Part 2

def find_last_winning_board_score():
    last_winning_board = None
    incomplete_boards = boards
    for number in numbers:
        for board in incomplete_boards:
            board.mark(number)
            if board.has_won():
                last_winning_board = board
                last_winning_number = number
        # Remove all winning boards from the list and start over
        incomplete_boards = [board for board in incomplete_boards if not board.has_won()]
    return last_winning_board.unmarked_sum() * int(last_winning_number)


print(f'The score of the last winning board is {find_last_winning_board_score()}')
    