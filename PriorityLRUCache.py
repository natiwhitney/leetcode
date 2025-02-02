import heapq

class PQLRUCache:
  """Represents the cache, which is able to store and retrieve objects, as well as evict the PQ + LRU object from cache with evict() is called."""

  def __init__(self):
    self.cache = {} # (k -> (v, p, access time-- counter))
    self.prio_heap = []  # will store (priority + usage, key) for easy min extraction
    self.counter = 0 # proxy for access time, an integer

  def _prio_key(self, p: int, at: int) -> str:
    return str(p) + ":" + str(at)

  def put(self, k: str, v: str, p: int) -> None:
    # increment access time
    self.counter += 1 
    # update cache
    self.cache[k] = (v, p, self.counter)
    # push new prio to heap
    prio_key = self._prio_key(p, self.counter)
    heapq.heappush(self.prio_heap, (prio_key, k))

  def get(self, k: str) -> None:
    # if object not in cache, exit
    if k not in self.cache:
      return None

    # grab value, priority from cache
    _, v, p, _ = self.cache[k]
    # increment access time
    self.counter += 1
    # udpate cache
    self.cache[k] = (v, p, self.counter)
    # push new prio to heap
    prio_key = self._prio_key(p, self.counter)
    heapq.heappush(self.prio_heap, (prio_key, k))

    # return value
    return v

  def evict(self) -> None:
  # lazily evict min element from the heap, until up to date key is found

    while self.prio_heap:

      prio_key, k = heapq.heappop(self.prio_heap) # grab the min prio_key

      if k not in self.cache: # already evicted, outdated
        continue # go to next iteration of while loop

      # see if the minimum is up to date in cache!
      _, curr_p, curr_at = self.cache[k]
      if self._prio_key(curr_p, curr_at) == prio_key:
        del self.cache[k] # delete object from cache
        break # exist while loop
