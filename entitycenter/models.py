class Entity:
    def __init__(self):
        self.name = ""
        self.type = None

    def __str__(self):
        return "{} : {}".format(self.name, self.type)

    def __repr__(self):
        return "{} : {}".format(self.name, self.type)

    def __iter__(self):
        return iter(self.type)
