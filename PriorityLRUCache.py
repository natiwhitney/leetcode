class PQLRUCache:
  """Represents the cache, which is able to store and retrieve objects, as well as evict the PQ + LRU object from cache with evict() is called."""

  def __init__(self):
    self.cache = [] # array of 4-length arrays, (k, v, p, access time-- counter)
    self.key_dict = {} # map keys to their index (k, i)
    self.prio_dict = {} # map prio+access time to their index (p+at, i)
    self.counter = 0 # proxy for access time, an integer
    
  def put(self, k: str, v: str, p: int) -> None:
    self.counter += 1 # increment access time
    at = self.counter
    obj = [k, v, p, at]
    prio = self._prio_key(p, at)
    # override existing object in cache
    if k in self.key_dict:
      i = self.key_dict[k]
      ## 1) update prio_dict
      _, _, p_prior, at_prior = self.cache[i]
      prio_prior = self._prio_key(p_prior, at_prior)
      del self.prio_dict[prio_prior]
      self.prio_dict[prio] = i
      ## 2) update cache
      self.cache[i] = obj
      ## 3) update key_dict -- N/A
    # add new object to cache
    else:
      ## 1) update_prio dict
      self.prio_dict[prio] = len(self.cache)
      ## 2) append to cache
      self.cache.append(obj)
      ## 3) update key_dict
      self.key_dict[k] = len(self.cache) - 1


  def _prio_key(self, p: int, at: int) -> str:
    return str(p) + ":" + str(at)
    
  def get(self, k: str) -> None:
    # if object not in cache, exit
    if k not in self.key_dict:
      return None

    # if obj in cache, update access time & override object in cache
    self.counter += 1
    i = self.key_dict[k]
    _, v, p, _ = self.cache[i]
    self.cache[i] = [k, v, p, self.counter]
    # return value
    return v

  def evict(self) -> None:
    # find the object(s) with the lowest priority, and then earliest access time
    min_prio = min(self.prio_dict)
    # grab its index
    i = self.prio_dict[min_prio]
    # grab its key from cache
    k, _, _, _ = self.cache[i]
    # delete its prio from min_prio
    del self.prio_dict[min_prio]
    # delete its object from cache
    del self.cache[i]
    # delete its index from key_dict
    del self.key_dict[k]

    
    


    
    
      
     
