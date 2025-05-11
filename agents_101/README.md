# 🐝 AI Agents with BeeAI
_Powering the future of open-source AI agent development_

Based on https://github.com/i-am-bee

* **BeeAI Platform** - The platform to easily discover, run, and compose AI agents from any framework. 
* **BeeAI Framework** - A production-grade framework for building AI agents in either Python or TypeScript. 
* **Agent Communication Protocol (ACP)** - The standard for agent-to-agent communication, built for automation, collaboration, and UI integration.
* **Model Context Protocol (MCP)** - Give AI agents a consistent way to connect with tools, services, and data — no matter where they live or how they're built.

## ⚙️ Setup
1. Copy the `.env.example` file to `.env` and fill in the relevant values:
```bash
cp .env.example .env
```
- `WATSONX_URL` - if using `watsonx.ai` as LLM provider
- `WATSONX_PROJECT_ID` - if using `watsonx.ai` as LLM provider
- `WATSONX_API_KEY` - if using `watsonx.ai` as LLM provider
- `VIRUSTOTAL_API_KEY` - For VirusTotal tools
- `TAVILY_API_KEY` - For Tavily (Search) tools


2. Some labs uses Local MCP servers. These servers requires `Node.js` to run. Recommended is working with `nvm` to switch between Node.js versions - [https://nodejs.org/en/download](https://nodejs.org/en/download) (Tested with version 20)

### Install BeeAI Platform (optional)
0. Start [Ollama](https://ollama.com/)
1. **Install** BeeAI using [Homebrew](https://brew.sh/) (or see the [installation guide](https://docs.beeai.dev/introduction/installation) for other methods):

```sh
brew install i-am-bee/beeai/beeai
brew services start beeai
```
for stopping the service use:
```sh
brew services stop beeai
```

2. **Configure** LLM provider (once):
```sh
beeai env setup
```

#### Ollama config:
- Choose LLM provider: Ollama 💻 local.
- Use the recommended model `llama3.1:8b`.
- Context window size of at least 8k tokens.

#### watsonx.ai config:
- Clone the repo and follow the [instructions](https://github.com/barvhaim/beeai-litellm-watsonx).
- Choose LLM provider: Other 🔧 provide API URL.
- base URL: http://localhost:4000
- API Key: `dummy`
- Model: `meta-llama/llama-3-3-70b-instruct`


## 🧪 Labs
- [Lab 0](./lab_0.py) - Demonstrates the use of the ReAct agent with weather and search tools.
- [Lab 1](./lab_1.py) - Integrates the ReAct agent with VirusTotal tools using MCP for domain and IP analysis.
- [Lab 2](./lab_2.py) - Uses the ReAct agent with Tavily tools for enhanced functionality via MCP.
- [Lab 3](./lab_3.py) - Showcases the ReAct agent with a custom Threat Intelligence tool.
- [Lab 4](./lab_4.py) - Implements a multi-agent workflow for research, weather forecasting, and data synthesis.
- [Lab 5](./lab_5.md) - Integrates the ReAct agent with BeeAI platform.


# 🤖 AI Agents with watsonx Orchestrate
TBD


## 📖 Further readings
- [BeeAI docs](https://docs.beeai.dev/)
- [IBM AgentLab](https://www.ibm.com/docs/en/watsonx/saas?topic=solutions-agent-lab-beta)
- [watsonx Orchestrate](https://www.ibm.com/products/watsonx-orchestrate)
