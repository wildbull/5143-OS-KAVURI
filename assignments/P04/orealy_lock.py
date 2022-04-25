import threading

class ReadWriteLock:
    """ A lock object that allows many simultaneous "read locks", but
    only one "write lock." """

    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock(  ))
        self._readers = 0
        self._writers = 0

    def acquire_read(self):
        """ Acquire a read lock. Blocks only if a thread has
        acquired the write lock. """
        self._read_ready.acquire(  )
        try:
            self._readers += 1
        finally:
            self._read_ready.release(  )

    def release_read(self):
        """ Release a read lock. """
        self._read_ready.acquire(  )
        try:
            self._readers -= 1
            if not self._readers:
                self._read_ready.notifyAll(  )
        finally:
            self._read_ready.release(  )

    def acquire_write(self):
        """ Acquire a write lock. Blocks until there are no
        acquired read or write locks. """
        self._read_ready.acquire(  )
        while self._readers > 0:
            self._read_ready.wait(  )
        self._writers += 1

    def release_write(self):
        """ Release a write lock. """
        self._read_ready.release(  )
        self._writers -= 1
#----------------------------------------------------------------------------------------------------------

class ReadRWLock:
  # Context Manager class for ReadWriteLock
  def __init__(self, rwLock):
    self.rwLock = rwLock

  def __enter__(self):
    self.rwLock.acquire_read()
    return self         # Not mandatory, but returning to be safe

  def __exit__(self, exc_type, exc_value, traceback):
    self.rwLock.release_read()
    return False        # Raise the exception, if exited due to an exception

#----------------------------------------------------------------------------------------------------------

class WriteRWLock:
  # Context Manager class for ReadWriteLock
  def __init__(self, rwLock):
    self.rwLock = rwLock

  def __enter__(self):
    self.rwLock.acquire_write()
    return self         # Not mandatory, but returning to be safe

  def __exit__(self, exc_type, exc_value, traceback):
    self.rwLock.release_write()
    return False        # Raise the exception, if exited due to an exception

#----------------------------------------------------------------------------------------------------------

