from suds.client import Client
from suds import WebFault

from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app
        self.api_url = self.app.base_url + "/api/soap/mantisconnect.php?wsdl"

    def urljoin(*args):
        trailing_slash = '/' if args[-1].endswith('/') else ''
        return "/".join(map(lambda x: str(x).strip('/'), args)) + trailing_slash

    def can_login(self):
        client = Client(self.api_url)
        try:
            client.service.mc_login(self.app.config['webadmin']['username'], self.app.config['webadmin']['password'])
            return True
        except WebFault:
            return False

    def get_project_list(self):
        client = Client(self.api_url)
        project_list = []
        items = client.service.mc_projects_get_user_accessible(self.app.config['webadmin']['username'],
                                                               self.app.config['webadmin']['password'])
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