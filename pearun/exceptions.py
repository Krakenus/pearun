class PearunException(Exception):
    def __init__(self, *args, **kwargs):
        self.parser = kwargs.pop('parser')
        super().__init__(*args)

    def print_help(self):
        self.parser.print_help()


class UnspecifiedCommandException(PearunException):
    pass


class PearunfileException(Exception):
    pass
