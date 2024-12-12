from mistralclient.api import client
from flask import current_app
import yaml

class MistralService:
    def __init__(self):
        try:
            self.client = client.Client()
        except Exception as e:
            current_app.logger.error(f"Failed to initialize Mistral client: {str(e)}")
            self.client = None

    def start_scan_workflow(self, scan_id):
        workflow_yaml = self._generate_workflow_yaml(scan_id)
        self.client.workflows.create(workflow_yaml)

    def _generate_workflow_yaml(self, scan_id):
        workflow = {
            'version': '2.0',
            'scan_target':
                {'type': 'direct',
                 'input': ['scan_id'],
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
        return yaml.dump(workflow)
