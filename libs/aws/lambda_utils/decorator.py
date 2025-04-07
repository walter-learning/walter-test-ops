import os
import json
import traceback
from typing import Type

from pydantic import BaseModel, ValidationError


from .context import Context


def lambda_handler(
    model: Type[BaseModel] | None = None,
    parse_json=True,
    sqs_support=False,
):
    """
    This decorator allow to setup Bugsnag debugging as well as input
    validation using a Pydantic model
    """

    def decorator(function):
        def new_function(event, _=None):
            print("📫 Raw Event before transformation :")
            raw_event = json.dumps(event)
            print(raw_event)  # JSON dump for easier copy/paste

            _event = event
            # Setup a global Bugsnag instance

            try:
                # Detect if the lambda was invoked by function URL or API Gateway
                invoked_from_web = (
                    type(event) is dict and "requestContext" in event.keys()
                )
                invoked_from_sqs = (
                    type(event) is dict and "Records" in event.keys() and sqs_support
                )

                def format_response(_status_code, _body, skip_bugsnag=False):
                    if invoked_from_web:
                        return {
                            "statusCode": _status_code,
                            "headers": {"Content-Type": "application/json"},
                            "body": json.dumps(_body, default=str),
                        }
                    else:
                        if _status_code > 400:
                            e = Exception(_body)
                            e.skip_bugsnag = skip_bugsnag  # type: ignore
                            raise e
                        return json.loads(json.dumps(_body, default=str))

                # In case of invocation from web
                if invoked_from_web:
                    # Authenticate the request
                    if os.environ.get("X_API_KEY"):
                        if event.get("headers", {}).get("x-api-key") != os.environ.get(
                            "X_API_KEY", ""
                        ):
                            return format_response(
                                401,
                                {"message": "Invalid or missing `x-api-key` header"},
                            )

                    # Set the event to the request body
                    try:
                        if parse_json:
                            body = event.get("body", "{}")
                            if type(body) is str:
                                try:
                                    event = json.loads(body)
                                except:
                                    event = body
                            else:
                                event = body
                    except json.JSONDecodeError as e:
                        print("❌", e)

                raw_event = json.dumps(event)

                print("🧰  Handler :", function.__name__)
                print("🌍  Invoked by web :", invoked_from_web)
                if sqs_support:
                    print(
                        "🚚  Invoked by SQS :",
                        invoked_from_sqs,
                        f"({len(event['Records'])})" if invoked_from_sqs else "",  # type: ignore
                    )
                print("📫  Event :")
                print(raw_event)  # JSON dump for easier copy/paste

                if os.environ.get("KILL_SWITCH", None):
                    e = Exception("🔴 Kill switch activated")
                    e.skip_bugsnag = True  # type: ignore
                    raise e

                events = []
                if invoked_from_sqs:
                    for record in event["Records"]:  # type: ignore
                        try:
                            event = json.loads(record["body"])  # type: ignore
                            event["__sqs"] = {
                                "messageId": record["messageId"],  # type: ignore
                                "messageAttributes": record["messageAttributes"],  # type: ignore
                            }
                            events.append(event)
                        except Exception as e:
                            print("🔴", e)
                else:
                    events.append(event)

                for event in events:
                    raw_event_dict = event

                    # Setup a context
                    context = Context(
                        event=raw_event_dict,
                        resource=(_event.get("resource") if type(_event) is dict else None),  # type: ignore
                        path=(_event.get("path", _event.get("rawPath")) if type(_event) is dict else None),  # type: ignore
                        httpMethod=(_event.get("httpMethod") if type(_event) is dict else None),  # type: ignore
                        requestContext=(
                            _event.get("requestContext", {})
                            if type(_event) is dict
                            else {}
                        ),
                        headers=(
                            _event.get("headers", {}) if type(_event) is dict else {}
                        ),
                        multiValueHeaders=(
                            _event.get("multiValueHeaders", {})
                            if type(_event) is dict
                            else {}
                        ),
                        queryStringParameters=(
                            _event.get("queryStringParameters", {})
                            if type(_event) is dict
                            else {}
                        ),
                        multiValueQueryStringParameters=(
                            _event.get("multiValueQueryStringParameters", {})
                            if type(_event) is dict
                            else {}
                        ),
                        pathParameters=(
                            _event.get("pathParameters", {})
                            if type(_event) is dict
                            else {}
                        ),
                    )

                    try:
                        if model:
                            # Perform schema loading and validation if a schema is specified
                            event = model.model_validate(
                                event
                            )  # unknown=EXCLUDE prevent raising ValidationError when unknown fields are supplied

                        # Execute the handler, passing the event and the context
                        response = function(event, context)
                        print("✅  Lambda successfully executed :")
                        print(json.dumps(response, default=str))

                        # Returned a formatted response
                        return format_response(200, response)
                    except ValidationError as e:
                        print("🔴  A ValidationError occurred :")
                        print(e.json())
                        return format_response(400, e.json())
                    except Exception as e:
                        print("🔴  An Exception occurred :")
                        traceback.print_exc()
                        return format_response(
                            500, {"message": "Internal server error"}, skip_bugsnag=True
                        )
            except Exception as e:
                print("🔴  A major Exception occurred :")
                traceback.print_exc()
                raise e

        return new_function

    return decorator
