
__author__ = "William Morris [morriswa]"
"""
    easy s3 client, to easily complete application needs
"""

import logging
import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

from dotenv import load_dotenv

load_dotenv('secrets.properties')

__aws_region = os.getenv('AWS_REGION')
__aws_env = os.getenv('AWS_ENVIRONMENT')
__bedrock_agent = boto3.client(service_name='bedrock-agent-runtime')
__log = logging.getLogger(__name__)


def invoke_flow(client, flow_id, flow_alias_id, input_data, execution_id):
    """
    Invoke an Amazon Bedrock flow and handle the response stream.

    https://docs.aws.amazon.com/bedrock/latest/userguide/flows-multi-turn-invocation.html

    Args:
        client: Boto3 client for Amazon Bedrock agent runtime
        flow_id: The ID of the flow to invoke
        flow_alias_id: The alias ID of the flow
        input_data: Input data for the flow
        execution_id: Execution ID for continuing a flow. Use the value None on first run.

    Returns:
        Dict containing flow_complete status, input_required info, and execution_id
    """

    response = None
    request_params = None

    if execution_id is None:
        # Don't pass execution ID for first run.
        request_params = {
            "flowIdentifier": flow_id,
            "flowAliasIdentifier": flow_alias_id,
            "inputs": [input_data],
        }
    else:
        request_params = {
            "flowIdentifier": flow_id,
            "flowAliasIdentifier": flow_alias_id,
            "inputs": [input_data],
        }

    response = client.invoke_flow(**request_params)
    # if "executionId" not in request_params:
    #     execution_id = response['executionId']

    input_required = None
    flow_status = ""

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
            print(event['flowOutputEvent']['content']['document'])

        elif 'flowTraceEvent' in event:
            __log.info("Flow trace:  %s", event['flowTraceEvent'])

    return {
        "flow_status": flow_status,
        "input_required": input_required,
        "execution_id": execution_id
    }


if __name__ == "__main__":

    # Replace these with your actual flow ID and alias ID
    FLOW_ID = 'MPPNBHOE27'
    FLOW_ALIAS_ID = 'QAHH4JAFVZ'

    flow_execution_id = None
    finished = False

    # Get the intial prompt from the user.
    user_input = input("Enter input: ")

    flow_input_data = {
        "content": {
            "document": user_input
        },
        "nodeName": "FlowInputNode",
        "nodeOutputName": "document"
    }

    __log.info("Starting flow %s", FLOW_ID)

    try:
        while not finished:
            # Invoke the flow until successfully finished.

            result = invoke_flow(
                __bedrock_agent, FLOW_ID, FLOW_ALIAS_ID, flow_input_data, flow_execution_id)
            status = result['flow_status']
            flow_execution_id = result['execution_id']
            more_input = result['input_required']
            if status == "INPUT_REQUIRED":
                # The flow needs more information from the user.
                __log.info("The flow %s requires more input", FLOW_ID)
                user_input = input(
                    more_input['flowMultiTurnInputRequestEvent']['content']['document'] + ": ")
                flow_input_data = {
                    "content": {
                        "document": user_input
                    },
                    "nodeName": more_input['flowMultiTurnInputRequestEvent']['nodeName'],
                    "nodeInputName": "agentInputText"

                }
            elif status == "SUCCESS":
                # The flow completed successfully.
                finished = True
                __log.info("The flow %s successfully completed.", FLOW_ID)

    except ClientError as e:
        print(f"Client error: {str(e)}")
        __log.error("Client error: %s", {str(e)})

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        __log.error("An error occurred: %s", {str(e)})
        __log.error("Error type: %s", {type(e)})
