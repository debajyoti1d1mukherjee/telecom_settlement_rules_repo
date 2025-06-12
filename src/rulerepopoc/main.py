import sys
# Import the globally instantiated crew object from crew.py
from rulerepopoc.crew import crew # Changed to import the globally instantiated crew

import os

def run():
    """
    Sets up inputs and kicks off the crew.
    """
    # Define inputs for the crew. This can be made more dynamic if needed.
    # For consistency, using the same example file as in crew.py's __main__ block.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = "MNO_MVNO_Tiered_Agreement.docx" # Or make this configurable
    inputs = {'file_path': os.path.join(script_dir, "..", file_name)} # Assuming main.py is in src/rulerepopoc and file is in src/

    print(f"\nKicking off the crew from main.py with input file: {inputs['file_path']}...\n")
    result = crew.kickoff(inputs=inputs) # Use the imported crew instance directly
    print("\nCrew execution finished. Result:")
    print(result)