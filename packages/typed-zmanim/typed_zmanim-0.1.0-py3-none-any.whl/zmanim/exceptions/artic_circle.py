class ArticCircleException(Exception):
    """Raised when the sun never sets or rises"""
    def __init__(self):
        self.message = "The sun does not set or rise at this location on this date. Zmanim cannot be calculated."