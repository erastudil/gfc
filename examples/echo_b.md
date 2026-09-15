When the socket dies, the client retries three times with exponential backoff and jitter before it drops the request on the floor.
