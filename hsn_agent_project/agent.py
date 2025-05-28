from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from pydantic import BaseModel
import pandas as pd
import os
import logging

#Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HSNCodeAgent")

#Load and preprocess HSN data
DATA_PATH = "/home/cluster-007/Documents/new/hsn_agent_project/HSN_SAC.xlsx"

try:
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"HSN data file not found at: {DATA_PATH}")
    
    hsn_df = pd.read_excel(DATA_PATH, engine="openpyxl")
    hsn_df.columns = hsn_df.columns.str.strip()

    if 'HSNCode' not in hsn_df.columns or 'Description' not in hsn_df.columns:
        raise ValueError("Excel file must contain 'HSNCode' and 'Description' columns.")

    hsn_df['HSNCode'] = hsn_df['HSNCode'].astype(str).str.strip()
    hsn_df['Description'] = hsn_df['Description'].astype(str).str.strip()

    logger.info("HSN data loaded and preprocessed successfully.")

except Exception as e:
    logger.exception("Error during HSN data loading:")
    raise

#Input Schemas
class HsnValidationInput(BaseModel):
    hsn_codes: list[str]

class HsnSuggestionInput(BaseModel):
    description: str

#Validation Tool
def validate_hsn(hsn_codes: list[str]) -> dict:
    valid = []
    invalid = []

    for raw_code in hsn_codes:
        code = str(raw_code).strip()

        if not code.isdigit() or len(code) not in {2, 4, 6, 8}:
            invalid.append(f"{code} (Invalid format)")
            continue

        if code in hsn_df['HSNCode'].values:
            desc = hsn_df.loc[hsn_df['HSNCode'] == code, 'Description'].values[0]
            result = f"{code}: {desc}"

            parent_codes = [code[:i] for i in (2, 4, 6) if i < len(code)]
            missing_parents = [p for p in parent_codes if p not in hsn_df['HSNCode'].values]
            if missing_parents:
                result += f"Missing parent codes: {', '.join(missing_parents)}"

            valid.append(result)
        else:
            invalid.append(f"{code} (Not found in dataset)")

    return {
        "valid_codes": valid,
        "invalid_codes": invalid
    }

#Suggestion Tool
def suggest_hsn(description: str) -> str:
    description = description.strip()
    if not description:
        return "Error: Description cannot be empty."

    prompt = (
        "You are a classifier for HSN codes.\n"
        f"Given this goods/services description:\n\"{description}\"\n\n"
        "Select the most appropriate HSN code(s) from the list below:\n"
        f"{hsn_df[['HSNCode', 'Description']].to_string(index=False)}\n\n"
        "Return the best match code(s) and justify your choice clearly."
    )

    try:
        return llama.call(prompt)
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return f"Suggestion failed due to LLM error: {e}"

#LLM Setup
MODEL = "llama3.2"
llama = LiteLlm(model=f"ollama_chat/{MODEL}")

#Agent Registration
root_agent = Agent(
    name="hsn_code_agent",
    model=llama,
    instruction="You are a helpful assistant for validating and suggesting HSN codes.",
    description="An HSN code validator and suggester.",
    tools=[validate_hsn, suggest_hsn]
)
