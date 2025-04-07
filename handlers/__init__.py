import importlib


def handle(event, context):
    question = event.get("question")
    assert question, "Question is required"
    handler = importlib.import_module(f"handlers.question_{question}")
    return handler.handle(event, context)
