class DoublyLinkedList:
    """
    Implementation of a doubly linked list
    """
    def __init__(self):
        """
        Declares head and tail nodes
        Initialises length of the list to 0
        """
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        """
        :return: The length of the list
        """
        return self.size

    def __iter__(self):
        """
        Initialises the iteration process by pointing to the head and setting the index to 0
        :return: This list
        """
        self.current = self.head
        self.index = 0
        return self

    def __next__(self):
        """
        Retrieves the current item in the iteration process
        Points to the next node in the list and increments the pointer
        :return: The current item in the iteration process
        """
        if self.index < self.size:
            result = self.current.key
            self.current = self.current.next
            self.index += 1
            return result
        else:
            raise StopIteration

    def __getitem__(self, index):
        """
        Retrieves the item pointed at by index
        Determines whether to traverse from right to left or vice versa according to the index
        :param index: The index in the list to retrieve the item from
        :return: The item at the given index
        """
        if (self.size // 2) > index:
            i = 0
            node = self.head
            while i < index:
                node = node.next
                i += 1
            return node.key
        else:
            i = self.size - 1
            node = self.tail
            while i > index:
                node = node.prev
                i -= 1
            return node.key

    def append_left(self, key):
        """
        Appends a key to the head of the list
        The new node containing this key is returned, which can be used to remove elements in constant time
        :param key: The value to be appended to the left
        :return: A pointer to the node in the list
        """
        if self.size > 0:
            current_head = self.head
            new_node = DoublyLinkedList.DoublyLinkedListNode(self, None, current_head, key)
            current_head.prev = new_node
            self.head = new_node
        else:
            new_node = DoublyLinkedList.DoublyLinkedListNode(self, None, None, key)
            self.head = new_node
            self.tail = new_node

        self.size += 1
        return new_node

    def append_right(self, key):
        """
        Appends a key to the tail of the list
        The new node containing this key is returned, which can be used to remove elements in constant time
        :param key: The value to be appended to the right
        :return: A pointer to the node in the list
        """
        if self.size > 0:
            current_tail = self.tail
            new_node = DoublyLinkedList.DoublyLinkedListNode(self, current_tail, None, key)
            current_tail.next = new_node
            self.tail = new_node
        else:
            new_node = DoublyLinkedList.DoublyLinkedListNode(self, None, None, key)
            self.head = new_node
            self.tail = new_node

        self.size += 1
        return new_node

    class DoublyLinkedListNode:
        """
        Implementation of a node in a doubly linked list
        """
        def __init__(self, list, prev, next, key):
            """
            Initialises a new node with given parameters
            :param list: The list this node belongs to. Used to remove itself from this list in constant time
            :param prev: A pointer to the previous node in the list
            :param next: A pointer to the next node in the list
            :param key: The key that is stored inside the node
            """
            self.key = key
            self.prev = prev
            self.next = next
            self.list = list

        def remove(self):
            """
            Removes itself from the list in which it resides
            Updates pointers of the list and neighbouring nodes accordingly
            """
            if self.list.size > 1:
                if self.prev is None:
                    self.list.head = self.next
                    self.next.prev = None
                elif self.next is None:
                    self.list.tail = self.prev
                    self.prev.next = None
                else:
                    self.prev.next, self.next.prev = self.next, self.prev
            else:
                self.list.head = None
                self.list.tail = None
            self.list.size -= 1
