# Adaptable Priority Queue as a Binary Heap that is used to maintain the open vertices
# Louis Sullivan 119363083

class Element:
    def __init__(self, key, value, index):
        self.key = key
        self.value = value
        self.index = index

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __str__(self):
        return '({}, {}, {})'.format(self.key, self.value, self.index)


class AdaptablePriorityQueue:
    def __init__(self):
        self.elements = []

    def length(self):
        return len(self.elements)

    def isEmpty(self):
        return len(self.elements) == 0

    def parent(self, val):
        return (val - 1) // 2

    def leftChild(self, val):
        return 2 * val + 1

    def rightChild(self, val):
        return 2 * val + 2

    def hasLeft(self, val):
        return self.leftChild(val) < self.length()

    def hasRight(self, val):
        return self.rightChild(val) < self.length()

    def bubbleup(self, val):
        # create parent of val
        parent = self.parent(val)
        # if val index is less than parent index and greater than  0
        if self.elements[val] < self.elements[parent] and val > 0:
            # swap val and parent
            self.swap(val, parent)
            # recursive bubbleup parent
            self.bubbleup(parent)

    def bubbledown(self, val):
        # if val has a left
        if self.hasLeft(val):
            left = self.leftChild(val)
            # set the smaller child variable is left
            small = left
            # if it has a right child
            if self.hasRight(val):
                right = self.rightChild(val)
                # if right is in lower index than the left
                if self.elements[right] < self.elements[left]:
                    # smaller child is on the right
                    small = right
            # if val is greater than the smallest child val
            if self.elements[val] > self.elements[small]:
                # swap val with smallest child
                self.swap(val, small)
                # recursive bubbledown smallest child
                self.bubbledown(small)

    def swap(self, val, other):
        # set values position in the list to other and vice versa
        self.elements[val], self.elements[other] = self.elements[other], self.elements[val]
        # set vals new position to the index it is now at
        self.elements[val].index = val
        # set others new position to the index it is now at
        self.elements[other].index = other

    def add(self, key, value):
        # create the Element object with index being at the bottom of the list
        elt = Element(key, value, self.length())
        # add it to the list
        self.elements.append(elt)
        # bubble up added Element to bottom of tree
        self.bubbleup(self.length() - 1)
        # return element
        return elt

    def min(self):
        # if empty return Error
        if self.isEmpty():
            return "APQ is empty"
        # read first cell in the list
        first = self.elements[0]
        # return the first cell key and value
        return first.key, first.value

    def remove_min(self):
        # if empty return Error
        if self.isEmpty():
            return "APQ is empty"
        else:
            # swap first cell with the last cell
            self.swap(0, self.length() - 1)
            # pop that element
            elt = self.elements.pop(self.length() - 1)
            # bubbledown the first cell
            self.bubbledown(0)
        # return the popped element key and value
        return elt.key, elt.value

    def update_key(self, elt, newkey):
        # get the index of the new element
        i = elt.index
        # set elements key to the newkey
        elt.key = newkey
        # vals index in tree is less than its parent
        if i > 0 and self.elements[i] < self.elements[self.parent(i)]:
            # bubble up val
            self.bubbleup(i)
        else:
            # else bubble down val
            self.bubbledown(i)

    def get_key(self, element):
        # if empty return Error
        if self.isEmpty():
            return "APQ is empty"
        # return the elements key
        return element.key

    def remove(self, element):
        # get elements index
        i = element.index
        # if the element is the last one in the list
        if i == self.length() - 1:
            # pop that element
            self.elements.pop()
        else:
            # swap the element at this index to the last position
            self.swap(i, self.length() - 1)
            # pop the last element
            self.elements.pop()
            # vals position in tree is less than its parent
            if i > 0 and self.elements[i] < self.elements[self.parent(i)]:
                # bubble up val
                self.bubbleup(i)
            else:
                # else bubble down val
                self.bubbledown(i)
            # return that element key and value
            return element.key, element.value

    def __str__(self):
        elt = []
        for e in self.elements:
            elt.append(str(e))
        return ', '.join(elt)
