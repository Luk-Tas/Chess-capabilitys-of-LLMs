import openai


class AccessBloomZAPI:

    openai.api_key = "xxx"
    openai.api_base = "http://localhost:5001//v1"

    def create_completion(self, prompt: str):
        completion = openai.Completion.create(
            model="xxx",
            prompt=prompt,
            max_tokens=32,
            min_tokens=1,
            temperature=0.7,
            echo=True,
            top_p=0.95,
        )
        return completion.choices[0].text

    def create_prob(self, prompt: str):
        probs = openai.Completion.create(
            model="xxx",
            prompt=prompt,
            max_tokens=0,
            min_tokens=0,
            temperature=1,
            echo=True,
            top_p=0.95,
            logprobs=1
        )
        return probs
