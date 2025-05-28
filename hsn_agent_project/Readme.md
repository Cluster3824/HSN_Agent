# HSN Code Validation and Suggestion Agent

## Project Overview
This project is an intelligent **HSN (Harmonized System Nomenclature) Code Validation and Suggestion Agent**, designed to validate HSN codes and suggest relevant codes based on product descriptions. It is built using **Google ADK (Agent Developer Kit), Ollama llm (llama3.2) LiteLLM, Pandas, OS, and Logging libraries**.

**Key Features**
- **HSN Code Validation**: Checks format, existence, and hierarchical structure.
- **HSN Code Suggestions**: Uses AI-based matching for product descriptions.
- **Structured Responses**: Presents validation results in a clear format.
- **Efficient Data Handling**: Loads and processes Excel files optimally.

---

**Technologies Used**

| Library       |Purpose                                                   |
|--------------|-----------------------------------------------------------|
| **Google ADK**  | Defines agent structure, tools, and response formatting. |
| **LiteLLM**  | Powers intelligent suggestions using LLama models.        |
| **Pandas**   | Handles data preprocessing from the Excel dataset.        |
| **OS**       | Manages file paths and environment interactions.          |
| **Logging**  | Provides structured logging for debugging and tracking.   |

---

**How It Works**

**Loads the dataset** (`HSN_Master_Data.xlsx`).  
**Validates HSN codes** using structured rules.  
**Suggests HSN codes** based on AI-powered text matching.  
**Logs errors and success cases** to ensure robustness.  


**Project Structure**

hsn_agent_project
    |
    |
    __init__.py     # Entry point for running the agent
    agent.py        # Contain logic for the HSN code validation and Suggestion
    HSN_Master_Data.xlsx  # HSC dataset 



