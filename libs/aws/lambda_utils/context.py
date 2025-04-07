class Context:

    def __init__(
        self,
        event: dict,
        resource: str,
        path: str,
        httpMethod: str,
        requestContext: dict,
        headers: dict,
        multiValueHeaders: dict,
        queryStringParameters: dict,
        multiValueQueryStringParameters: dict,
        pathParameters: dict,
    ):
        self.event = event
        self.resource = resource
        self.path = path
        self.httpMethod = httpMethod
        self.requestContext = requestContext
        self.headers = headers
        self.multiValueHeaders = multiValueHeaders
        self.queryStringParameters = queryStringParameters
        self.multiValueQueryStringParameters = multiValueQueryStringParameters
        self.pathParameters = pathParameters
