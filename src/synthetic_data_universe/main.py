#!/usr/bin/env python
import sys
import warnings
import openai

from synthetic_data_universe.crew import SyntheticDataUniverse

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


#using Gaianet LLM
openai.api_base = "https://0x4a9a395e9b969605c51d5e655bcaf60d1558ff7a.us.gaianet.network"


import json

def run():
    """
    Run the crew.
    """
    with open('input.jsonl', 'r') as file:
        inputs = [json.loads(line) for line in file]

    # Assuming the first entry in the list is the correct input
    if inputs:
        SyntheticDataUniverse().crew().kickoff(inputs=inputs[0])
    else:
        raise ValueError("No inputs found in input.jsonl")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        SyntheticDataUniverse().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SyntheticDataUniverse().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        SyntheticDataUniverse().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
