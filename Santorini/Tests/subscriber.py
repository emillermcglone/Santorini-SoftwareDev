class Subscriber:
    def __init__(self):
        self.value = ""

    def handle(self, message):
        self.value = message