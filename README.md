# CODE Sherpa

**Theme:** Open Innovation  
**Project Nature:** *Deterministic Codebase Analysis & Guided Learning Tool*

---

## 📑 Table of Contents

- [CODE Sherpa](#code-sherpa)
  - [📑 Table of Contents](#-table-of-contents)
  - [Problem Statement](#problem-statement)
  - [Background \& Motivation](#background--motivation)
  - [Research \& Observations](#research--observations)
  - [Proposed Solution](#proposed-solution)
  - [Existing Approaches and Identified Gaps](#existing-approaches-and-identified-gaps)
  - [**Unlike IDE navigation tools that expose relationships, CODE Sherpa orders and teaches them as a structured learning path.**](#unlike-ide-navigation-tools-that-expose-relationships-code-sherpa-orders-and-teaches-them-as-a-structured-learning-path)
  - [Current Prototype Overview](#current-prototype-overview)
  - [Conceptual Workflow](#conceptual-workflow)
  - [System Overview](#system-overview)
  - [How to Run the Prototype](#how-to-run-the-prototype)
    - [Prerequisites](#prerequisites)
    - [Quick Start](#quick-start)
    - [Output Files](#output-files)
    - [Viewing Results](#viewing-results)
    - [Expected Output](#expected-output)
    - [Troubleshooting](#troubleshooting)
    - [Testing Individual Components](#testing-individual-components)
  - [System Architecture](#system-architecture)


---

## Problem Statement

Developers frequently struggle to understand large or unfamiliar codebases when joining new projects. Existing approaches rely on static documentation, informal knowledge transfer, or ad-hoc assistance, which fail to clearly explain **code flow**, **inter-file dependencies**, and **underlying design decisions**. As a result, onboarding time increases, errors become more frequent, and developers often hesitate to modify critical parts of the system.

---

## Background & Motivation

Modern software projects grow rapidly in size and complexity, while documentation often becomes outdated or incomplete.

New contributors spend a significant portion of their time navigating unfamiliar files, tracing execution paths, and understanding implicit dependencies across the codebase.

Although tools exist for code navigation, search, and autocomplete, they primarily support **writing new code** rather than **learning an existing system**. This creates a gap where developers rely on trial-and-error and repeated context switching, slowing productivity and contributing to long-term technical debt.

---

## Research & Observations

Research across academia, industry, and developer communities consistently indicates that **understanding existing codebases** is a major challenge in software engineering.

**Key findings from prior work and observations include:**

- **Program comprehension studies** show that developers spend a significant portion of their time reading and understanding existing code rather than writing new functionality, especially during maintenance and onboarding phases.  
  *Program Comprehension – IEEE*  
  https://ieeexplore.ieee.org/document/8468136

- **Developer onboarding research** highlights that new contributors often struggle to build a *system-level mental model* due to implicit design decisions, missing architectural context, and reliance on informal knowledge transfer.  
  *Developer Onboarding – ACM*  
  https://dl.acm.org/doi/10.1145/3196398.3196400

- **Industry productivity reports** frequently identify code comprehension, legacy systems, and onboarding as major bottlenecks, with a substantial share of engineering time spent navigating and tracing existing code rather than implementing new features.  
  *Engineering Productivity – InfoQ*  
  https://www.infoq.com/articles/developer-productivity/

- **Community discussions** on platforms such as Reddit and X reinforce that this difficulty persists across experience levels. Developers often report being able to complete isolated tasks while lacking confidence to modify critical or interconnected parts of a system, even after extended exposure.

Together, these observations suggest that the challenge of understanding codebases is **systemic rather than a skill deficiency**, and that existing tools do not adequately support **structured learning** of complex software systems.

---

## Proposed Solution

CODE Sherpa is designed as a **guided learning system** that helps developers understand unfamiliar codebases in a structured and progressive manner.

Instead of relying on static documentation or reactive question-answering, the system proactively walks a user through key parts of a project—explaining how components are organized, how control flows through the code, and why certain design decisions exist.

The solution analyzes an existing repository to identify important files, modules, and relationships, and then generates an **interactive learning path** tailored to the codebase. Developers can follow this path step-by-step, receiving concise explanations and contextual guidance while navigating the actual source code.

By focusing on **guided exploration** rather than isolated answers, CODE Sherpa aims to reduce onboarding time, lower cognitive load, and increase developer confidence when working with complex or legacy systems.

---

## Existing Approaches and Identified Gaps

Several tools exist to help developers work with unfamiliar codebases, but they address only isolated aspects of the problem and do not provide **structured understanding**.

- **Static documentation (README files, wikis)** focuses on setup and surface-level usage. These documents quickly become outdated and rarely explain internal logic, design rationale, or runtime behavior.

- **IDE navigation tools** (search, go-to-definition, call hierarchies) help locate code elements but require developers to manually explore and infer relationships. They support navigation, not guided comprehension.

- **AI-assisted chat and coding tools** provide reactive explanations based on user queries. While helpful, they depend on the user already knowing what to ask and typically produce fragmented, context-limited insights rather than a holistic view of the system.

Overall, existing approaches emphasize *access to information* rather than *learning the codebase*. This gap motivates the need for a **proactive, step-by-step mechanism** that helps developers form an accurate mental model of a software system.

---
**Unlike IDE navigation tools that expose relationships, CODE Sherpa orders and teaches them as a structured learning path.**
---

## Current Prototype Overview

The CODE Sherpa prototype demonstrates an **end-to-end workflow** for transforming an unfamiliar software repository into a structured, interactive learning experience.

At a high level, the prototype:
- Analyzes a codebase to identify important code segments
- Generates concise explanations and learning checkpoints for those segments
- Presents them as a guided, step-by-step learning flow alongside the source code

**Note:** The current prototype supports **Python repositories only**. It analyzes Python source files (`.py`) using Python's Abstract Syntax Tree (AST) module to extract imports, functions, dependencies, and entry points.

The objective of the prototype is to show how code comprehension can move from an *ad-hoc, manual activity* to a *structured and repeatable learning process*.

---

## Conceptual Workflow

The prototype operates as a **three-stage pipeline**:

1. **Code Analysis**  
   The repository is scanned to identify key files, entry points, and logical code segments, along with their precise locations in the source code.

2. **Guided Tour Generation**  
   Identified code segments are processed to produce grounded explanations and lightweight comprehension checks, which are assembled into an ordered learning sequence.

3. **Interactive Learning Experience**  
   The learning sequence guides developers through the codebase step-by-step, opening relevant files, highlighting important sections, and presenting explanations as the user progresses.

---

## System Overview

The CODE Sherpa system operates as a **deterministic, reproducible pipeline**:

1. **Repository Analysis**: The codebase is analyzed using static analysis to extract verified structural facts such as files, functions, imports, and call relationships.

2. **Learning Path Derivation**: Verified relationships are interpreted to derive an ordered learning path that introduces the codebase progressively and logically.

3. **Structured Outputs**: The derived understanding is presented through structured artifacts, including guided walkthrough data and a visual flowchart representing overall code flow.

This approach emphasizes **structured comprehension** over ad-hoc exploration or reactive assistance.


---

## How to Run the Prototype

### Prerequisites

- **Python 3.7 or higher** (Python 3.12+ recommended)
- **Install dependency:** `requests`
  ```bash
  pip install requests
  ```
- **Optional (for semantic enrichment):**
  - Set `GROQ_API_KEY` in your environment (enables LLM-backed explanations)
  - Internet access (enrichment calls the Groq API)
- **Language Support:** The prototype currently supports **Python repositories only**. It analyzes `.py` files and uses Python's AST (Abstract Syntax Tree) for code analysis.

Verify your Python version:
```bash
python --version
```

### Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd CODE_Sherpa__HackTheWinter-SecondWave
   ```

2. **Install `requests` (if not already installed):**
   ```bash
   pip install requests
   ```

3. **(Optional) Enable semantic enrichment via Groq:**
   ```powershell
   # Windows PowerShell
   $env:GROQ_API_KEY="your_api_key_here"
   ```
   ```bash
   # Linux / Mac
   export GROQ_API_KEY="your_api_key_here"
   ```

4. **Run the pipeline on a repository:**
   ```bash
   python cli/main.py analyze <repository_path>
   ```

   **Example with sample repository:**
   ```bash
   python cli/main.py analyze sample_repo
   ```

   **Example with your own repository:**
   ```bash
   python cli/main.py analyze C:\Users\YourName\Projects\my_project
   ```

### Output Files

After running, the following files will be generated in the `demo/` folder:

- **`demo/analysis.json`** — Complete code analysis including:
  - Entry point detection
  - File-level dependencies
  - Function definitions and call relationships
  - Import statements

- **`demo/enriched_analysis.json`** — Enriched analysis (if enrichment succeeds) including:
  - File-level explanations
  - Function-level explanations
  - Structure-preserving, additive metadata only

- **`demo/learning_order.json`** — Structured learning path with:
  - Ordered list of files to explore
  - Function-level guidance
  - Entry point identification

- **`demo/flowchart.md`** — Visual dependency graph in Mermaid format showing:
  - File-to-file dependencies
  - Code flow visualization

### Viewing Results

**View the analysis:**
```bash
# Windows PowerShell
Get-Content demo/analysis.json

# Windows CMD / Linux / Mac
type demo/analysis.json
```

**View the enriched analysis (if present):**
```bash
Get-Content demo/enriched_analysis.json
```

**View the learning order:**
```bash
Get-Content demo/learning_order.json
```

**View the flowchart:**
```bash
Get-Content demo/flowchart.md
```

The flowchart can be visualized using any Mermaid-compatible viewer (e.g., GitHub, VS Code with Mermaid extension, or online Mermaid editors).

### Expected Output

When you run the command, you should see:
```
Running static analysis...
Analysis completed

Running semantic enrichment...
Enrichment completed

Generating tour...
Tour generated

Generating flowchart...
Flowchart exported

Pipeline completed successfully
```

**Notes:**
- If `GROQ_API_KEY` is **set**, enrichment will attempt to use the Groq API for explanations.
- If `GROQ_API_KEY` is **not set** (or enrichment fails), the pipeline **falls back automatically** and continues using `analysis.json`.

### Troubleshooting

**Encoding errors on Windows:**
If you encounter Unicode encoding issues, set the encoding environment variable:
```powershell
$env:PYTHONIOENCODING="utf-8"
python cli/main.py analyze sample_repo
```

**Repository path not found:**
- Use absolute paths: `python cli/main.py analyze C:\full\path\to\repo`
- Or relative paths: `python cli/main.py analyze ./repo_name`
- Ensure the path exists and contains Python files (`.py` extension)
- **Note:** Only Python repositories are currently supported

**`ModuleNotFoundError: No module named 'requests'`:**
- Install the dependency:
  ```bash
  pip install requests
  ```

**Module not found errors:**
- Ensure you're running from the project root directory
- Verify all folders (`analyzer/`, `cli/`, `tour/`, `flowchart/`, `enrich/`) exist

### Testing Individual Components

You can also run individual components separately:

**Test analyzer only:**
```bash
python -c "from analyzer.analyzer import build_unified_model; import json; result = build_unified_model('sample_repo'); print(json.dumps(result, indent=2))"
```

**Test tour builder:**
```bash
python tour/tour_builder.py demo/analysis.json
```

**Test flowchart builder:**
```bash
python flowchart/flow_builder.py demo/analysis.json
```

**Test explainer:**
```bash
python tour/explainer.py demo/analysis.json demo/learning_order.json
```

- [Execution Flow Diagram](Plannings/diagrams/execution_flow.png)
- [Syatem Architecture Diagram](Plannings/diagrams/system_architecture.png)

---


## System Architecture

CODE-Sherpa is designed as a deterministic, static-analysis–driven system
for understanding codebases through verified structure rather than inference.

The system is organized as a linear pipeline:
source code is statically analyzed into a unified JSON knowledge model,
which is then consumed by independent generators to produce
guided explanations and repository-level flowcharts.