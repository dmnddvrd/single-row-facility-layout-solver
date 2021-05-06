class SrflpError(Exception):

    def __init__(self, message="An error occured in the srflp algorithm"):
        self.message = message
        super().__init__(self.message)

class SrflpInputError(SrflpError):
    
    def __init__(self, message='Incorrect input provided'):
        self.message = message
        super().__init__(self.message)


