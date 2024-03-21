"""implements are mixins that add functionality to an object"""

from cython import cclass

@cclass
class CImplement:
    """The implement base class does not have a Thing ID"""

    def __init__(self, *args, **kwargs):
        self.validate()

    def validate(self):
        pass


