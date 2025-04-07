class LambdaInvocationException(Exception):

    def __init__(self, status_code=500, message="An error occurred while processing your request"):
        super(LambdaInvocationException, self).__init__()
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f"InvocationException({self.status_code}) : {self.message}"
