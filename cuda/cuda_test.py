from collections import deque

def drawskip(sequence):
    skip = deque(sequence)  # Convert the sequence array to a deque
    insort = []

    while skip:
        x = skip.popleft()  # Pop the element from the skip queue
        insort.append(x)  # Store the element in the sorted array

        if skip:  # Queue the next element
            y = skip.popleft()
            skip.append(y)

    return insort
