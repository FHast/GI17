class DoublyLinkedList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        self.current = self.head
        self.index = 0
        return self

    def __next__(self):
        if self.index < self.size:
            result = self.current.key
            self.current = self.current.next
            self.index += 1
            return result
        else:
            raise StopIteration

    def __getitem__(self, index):
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
        def __init__(self, list, prev, next, key):
            self.key = key
            self.prev = prev
            self.next = next
            self.list = list

        def remove(self):
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
