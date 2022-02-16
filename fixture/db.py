import pymysql.cursors
from model.project import Project


class DbFixture:
    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = pymysql.connect(
            host="127.0.0.1"
            , database="bugtracker"
            , user="root"
            , password=""
            , autocommit=True)

    def get_project_list(self):
        project_list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select id, name, status, view_state, description, inherit_global, enabled from mantis_project_table")
            for row in cursor:
                (id, name, status, view_state, description, inherit_global, enabled) = row
                project_list.append(Project(id=str(id), name=name, status=Project.Status.convert_int_to_status(status)
                                            , view_state=Project.ViewState.convert_int_to_view_state(view_state)
                                            , description=description, inherit_global=bool(inherit_global)
                                            , enabled=bool(enabled)))

        finally:
            cursor.close()
        return project_list

    def destroy(self):
        self.connection.close()
