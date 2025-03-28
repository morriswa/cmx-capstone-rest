
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


def __invoke_flow(input_data):
    """
    Invoke an Amazon Bedrock flow and handle the response stream.

    https://docs.aws.amazon.com/bedrock/latest/userguide/flows-multi-turn-invocation.html

    Args:
        input_data: Input data for the flow

    Returns:
        Dict containing flow_complete status, input_required info, and output
    """

    request_params = {
        "flowIdentifier": __bedrock_flow_id,
        "flowAliasIdentifier": __bedrock_flow_alias_id,
        "inputs": [input_data],
    }

    try:
        response = __bedrock_client.invoke_flow(**request_params)

        input_required = None
        flow_status = ""
        output = ""
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
                output += f"{event['flowOutputEvent']['content']['document']}\n"

            elif 'flowTraceEvent' in event:
                __log.error("Flow trace:  %s", event['flowTraceEvent'])

        return {
            "flow_status": flow_status,
            "input_required": input_required,
            "output": output
        }

    except ClientError as e:
        __log.error("Client error: %s", {str(e)})

    except Exception as e:
        __log.error("An error occurred: %s", {str(e)})


def ask(question):

    flow_input_data = {
        "content": {
            "document": question
        },
        "nodeName": "FlowInputNode",
        "nodeOutputName": "document"
    }

    __log.info("Starting flow %s", __bedrock_flow_id)

    # Invoke the flow until successfully finished.
    result = __invoke_flow(flow_input_data)
    status = result['flow_status']
    output = result['output']

    if status != "SUCCESS":
        raise APIException(f"Flow {__bedrock_flow_id} failed with status {status}")

    # The flow completed successfully.
    __log.info("The flow %s successfully completed.", __bedrock_flow_id)
    return output
