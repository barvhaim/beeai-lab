# 🤖 AI Agents with BeeAI
_Powering the future of open-source AI agent development_

Based on https://github.com/i-am-bee

* **BeeAI platform** - The platform to easily discover, run, and compose AI agents from any framework. 
* **BeeAI framework** - A production-grade framework for building AI agents in either Python or TypeScript. 
* **Agent Communication Protocol (ACP)** - The standard for agent-to-agent communication, built for automation, collaboration, and UI integration.


## 📚 Introduction with Agent Lab
https://www.ibm.com/docs/en/watsonx/saas?topic=solutions-agent-lab-beta

## 🧪 Labs
- [Lab 0](./lab_0.py) - Demonstrates the use of the ReAct agent with weather and Wikipedia tools.
- [Lab 1.1](./lab_1_1.py) - Integrates the ReAct agent with VirusTotal tools using MCP for domain and IP analysis.
- [Lab 1.2](./lab_1_2.py) - Uses the ReAct agent with Tavily tools for enhanced functionality via MCP.
- [Lab 2](./lab_2.py) - Showcases the ReAct agent with a custom Threat Intelligence tool.
- [Lab 3](./lab_3.md) - Work in progress. BeeAI is rebuilding their agent SDK.
- [Lab 4](./lab_4.py) - Implements a multi-agent workflow for research, weather forecasting, and data synthesis.


## BeeAI platform
0. Start [Ollama](https://ollama.com/)
1. **Install** BeeAI using [Homebrew](https://brew.sh/) (or see the [installation guide](https://docs.beeai.dev/introduction/installation) for other methods):

```sh
brew install i-am-bee/beeai/beeai
brew services start beeai
```

2. **Configure** LLM provider:

```sh
beeai env setup
```

3. **Launch** the web interface:

```sh
beeai ui
```

4. **Use** from the terminal:

```sh
# List commands
beeai --help

# List all available agents
beeai list

# Run the chat agent
beeai run chat
```
