import threading


class Worker(threading.Thread):
    def __init__(self, function, in_queue):
        self.function = function
        self.in_queue = in_queue
        super(Worker, self).__init__()

    def run(self):
        while True:
            if self.in_queue.empty():
                break
            data = self.in_queue.get()
            self.function(*data)
            self.in_queue.task_done()