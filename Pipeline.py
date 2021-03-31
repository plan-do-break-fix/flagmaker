

class Task:

    def __init__(self):
        self.path_in = ""
        self.path_out = ""
        self.processes = []

class Pipeline:

    def __init__(self):
        self.methods = {}
        self.tasks = []

    def run(self, task: Task) -> None:
        