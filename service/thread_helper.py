import threading


class ThreadHelper:
    def __init__(self):
        self.threads = []
        self.results = {}
        self.lock = threading.Lock()

    def run_in_threads(self, function, args, key):
        def target():
            result = function(*args)
            with self.lock:
                self.results[key] = result

        thread = threading.Thread(target=target)
        thread.start()
        self.threads.append(thread)

    def wait_for_completion(self):
        for thread in self.threads:
            thread.join()

    def clear(self):
        self.threads = []
        self.results = {}
