class TimeRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def to_dict(self):
        return {"start": self.start, "end": self.end}
