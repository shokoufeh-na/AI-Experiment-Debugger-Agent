# AI-Experiment-Debugger-Agent

An AI-powered agent for analyzing machine learning experiments, diagnosing training problems, and recommending better experiment configurations using **NVIDIA Nemotron models** served through **Nebius Token Factory**.

Built for the **Nebius x NVIDIA Global AI Hackathon 2026**.

##  Overview

Machine learning experimentation often requires manually inspecting training logs, metrics, hyperparameters, and previous runs to understand why a model failed or underperformed.

**AI Experiment Debugger Agent** helps automate this process.

The system analyzes ML experiment information such as:

- Training and validation loss
- Training and validation accuracy
- Hyperparameters
- Model configuration
- Training logs
- Previous experiments

It then uses an NVIDIA Nemotron model to identify potential problems, explain the evidence behind its diagnosis, and recommend changes for the next experiment.

For example:

```text
Training Accuracy:   94%
Validation Accuracy: 61%

Training Loss:       0.12
Validation Loss:     1.34
```

The agent may identify:

```text
Diagnosis: Overfitting

Evidence:
Large training-validation performance gap and increasing validation loss.

Recommended Actions:
- Increase dropout
- Add weight decay
- Apply early stopping
- Consider reducing model complexity

Suggested Next Experiment:
Dropout: 0.4
Weight Decay: 1e-4
```

---

## 🎯 Project Goal

The goal is to build an AI assistant that acts as an **ML experiment debugging and decision-support agent**.

Instead of manually comparing experiment results, users can provide their training metrics and logs and receive structured analysis of:

1. **What went wrong**
2. **Why it likely happened**
3. **What evidence supports the diagnosis**
4. **What should be changed in the next experiment**

---

## ✨ Features

### Current / MVP

- Analyze ML training and validation metrics
- Detect common training problems
- Generate explanations using NVIDIA Nemotron
- Recommend potential corrective actions
- Suggest configurations for the next experiment
- Simple interactive user interface

### Planned

- Training-log file upload
- Experiment history
- Comparison between multiple experiments
- Persistent experiment memory
- Retrieval of similar previous experiments
- Automatic hyperparameter recommendations
- Experiment visualization
- Structured JSON analysis
- Background experiment analysis
- Nebius deployment

---

## 🧠 Problems the Agent Can Analyze

The agent is designed to help identify problems such as:

- Overfitting
- Underfitting
- Learning-rate problems
- Class imbalance
- Training instability
- Poor convergence
- Data-quality problems
- GPU memory errors
- Batch-size issues
- Ineffective hyperparameter configurations

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │   User / ML Engineer │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Streamlit UI      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Experiment Analyzer │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ NVIDIA Nemotron     │
                    │ Nebius Token Factory│
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
        Diagnosis          Evidence       Recommendations
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Experiment Report   │
                    └─────────────────────┘
```

---

## 🔄 Agent Workflow

```text
Experiment Metrics / Logs
          ↓
Parse Experiment Data
          ↓
Retrieve Previous Experiments
          ↓
NVIDIA Nemotron Analysis
          ↓
Identify Training Problems
          ↓
Explain Supporting Evidence
          ↓
Recommend Corrective Actions
          ↓
Suggest Next Experiment
```

---

## 🛠️ Tech Stack

**AI / LLM**

- NVIDIA Nemotron
- Nebius Token Factory

**Backend**

- Python
- FastAPI
- OpenAI-compatible API

**Frontend**

- Streamlit

**ML / Data**

- NumPy
- Pandas
- scikit-learn

**Infrastructure**

- Nebius AI Cloud
- Nebius Token Factory
- Docker

---

## 📁 Project Structure

```text
ai-experiment-debugger/
│
├── app.py
├── agent.py
├── nebius_client.py
├── prompts.py
│
├── utils/
│   ├── log_parser.py
│   └── experiment_parser.py
│
├── data/
│   └── experiments/
│
├── tests/
│   └── test_agent.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-experiment-debugger.git

cd ai-experiment-debugger
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
NEBIUS_API_KEY=your_api_key_here
NEBIUS_BASE_URL=your_token_factory_endpoint
NEMOTRON_MODEL=your_nemotron_model
```

Do **not** commit `.env` or API keys to GitHub.

An example configuration is provided in:

```text
.env.example
```

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Then open the local address displayed by Streamlit, typically:

```text
http://localhost:8501
```

---

## 🤖 NVIDIA + Nebius Integration

The project uses an **NVIDIA open-source Nemotron model** as its primary LLM reasoning engine.

Nemotron inference is performed through **Nebius Token Factory**.

Conceptually:

```text
AI Experiment Debugger
        │
        ▼
Experiment Prompt
        │
        ▼
Nebius Token Factory API
        │
        ▼
NVIDIA Nemotron
        │
        ▼
Structured Analysis
        │
        ▼
Diagnosis + Recommendations
```

The Nemotron model is responsible for reasoning over experiment results, identifying likely training problems, explaining supporting evidence, and generating recommendations.

---

## 💾 Experiment Memory

A planned component of the system is persistent experiment memory.

Instead of analyzing each experiment independently, the agent will be able to retrieve relevant previous experiments.

For example:

```text
Experiment #12
Learning Rate: 0.001
Validation Accuracy: 82%

Experiment #17
Learning Rate: 0.01
Validation Accuracy: 63%

Experiment #21
Learning Rate: 0.0005
Validation Accuracy: 86%
```

When a new experiment is analyzed, the agent can use previous results as additional context before recommending the next configuration.

This creates the workflow:

```text
New Experiment
      ↓
Retrieve Similar Experiments
      ↓
Compare Previous Results
      ↓
Nemotron Reasoning
      ↓
Diagnosis
      ↓
Recommended Next Experiment
```

---

## 🗺️ Roadmap

- [ ] Connect NVIDIA Nemotron through Nebius Token Factory
- [ ] Implement experiment-analysis agent
- [ ] Create structured diagnosis output
- [ ] Build Streamlit interface
- [ ] Add training-log upload
- [ ] Add experiment history
- [ ] Add persistent memory
- [ ] Add experiment similarity search
- [ ] Add experiment comparison
- [ ] Add visualizations
- [ ] Add automated hyperparameter recommendations
- [ ] Containerize with Docker
- [ ] Deploy application
- [ ] Add public demo

---

## 🏆 Hackathon

This project is being developed for the **Nebius x NVIDIA Global AI Hackathon 2026**.

**Track:** Best Apps and Agents

The project uses:

- NVIDIA open-source Nemotron models
- Nebius Token Factory
- AI agent workflows
- ML experiment analysis
- Persistent experiment memory

---

## 🔒 Security

API keys and credentials should never be committed to the repository.

The `.gitignore` file should include:

```gitignore
.env
venv/
.venv/
__pycache__/
*.pyc
.DS_Store
```

---

## 📊 Project Status

🚧 **Currently under active development for the Nebius x NVIDIA Global AI Hackathon 2026.**

The initial MVP focuses on connecting Nebius Token Factory with NVIDIA Nemotron and producing structured ML experiment diagnoses.

---

## 📄 License

This project is released under an open-source license. See the `LICENSE` file for details.

---

## 👩‍💻 Author

**S. Namazian **

Graduate Computer Science Student  
AI / Machine Learning / LLM Research
 
