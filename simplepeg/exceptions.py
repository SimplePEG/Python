class GrammarParseError(ValueError):
    """Something is wrong with your PEG grammar"""
    def __init__(self, message, *args):
        self.message = message
        super(GrammarParseError, self).__init__(message, *args)


class TextParseError(ValueError):
    """Something is wrong with your text"""
    def __init__(self, message, *args):
        self.message = message
        super(TextParseError, self).__init__(message, *args)
