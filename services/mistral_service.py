import logging
import yaml
from flask import current_app
from mistralclient.api import client

class MistralService:
    def __init__(self):
        """
        Initializes the Mistral client. Logs any errors that occur during initialization.
        """
        try:
            self.client = client.Client()
            current_app.logger.info("Mistral client initialized successfully.")
        except Exception as e:
            current_app.logger.error(f"Failed to initialize Mistral client: {str(e)}")
            self.client = None

    def start_scan_workflow(self, scan_id):
        """
        Starts a scan workflow in Mistral by generating the workflow YAML
        and creating it in Mistral.

        Args:
            scan_id (int): The ID of the scan to start the workflow for.
        """
        if not self.client:
            current_app.logger.error("Mistral client is not initialized. Cannot start scan workflow.")
            return
        
        try:
            # Generate the workflow YAML based on the scan_id
            workflow_yaml = self._generate_workflow_yaml(scan_id)
            # Create the workflow in Mistral
            current_app.logger.info(f"Starting workflow for scan_id {scan_id}.")
            self.client.workflows.create(workflow_yaml)
            current_app.logger.info(f"Workflow for scan_id {scan_id} initiated successfully.")
        except Exception as e:
            current_app.logger.error(f"Failed to start workflow for scan_id {scan_id}: {str(e)}")

    def _generate_workflow_yaml(self, scan_id):
        """
        Generates the workflow YAML for the scan. This includes a set of tasks
        for fetching the target, running a vulnerability scan, analyzing results,
        and storing the findings.

        Args:
            scan_id (int): The ID of the scan to generate the workflow for.

        Returns:
            str: The generated workflow YAML as a string.
        """
        try:
            workflow = {
                'version': '2.0',
                'scan_target': {
                    'type': 'direct',
                    'input': [str(scan_id)],  # Ensure the scan_id is correctly formatted
                    'tasks': {
                        'fetch_target': {
                            'action': 'sql-query',
                            'input': {'query': f'SELECT target_url FROM scans WHERE id={scan_id}'}
                        },
                        'run_vulnerability_scan': {
                            'action': 'security.scan_target',
                            'requires': ['fetch_target']
                        },
                        'analyze_results': {
                            'action': 'ml.analyze_vulnerabilities',
                            'requires': ['run_vulnerability_scan']
                        },
                        'store_results': {
                            'action': 'snowflake.store_findings',
                            'requires': ['analyze_results']
                        }
                    }
                }
            }

            # Convert workflow dictionary to a formatted YAML string
            return yaml.dump(workflow, default_flow_style=False)
        
        except Exception as e:
            current_app.logger.error(f"Failed to generate workflow YAML for scan_id {scan_id}: {str(e)}")
            raise  # Re-raise the exception to be handled by the caller
