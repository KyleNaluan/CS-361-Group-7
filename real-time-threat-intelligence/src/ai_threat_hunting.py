import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("../api/OSINT.env")

# Function to predict threat behavior using GPT-4
def predict_threat_behavior(threat_description):
    prompt = f"Analyze this security threat and predict possible next attack vectors: {threat_description}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Example Usage
threat_description = "SQL Injection detected on login page"
prediction = predict_threat_behavior(threat_description)
print(f"Predicted Next Steps: {prediction}")
