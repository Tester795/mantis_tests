from suds.client import Client
from suds import WebFault

from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        project_list = []
        items = client.service.mc_projects_get_user_accessible(username, password)
        for item in items:
            project_list.append(
                Project(
                    id=str(item.id)
                    , name=item.name
                    , status=item.status.name
                    , view_state=item.view_state.name
                    , description=item.description
                    , enabled=item.enabled))
        return project_list