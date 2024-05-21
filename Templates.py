class Template:
    templates = dict()

    def __init__(self, name, temp):
        self.name = name

        self.temp = temp

        Template.templates[self.name] = self
