from model.project import Project


def test_add_project(app_admin, db, check_ui, json_projects):
    current_username = app_admin.config['webadmin']['username']
    current_password = app_admin.config['webadmin']['password']
    project = json_projects
    old_projects = app_admin.soap.get_project_list(current_username, current_password)
    app_admin.project.create(project)
    new_projects = app_admin.soap.get_project_list(current_username, current_password)
    old_projects.append(project)
    assert sorted(new_projects, key=Project.id_or_max) == sorted(old_projects, key=Project.id_or_max)
    if check_ui:
        print("CHECK_UI")
        assert sorted(new_projects, key=Project.id_or_max) == sorted(app_admin.project.get_project_list(), key=Project.id_or_max)
