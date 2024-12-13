from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "this tool reads the dataset of the input file"
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
    # Read input JSONL
        with open(argument, 'r') as file:
            data = [json.loads(line) for line in file]

        # Process data (example)
        processed_data = [{"processed": entry} for entry in data]

        # Write output JSONL
        with open('output.jsonl', 'w') as file:
            for entry in processed_data:
                file.write(json.dumps(entry) + '\n')

        return "Processing complete, output written to output.jsonl."
