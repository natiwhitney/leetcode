# implement get/put in amortized O(1)
class Node:
    """Represents an element in the cache, including its positioning in the DLL
    ordered by how recently an object was accessed."""
    def __init__(self, key: int, val:int):
        """Initializes a Node object.

        Args:
            key (int): The key used to access the value.
            val (int): The value stored in cache.
        """
        self.key = key
        self.val = val
        self.next = None # pointer to less recently accessed Node
        self.prev = None # pointer to more recently accessed Node

class LRUCache:
    """Represents the cache, which is able to store and retrieve objects, as well as evict the LRU object from cache when capacity is exceeded."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # hashmap (key->Node)
        self.head = Node(0,0) # dummy head for DLL, to avoid edge cases
        self.tail = Node(100,0) # dummy tail for DLL, to avoid edge cases
        self.head.next = self.tail # initialize head to point to tail
        self.tail.prev = self.head # initialize tail to point to head

    def _remove_from_dll(self, node:Node) -> None:
        """Helper function that removes an arbitrary node from a DLL.

        Args:
            node (Node): The node to remove.
        """ 
        node.next.prev = node.prev
        node.prev.next = node.next

        node.prev = None
        node.next = None

    def _insert_after_head(self, node: Node) -> None:
        """Helper function that adds a node to the head of a DLL.

        Args:
            node (Node): The new MRU node.
        """
        curr_mru = self.head.next

        # update forward points, left to right
        self.head.next = node
        node.next = curr_mru

        # update backward pointers, right to left
        curr_mru.prev = node
        node.prev = self.head

    def _move_after_head(self, node: Node) -> None:
        """Helper function that makes an existing node the MRU.

        Args:
            node (Node): the existing node to move to head
        """
        self._remove_from_dll(node)
        self._insert_after_head(node)

    def get(self, key: int) -> int:
        """Return the value of the key, if it exists. Otherwise return -1.
         Set key as MRU.

        Args:
            key (int): The key used to access the value.
        """
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_after_head(node)
        return node.val

    def put(self, key: int, val: int) -> None:
        """Update the value of the key if it exists or add the k-v to the cache. Check if number
        of keys exceeds capacity, if so, evict the LRU key.

        Args:
            key (int): The key used to access the value.
            val (int): The value in cache
        """

        if key in self.cache: 
            # Update existing node
            existing_node = self.cache[key]
            existing_node.val = val
    
            # Move existing node to head
            self._move_after_head(existing_node)
        else:
            # Create a new node
            new_node = Node(key, val)
            self.cache[key] = new_node

            # Insert new node at head
            self._insert_after_head(new_node)

            # Evict if we exceed capacity
            if len(self.cache) > self.capacity:
                self._evict_()

    def _evict_(self) -> None:
        """Helper function that removes the LRU item from the DLL.
        """
        # Evict node from DLL
        lru = self.tail.prev
        self._remove_from_dll(lru)

        # Remove node from cache!
        del self.cache[lru.key]
