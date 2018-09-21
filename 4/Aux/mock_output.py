class MockOutput:
    def __init__(self):
        self.results = []

    def write(self, string):
        self.results.append(string)

    def equal(self, json_list):
        return self.results == json_list