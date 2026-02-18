import re
from typing import Dict, Union


# Intent Detection

def detect_intent(prompt: str) -> str:
    p = prompt.lower()

    if any(word in p for word in ["remember", "save", "store"]):
        return "memory_save"

    if any(word in p for word in ["what is my", "recall", "fetch my"]):
        return "memory_read"

    if any(word in p for word in ["what is", "calculate", "compute"]):
        return "calculator"

    return "unknown"



# Math Expression Extraction

def extract_math_expression(prompt: str) -> str:
    """
    Converts English math into symbolic math expression.
    Example:
    'What is 10 plus 5?' -> '10 + 5'
    """
    p = prompt.lower()

    replacements = {
    "plus": "+",
    "minus": "-",
    "multiplied by": "*",
    "multiply by": "*",
    "times": "*",
    "into": "*",
    "divided by": "/",
    "divide by": "/",
}


    for word, symbol in replacements.items():
        p = p.replace(word, symbol)

    # Remove leading question words
    p = re.sub(r"what is|calculate|compute", "", p)

    # Keep only math-safe characters
    expression = re.findall(r"[0-9+\-*/(). ]+", p)

    return "".join(expression).strip()



# Memory Save Extraction (key, value)
def extract_memory_save(prompt: str) -> Dict[str, str]:
    """
    Example:
    'Remember my cat's name is Fluffy'
    """
    p = prompt.lower()

    # Remove trigger words
    p = re.sub(r"remember|save|store", "", p).strip()

    # Split at ' is '
    if " is " not in p:
        return {}

    left, right = p.split(" is ", 1)

    # Clean key
    key = left.replace("my", "").strip()

    # Clean value
    value = right.strip().capitalize()

    return {"key": key, "value": value}


# Memory Read Extraction (key)

def extract_memory_read(prompt: str) -> Dict[str, str]:
    """
    Example:
    'What is my cat's name?'
    'Recall my dog's name'
    """
    p = prompt.lower()

    p = re.sub(r"what is my|recall|fetch my", "", p)
    p = p.replace("?", "").strip()

    # Remove accidental 'my' if still present
    p = p.replace("my ", "").strip()

    return {"key": p}




# Main Router (Agent Brain)

def route_prompt(prompt: str) -> Dict[str, Union[str, dict]]:
    """
    Core reasoning function.
    Determines which tool to use and prepares its input.
    """
    intent = detect_intent(prompt)

    if intent == "calculator":
        expression = extract_math_expression(prompt)
        return {
            "tool": "calculator",
            "tool_input": expression
        }

    if intent == "memory_save":
        data = extract_memory_save(prompt)
        return {
            "tool": "memory_save",
            "tool_input": data
        }

    if intent == "memory_read":
        data = extract_memory_read(prompt)
        return {
            "tool": "memory_read",
            "tool_input": data
        }

    return {
        "tool": "unknown",
        "tool_input": None
    }


# Test

# if __name__ == "__main__":
#     test_prompts = [
#         "What is 10 plus 5?",
#         "Calculate 7 times 6",
#         "Remember my cat's name is Fluffy",
#         "Store my dog's name is Bruno",
#         "What is my cat's name?",
#         "Recall my dog's name",
#         "Tell me a joke"
#     ]

#     for prompt in test_prompts:
#         print(f"\nPrompt: {prompt}")
#         print(route_prompt(prompt))
