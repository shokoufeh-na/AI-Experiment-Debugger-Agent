from openai import OpenAI
import os
from dotenv import load_dotenv

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