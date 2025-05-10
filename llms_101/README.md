# 🤖 Explore LLMs
Using `LangChain` With `watsonx.ai` and `Ollama`

## 📚 LLMs
### ⚙️ How it works
LLMs are a type of neural network architecture that uses self-attention mechanisms to process and generate text. They are trained on large datasets to learn the statistical properties of language, allowing them to generate coherent and contextually relevant text.

### ⚖️ LLMs vs SLMs
- LLMs (Large Language Models) are designed to handle a wide range of tasks and can generate text in a more flexible and creative manner. They are typically trained on vast amounts of data and can understand context, nuances, and even humor.

- SLMs (Small Language Models) are smaller and more specialized models that are often used for specific tasks. They may not have the same level of flexibility or creativity as LLMs, but they can be more efficient and faster for certain applications.

LLMs are generally more powerful and capable of generating high-quality text, while SLMs are more focused on specific tasks and may be more efficient in those areas.

### 🔧 LMs Configuration
- Temperature - Controls the randomness of the model's output. A higher temperature (e.g., 1.0) results in more random outputs, while a lower temperature (e.g., 0.2) makes the output more deterministic.
- Top-p (nucleus sampling) - This parameter controls the diversity of the generated text. It considers the smallest set of words whose cumulative probability exceeds the threshold p. For example, if p=0.9, the model will sample from the top 90% of the probability mass.
- Top-k - This parameter limits the sampling pool to the top k most probable words. For instance, if k=50, the model will only consider the 50 most likely words for generating the next token.
- Max tokens - This parameter sets the maximum number of tokens (words or subwords) that the model can generate in a single response. For example, if max tokens=100, the model will stop generating text after producing 100 tokens.

## ⚙️ Setup
Copy the `.env.example` file to `.env` and fill in the relevant values:
```bash
cp .env.example .env
```
- `LLM_PROVIDER` can be `ollama` or `watsonx`
- `WATSONX_APIKEY` is required if `LLM_PROVIDER` is `watsonx`
- `WATSONX_URL` is required if `LLM_PROVIDER` is `watsonx`
- `WATSONX_PROJECT_ID` is required if `LLM_PROVIDER` is `watsonx`

If `LLM_PROVIDER` is `ollama`, make sure your [Ollama](https://ollama.com) is installed and running.

For using `watsonx.ai` you need an api key. You can get it from [watsonx.ai](https://watsonx.ai/) (Personal internal account for IBMers, log-in with your IBMId).

## 🧪 Labs
To run a lab use `uv run <lab_filename>` for example `uv run lab_0.py`.
- [Lab 0](./lab_0.py) - **Sanity check for LLM**: This lab demonstrates a basic invocation of the LLM to ensure it is running correctly.
- [Lab 1](./lab_1.py) - **Country information retrieval**: This lab uses a prompt template to retrieve information about a country (capital and population) in JSON format.
- [Lab 2](./lab_2.py) - **Summarizing CTI reports**: This lab uses a CTI report as input and generates a structured JSON summary using a prompt template and output parser.
- [Lab 3](./lab_3.py) - **Chained prompts for contextual queries**: This lab demonstrates the use of chained prompts to answer contextual queries, such as determining a person's city of origin and the country of that city in a specified language.

## 📖 Further readings
- ["Attention is All You Need" paper](https://arxiv.org/abs/1706.03762)
- [LLMs leaderboard](https://llm-stats.com)
- [LLM visualization](https://poloclub.github.io/transformer-explainer/)
- [LangChain introduction](https://python.langchain.com/docs/introduction/)
- [watsonx.ai](https://watsonx.ai/)
- [Prompting guide](https://www.promptingguide.ai)
- [HuggingFace](https://huggingface.co/)