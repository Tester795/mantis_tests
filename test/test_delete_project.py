# -*- coding: utf-8 -*-
from model.project import Project
import random


def test_delete_some_project(app, db, check_ui, json_projects):
    project = json_projects
    if len(db.get_project_list()) == 0:
        app.group.create(project)
    old_projects = db.get_project_list()
    project = random.choice(old_projects)
    app.project.delete_by_id(project.id)

    new_projects = db.get_project_list()
    old_projects.remove(project)
    assert sorted(new_projects, key=Project.id_or_max) == sorted(old_projects, key=Project.id_or_max)
    if check_ui:
        print("CHECK_UI")
        assert sorted(new_projects, key=Project.id_or_max) == sorted(app.group.get_group_list(), key=Project.id_or_max)
