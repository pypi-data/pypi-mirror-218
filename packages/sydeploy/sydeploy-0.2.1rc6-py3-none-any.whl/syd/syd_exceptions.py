
class MissingSCIDCConfig(Exception):
    def __init__(self, directory):
        super().__init__(f"The directory {directory} must have a syd file.")