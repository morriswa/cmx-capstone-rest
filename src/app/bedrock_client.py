
__author__ = "William Morris [morriswa]"


"""
    ask questions to amazon bedrock
"""

import logging
import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from app.exceptions import APIException


__aws_region = os.getenv('AWS_REGION')
__aws_env = os.getenv('AWS_ENVIRONMENT')
__bedrock_client = boto3.client(service_name='bedrock-agent-runtime')
__bedrock_flow_id = os.getenv('AWS_BEDROCK_FLOW_ID')
__bedrock_flow_alias_id = os.getenv('AWS_BEDROCK_FLOW_ALIAS_ID')
__log = logging.getLogger(__name__)


def __invoke_flow(question):
    """
    Invoke an Amazon Bedrock flow and handle the response stream.

    https://docs.aws.amazon.com/bedrock/latest/userguide/flows-multi-turn-invocation.html

    Args:
        input_data: Input data for the flow

    Returns:
        Dict containing flow_complete status, input_required info, and output
    """

    __log.info("Starting flow %s with question %s", __bedrock_flow_id, question)

    request_params = {
        "flowIdentifier": __bedrock_flow_id,
        "flowAliasIdentifier": __bedrock_flow_alias_id,
        "inputs": [{
            "content": {
                "document": question
            },
            "nodeName": "FlowInputNode",
            "nodeOutputName": "document"
        }],
    }

    try:
        response = __bedrock_client.invoke_flow(**request_params)

        input_required = None
        flow_status = ""
        output = []
        # Process the streaming response
        for event in response['responseStream']:
            # Check if flow is complete.
            if 'flowCompletionEvent' in event:
                flow_status = event['flowCompletionEvent']['completionReason']

            # Check if more input us needed from user.
            elif 'flowMultiTurnInputRequestEvent' in event:
                input_required = event

            # Print the model output.
            elif 'flowOutputEvent' in event:
                output.append(event['flowOutputEvent']['content']['document'])

            elif 'flowTraceEvent' in event:
                __log.error("Flow trace:  %s", event['flowTraceEvent'])



    except ClientError as e:
        __log.error("Client error: %s", {str(e)})

    except Exception as e:
        __log.error("An error occurred: %s", {str(e)})

    if status != "SUCCESS":
        raise APIException(f"Flow {__bedrock_flow_id} failed with status {status}")

    # The flow completed successfully.
    __log.info("The flow %s successfully completed.", __bedrock_flow_id)
    return output


def ask(question) -> list[str]:

    return __invoke_flow(question)
