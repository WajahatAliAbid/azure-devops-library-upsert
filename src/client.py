import os
import typing
import msrest.authentication
import azure.devops.connection
import azure.devops.v7_1.task_agent.models as tg_models
class AzureDevOpsClient:
    def __init__(
        self,
        organization_name: str,
        project: str
    ):
        credentials = msrest.authentication.BasicAuthentication("", os.environ.get("AZURE_PAT"))
        org_url = f"https://dev.azure.com/{organization_name}"
        connection = azure.devops.connection.Connection(base_url=org_url, creds=credentials)
        self._project_name = project
        self.task_agent_client = connection.clients.get_task_agent_client()
        self.core_client = connection.clients.get_core_client()
        self.project_id = self.get_project(project).id
        
        self.project_references = [
            {
                'name':  project,
                'projectReference': {
                    'id': self.project_id
                }
            }
        ]
    def get_project(self, name: str):
        projects = self.core_client.get_projects()
        for project in projects:
            if project.name == name:
                return project

    def get_variable_groups(self) -> typing.List[tg_models.VariableGroupParameters]:
        variable_groups = self.task_agent_client.get_variable_groups(project=self._project_name)
        return variable_groups
    
    def get_variable_group(self, name: str) -> tg_models.VariableGroupParameters:
        groups = self.get_variable_groups()
        for group in groups:
            if group.name == name:
                return group
        
    def update_variable_group(self, name: str, variables: typing.Dict[str, str]):
        group = self.get_variable_group(name)
        g_variables = group.variables
        for key, value in variables.items():
            g_variables[key] = tg_models.VariableValue(
                value=value
            )
        group.variable_group_project_references = self.project_references
        self.task_agent_client.update_variable_group(
            variable_group_parameters=group, group_id=group.id
        )