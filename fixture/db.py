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
                status_str = Project.statuses[int(status)]
                view_state_str = Project.view_states[int(view_state)]
                project_list.append(Project(id=str(id), name=name, status=status_str
                                            , view_state=view_state_str
                                            , description=description, inherit_global=bool(inherit_global)
                                            , enabled=bool(enabled)))

        finally:
            cursor.close()
        return project_list

    def delete_all_projects(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("delete from mantis_project_table")
        finally:
            cursor.close()

    def destroy(self):
        self.connection.close()
