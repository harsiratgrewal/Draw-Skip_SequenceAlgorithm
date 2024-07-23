import argparse
from cuda_test import drawskip
import numpy as np
from numba import cuda, int32, boolean


@cuda.jit
def create_matrix_kernel(previous_row, new_row, sequence_tracker_values, sequence_tracker_index):
    idx = cuda.grid(1)
    if idx < len(previous_row):
        if previous_row[idx] == -1:
            new_row[idx] = sequence_tracker_values[sequence_tracker_index[0]]
            sequence_tracker_index[0] += 1
        else:
            new_row[idx] = 0


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

    first_row = [sequence_tracker.next_value() for _ in range(n)]
    matrix.append(first_row)

    while True:
        previous_row = matrix[-1]
        new_row = [0] * len(previous_row)

        previous_row_numeric = [-1 if x == 'S' else x for x in previous_row]

        threads_per_block = 16
        blocks_per_grid = (len(previous_row_numeric) + (threads_per_block - 1)) // threads_per_block

        d_previous_row = cuda.to_device(np.array(previous_row_numeric, dtype=np.int32))
        d_new_row = cuda.device_array(len(previous_row_numeric), dtype=np.int32)

        sequence_tracker_values = np.array([sequence_tracker.next_value() for _ in range(n)], dtype=np.int32)
        sequence_tracker_index = np.array([0], dtype=np.int32)

        create_matrix_kernel[blocks_per_grid, threads_per_block](
            d_previous_row, d_new_row, sequence_tracker_values, sequence_tracker_index
        )

        new_row_numeric = d_new_row.copy_to_host()

        new_row = ['S' if x == -1 else x for x in new_row_numeric]

        matrix.append(new_row)

        if not any(x == 'S' for x in new_row):
            break

        sequence_tracker.current_number = len(sequence_tracker_values)
        sequence_tracker.next_is_s = True

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
    for i in range(len(array) - 1):
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
