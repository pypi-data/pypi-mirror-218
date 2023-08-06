"""
:example:
    >>> from queue import PriorityQueue as BuiltInPriorityQueue
    >>>
    >>> q = BuiltInPriorityQueue()
    >>>
    >>> q.put((4, 'Read'))
    >>> q.put((2, 'Play'))
    >>> q.put((5, 'Write'))
    >>> q.put((1, 'Code'))
    >>> q.put((3, 'Study'))
    >>>
    >>> while not q.empty():
    ...     next_item = q.get()
    ...     print(next_item)
    (1, 'Code')
    (2, 'Play')
    (3, 'Study')
    (4, 'Read')
    (5, 'Write')
"""


class PriorityQueue:
    """
    :usage:
        >>> myQueue = PriorityQueue()
        >>> myQueue.put(12)
        >>> myQueue.put(1)
        >>> myQueue.put(14)
        >>> myQueue.put(7)
        >>> str(myQueue)
        '12 1 14 7'

        >>> while not myQueue.is_empty():
        ...     myQueue.pop()
        14
        12
        7
        1

        >>> myQueue.pop()

    """

    def __init__(self):
        self.queue = []

    def __str__(self):
        return " ".join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def is_empty(self) -> bool:
        return len(self.queue) == 0

    # for inserting an element in the queue
    def put(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def pop(self):
        try:
            max_val = 0
            for i in range(len(self.queue)):
                if self.queue[i] > self.queue[max_val]:
                    max_val = i
            return self.queue.pop(max_val)
        except IndexError:
            return None
