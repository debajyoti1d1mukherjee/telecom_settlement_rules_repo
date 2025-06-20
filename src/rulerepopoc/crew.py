from dotenv import load_dotenv
from crewai import Crew, Process, Agent, Task
import os
from crewai.project import CrewBase, agent, task, crew as crew_decorator
from rulerepopoc.tools.customtools import FileReadingToolkit
from dotenv import load_dotenv
load_dotenv()

@CrewBase
class SettlementCrew():
    """Settlement crew definition relying on YAML configurations for agents and tasks."""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
       
    inputs = {
        'file_path': {  # Changed from 'path' to 'file_path' to match task expectation
            'type': 'text',
            'label': 'Plan File',
            'description': 'Provide the path to the input plan file',
            'required': True
        }
    }

    @agent
    def file_handler_agent(self) -> Agent:
        return Agent(
			config=self.agents_config['file_handler_agent'],
            tools=[FileReadingToolkit.read_txt_file_tool,
                   FileReadingToolkit.read_docx_file_tool,
                   FileReadingToolkit.read_xlsx_file_tool],
			verbose=True,
			memory=False,
            )

    @agent
    def entity_extractor_agent(self) -> Agent:
        return Agent(
			config=self.agents_config['entity_extractor_agent'],
			# No tools specified for this agent in agents.yaml
			verbose=True,
			memory=False,
		)

    @agent
    def advanced_rating_rule_creator_agent(self) -> Agent:
        return Agent(
			config=self.agents_config['advanced_rating_rule_creator_agent'],
			# No tools specified for this agent in agents.yaml
			verbose=True,
			memory=False,
		)

    @agent
    def drl_generator_agent(self) -> Agent:
        return Agent(
			config=self.agents_config['drl_generator_agent'],
			# No tools specified for this agent in agents.yaml
			verbose=True,
			memory=False,
        )

    @task
    def read_file_task(self) -> Task:
        config = self.tasks_config['read_file_task']
        return Task(
			description=config['description'],
            expected_output=config['expected_output'],
			agent=self.file_handler_agent(),
            human_input=config.get('human_input', False),
            async_execution=config.get('async_execution', False)
		)

    @task
    def extract_entities_task(self) -> Task:
        config = self.tasks_config['extract_entities_task']
        task_instance = Task(
			description=config['description'],
            expected_output=config['expected_output'],
			agent=self.entity_extractor_agent(), 
            async_execution=config.get('async_execution', False)
		)
        task_instance.context = [self.read_file_task()]
        return task_instance

    @task
    def generate_detailed_rating_rules_task(self) -> Task:
        config = self.tasks_config['generate_detailed_rating_rules_task']
        task_instance = Task(
			description=config['description'],
            expected_output=config['expected_output'],
			agent=self.advanced_rating_rule_creator_agent(), 
            async_execution=config.get('async_execution', False)
		)
        task_instance.context = [self.extract_entities_task()]
        return task_instance

    @task
    def generate_drl_task(self) -> Task:
        config = self.tasks_config['generate_drl_task']
        task_instance = Task(
			description=config['description'],
            expected_output=config['expected_output'],
			agent=self.drl_generator_agent(), 
            async_execution=config.get('async_execution', False)
		)
        task_instance.context = [self.generate_detailed_rating_rules_task()]
        return task_instance

    @crew_decorator
    def crew(self) -> Crew:
        """Creates the Settlement crew"""
        return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
            #inputs=self.inputs,
            inputs={ # This is the active inputs definition for the Crew object
                'file_path': { # Changed from 'path' to 'file_path'
                    'type': 'text',
                    'label': 'Plan File',
                    'description': 'Provide the path to the input plan file',
                    'required': True
                }
            }
		)
    

# This is the global `crew` instance that `crewai run crew` would look for.
# It's also what your `if __name__ == "__main__":` block should use.
crew_instance_builder = SettlementCrew()
crew = crew_instance_builder.crew()
 
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Script directory: {script_dir}")
    file_name = "Settlement RFP_Skeleton.xlsx"
    inputs = {'file_path': os.path.join(script_dir, file_name)} # Changed key to file_path

    print(f"\nKicking off the crew with input file: {inputs['file_path']}...\n") # Changed key to file_path
    crew_result = crew.kickoff(inputs=inputs) # Call kickoff on the Crew instance
    print(crew_result)