import argparse
from test import drawskip


class SequenceTracker:
    def __init__(self):
        self.current_number = 1
        self.next_is_s = False

    def next_value(self):
        if self.next_is_s:
            self.next_is_s = False
            return 'S'
        else:
            value = self.current_number
            self.current_number += 1
            self.next_is_s = True
            return value


def create_matrix(n):
    sequence_tracker = SequenceTracker()
    matrix = []

    # Create the first row
    first_row = [sequence_tracker.next_value() for _ in range(n)]
    matrix.append(first_row)

    while True:
        previous_row = matrix[-1]
        new_row = []
        has_s = False

        for elem in previous_row:
            if elem == 'S':
                new_value = sequence_tracker.next_value()
                new_row.append(new_value)
                if new_value == 'S':
                    has_s = True
            else:
                new_row.append(0)

        matrix.append(new_row)

        if not has_s:
            break

    return matrix


def extract_numeric_values(matrix):
    if not matrix:
        return []

    num_columns = len(matrix[0])
    sequence = []

    for col in range(num_columns):
        for row in matrix:
            if isinstance(row[col], int) and row[col] != 0:
                sequence.append(row[col])
                break

    return sequence


def print_matrix(matrix):
    col_widths = [max(len(str(matrix[row][col])) for row in range(len(matrix))) for col in range(len(matrix[0]))]
    result = ""
    for row in matrix:
        result += "  [" + ", ".join(f"{elem:>{col_widths[i]}}" for i, elem in enumerate(row)) + "],\n"
    print(result)

def is_incremental(array):
    # Iterate through the array up to the second last element
    for i in range(len(array) - 1):
        # Check if the current element is not less than the next element
        if array[i] >= array[i + 1]:
            return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a numeric argument n.')
    parser.add_argument('n', type=int, help='A numeric parameter to be passed to the script')
    args = parser.parse_args()
    n = args.n

    matrix = create_matrix(n)

    print("Matrix:")
    print_matrix(matrix)

    sequence = extract_numeric_values(matrix)
    print("Sequence:", sequence)

    sorted_sequence = drawskip(sequence)
    print("Draw-Skip Test:", sorted_sequence)

    print("Array is sorted:", is_incremental(sorted_sequence))
