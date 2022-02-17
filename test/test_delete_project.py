# -*- coding: utf-8 -*-
from model.project import Project
import random


def test_delete_some_project(app_admin, db, check_ui, json_projects):
    current_username = app_admin.config['webadmin']['username']
    current_password = app_admin.config['webadmin']['password']
    project = json_projects
    if len(db.get_project_list()) == 0:
        app_admin.project.create(project)
    old_projects = app_admin.soap.get_project_list(current_username, current_password)
    project = random.choice(old_projects)
    app_admin.project.delete_by_id(project.id)

    new_projects = app_admin.soap.get_project_list(current_username, current_password)
    old_projects.remove(project)
    assert sorted(new_projects, key=Project.id_or_max) == sorted(old_projects, key=Project.id_or_max)
    if check_ui:
        print("CHECK_UI")
        assert sorted(new_projects, key=Project.id_or_max) == sorted(app_admin.group.get_group_list(), key=Project.id_or_max)
