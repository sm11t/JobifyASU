import openai

def test_chatgpt_api(api_key, prompt):
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the appropriate model, e.g., gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content'].strip()

def main():
    api_key = "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"  # Replace with your actual API key
    prompt = "Generate a cover letter for a software developer position."

    response = test_chatgpt_api(api_key, prompt)
    print("Generated Response:\n", response)

if __name__ == "__main__":
    main()