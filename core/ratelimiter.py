import time

class RateLimiter:
	def __init__(self, max_calls, period_in_seconds):
		self.delay = float(period_in_seconds) / float(max_calls)
		self.last = 0

	def limit(self):
		since_last = time.time() - self.last
		time.sleep(max(0, self.delay - since_last))
		self.last = time.time()