GRAD_SIZE = 9


def num_in_row(board, number, row) -> bool:
    for i in range(9):
        if board[row][i] == number:
            return True
    return False


def num_in_column(board, number, column) -> bool:
    for i in range(9):
        if board[i][column] == number:
            return True
    return False


def num_in_box(board, number, row, column) -> bool:
    local_row = row - row % 3
    local_column = column - column % 3
    for i in range(local_row, local_row + 3):
        for j in range(local_column, local_column + 3):
            if board[i][j] == number:
                return True
    return False
