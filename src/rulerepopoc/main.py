import os
from rulerepopoc.crew import SettlementCrew  # make sure this path is correct

def start_crew(input_file_name: str):
    """
    Sets up inputs using the provided input_file_name and kicks off the crew.
    """
    # Create an instance of SettlementCrew
    crew_instance = SettlementCrew()

    # Build input path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", input_file_name)
    inputs = {'file_path': input_path}

    print(f"\nKicking off the crew with input file: {inputs['file_path']}...\n")
    
    result = crew_instance.crew().kickoff(inputs=inputs)
    
    print("\nCrew execution finished. Result:")
    print(result)

 #if __name__ == "__main__":
     #run("MNO_MVNO_Tiered_Agreement.docx")  # Or replace with dynamic value
