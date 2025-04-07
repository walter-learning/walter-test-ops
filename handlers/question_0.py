from libs.aws.lambda_utils import lambda_handler


@lambda_handler()
def handle(event, context):
    print("👋 Hello, World!")
    return {}
