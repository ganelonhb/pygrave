"""implements are mixins that add functionality to an object"""

class Implement:
    """The implement base class does not have a Thing ID"""

    def __init__(self, *args, **kwargs):
        self.validate()

    def validate(self):
        pass


