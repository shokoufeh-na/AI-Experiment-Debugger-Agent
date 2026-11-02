from openai import OpenAI
import os
from dotenv import load_dotenv

import json

# Load variables from .env
load_dotenv()

NEBIUS_API_KEY = os.environ["NEBIUS_API_KEY"]

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

def analyze_experiment(experiment_data):
    response = client.chat.completions.create(
        model="nvidia/Nemotron-3_5-Lightning",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an ML experiment debugging agent. "
                    "Analyze training results, identify likely problems, "
                    "explain the evidence, and recommend fixes."
                )
            },
            {
                "role": "user",
                "content": experiment_data
            }
        ]
    )

    return response.choices[0].message.content


 
def analyze_experiment_json(experiment_data):
    response = client.chat.completions.create(
        model="nvidia/Nemotron-3_5-Lightning",
        messages=[
            {
                "role": "system",
                "content": """
You are an ML Experiment Debugger Agent.

Analyze the supplied experiment data.

Return ONLY valid JSON with these fields:
{
  "diagnosis": "string",
  "severity": "low, medium, or high",
  "evidence": ["string"],
  "likely_causes": ["string"],
  "recommended_fixes": ["string"],
  "next_experiment": "string"
}

Rules:
- Use actual experiment metrics as evidence.
- Distinguish observed problems from possible causes.
- Do not invent missing metrics or configurations.
- Do not guarantee performance improvements.
- Return JSON only, without Markdown.
"""
            },
            {
                "role": "user",
                "content": experiment_data
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Nemotron returned an empty response.")

    return json.loads(content)


# Test the agent
if __name__ == "__main__":
    experiment_data = """
    Model: CNN
    Dataset: CIFAR-10

    Training accuracy: 94%
    Validation accuracy: 61%

    Training loss: 0.12
    Validation loss: 1.34

    Diagnose this experiment.
    """

    result = analyze_experiment(experiment_data)
    print(result)