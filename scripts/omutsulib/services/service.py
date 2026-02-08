class OmutsuService:

    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def is_setup(self):
        return True
