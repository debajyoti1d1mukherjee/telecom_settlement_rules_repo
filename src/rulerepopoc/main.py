import os
from rulerepopoc.crew import SettlementCrew

def run(inputs: dict):
    """
    Entrypoint for CrewAI CLI and Cloud.
    Expects `inputs` to include a "file_path" string.
    """
    file_path = inputs.get("file_path")
    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError(f"Invalid or missing 'file_path' input: {file_path!r}")

    # Resolve the path relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.normpath(os.path.join(base_dir, "..", file_path))
    
    if not os.path.isfile(full_path):
        raise FileNotFoundError(f"File not found at provided path: {full_path}")

    print(f"\n Running Crew with file: {full_path}\n")
    crew_instance = SettlementCrew()
    result = crew_instance.crew().kickoff(inputs={"file_path": full_path})
    
    print("\nCrew run finished. Result:")
    print(result)
    return result

if __name__ == "__main__":
    # Local test — replace with a real file path
    run({"file_path": "MNO_MVNO_Tiered_Agreement.docx"})
