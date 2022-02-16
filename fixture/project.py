import re
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from model.project import Project


class ProjectHelper:
    def __init__(self, app):
        self.app = app

    project_cache = None

    def open_projects_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php") and
                len(wd.find_elements(By.XPATH, "//input[@value='Create New Project']")) > 0):
            wd.find_element(By.LINK_TEXT, "Manage").click()
            wd.find_element(By.LINK_TEXT, "Manage Projects").click()

    def create(self, project):
        wd = self.app.wd
        # ini group creation
        self.open_projects_page()
        wd.find_element(By.XPATH, "//input[@value='Create New Project']").click()
        # fill group form
        self.fill_project_form(project)
        # submit group creation
        wd.find_element(By.XPATH, "//input[@value='Add Project']").click()

        WebDriverWait(wd, 10).until(
            lambda method:
            (len(wd.find_elements(By.XPATH, "//input[@value='Create New Project']")) > 0)
        )

        self.project_cache = None

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)
        self.change_field_value("status", project.status)
        self.change_field_value("inherit_global", project.inherit_global)
        # checkbox = wd.find_element(By.NAME, "inherit_global")
        # if checkbox.get_attribute("checked") is not None: # if Checked
        #     if project.inherit_global is True:
        #         pass
        #     else:
        #         checkbox.click() #  to Uncheck it
        # else: # if not Checked
        #     if project.inherit_global is True:
        #         checkbox.click() #  to Check it
        #     else:
        #         pass

        # checkbox = wd.find_element(By.NAME, "inherit_global")
        # if checkbox.get_attribute("checked") is None and project.inherit_global is True:
        #     checkbox.click()
        # elif checkbox.get_attribute("checked") is not None and project.inherit_global is not True:
        #     checkbox.click()

        # if project.inherit_global is True:
        #     if checkbox.get_attribute("checked") is None: # if not checked yet
        #         checkbox.click() # check
        # else:
        #     if checkbox.get_attribute("checked") is not None: # if already checked
        #         checkbox.click() # uncheck

        self.change_field_value("view_state", project.view_state)
        self.change_field_value("description", project.description)

    def change_field_value(self, field_name, value):
        wd = self.app.wd
        if value is not None:
            wd.find_element(By.NAME, field_name).clear()
            wd.find_element(By.NAME, field_name).send_keys(value)

    # def return_to_groups_page(self):
    #     wd = self.app.wd
    #     wd.find_element(By.LINK_TEXT, "group page").click()

    # def select_by_index(self, index):
    #     wd = self.app.wd
    #     wd.find_elements(By.NAME, "selected[]")[index].click()

    def select_by_id(self, project_id):
        wd = self.app.wd
        wd.find_element(By.CSS_SELECTOR, "a[href='manage_proj_edit_page.php?project_id=%s']" % project_id).click()

    # def select_first_group(self):
    #     wd = self.app.wd
    #     wd.find_element(By.NAME, "selected[]").click()
    #
    # def delete_first(self):
    #     self.delete_by_index(0)

    # def delete(self, group_name):
    #     wd = self.app.wd
    #     self.open_projects_page()
    #     # select group with specific name
    #     if group_name != "":
    #         xpath = "//*[@id='content']//span[@class='group' and text()='%s']/input" % group_name
    #     else:
    #         xpath = "//*[@id='content']//span[@class='group' and not(text())]/input"
    #
    #     wd.find_element(By.XPATH, xpath).click()
    #     # submit deletion
    #     wd.find_element(By.NAME, "delete").click()
    #     self.return_to_groups_page()
    #     self.project_cache = None

    # def delete_by_index(self, index):
    #     wd = self.app.wd
    #     self.open_projects_page()
    #     # select first group
    #     # submit deletion
    #     self.select_by_index(index)
    #     wd.find_element(By.NAME, "delete").click()
    #     self.return_to_groups_page()
    #     self.project_cache = None

    def delete_by_id(self, project_id):
        wd = self.app.wd
        self.open_projects_page()
        self.select_by_id(project_id)
        project_name = wd.find_element(By.CSS_SELECTOR, "a[href='manage_proj_edit_page.php?project_id=%s']" % project_id).text
        wd.find_element(By.XPATH, "//input[@value='Delete Project']").click()
        assert wd.find_element(By.XPATH, "/html/body/div[2]").text \
               == "Are you sure you want to delete this project and all attached issue reports?\nProject Name: %s" % project_name
        #
        wd.find_element(By.XPATH, "//input[@value='Delete Project']").click()
        WebDriverWait(wd, 10).until(
            lambda method:
            (len(wd.find_elements(By.XPATH, "//input[@value='Create New Project']")) > 0)
        )

        self.project_cache = None

    # def modify(self, group_name, new_group):
    #     wd = self.app.wd
    #     self.open_projects_page()
    #     # select group with specific name
    #     if group_name != "":
    #         xpath = "//*[@id='content']//span[@class='group' and text()='%s']/input" % group_name
    #     else:
    #         xpath = "//*[@id='content']//span[@class='group' and not(text())]/input"
    #
    #     wd.find_element(By.XPATH, xpath).click()
    #     # init modify
    #     wd.find_element(By.NAME, "edit").click()
    #
    #     # fill group form with new values
    #     self.fill_group_form(new_group)
    #
    #     # submit modify
    #     wd.find_element(By.NAME, "update").click()
    #
    #     self.return_to_groups_page()
    #     self.project_cache = None

    # def modify_first_group(self, new_group_data):
    #     self.modify_by_index(0, new_group_data)
    #
    # def modify_by_index(self, index, new_group_data):
    #     wd = self.app.wd
    #     self.open_projects_page()
    #     self.select_by_index(index)
    #     # open modification form
    #     wd.find_element(By.NAME, "edit").click()
    #     # fill group
    #     self.fill_group_form(new_group_data)
    #     # submit modification
    #     wd.find_element(By.NAME, "update").click()
    #     self.return_to_groups_page()
    #     self.project_cache = None

    # def modify_by_id(self, group_id, group):
    #     wd = self.app.wd
    #     self.open_projects_page()
    #     self.select_by_id(group_id)
    #     wd.find_element(By.NAME, "edit").click()
    #     self.fill_group_form(group)
    #     wd.find_element_by_name("update").click()
    #     self.return_to_groups_page()
    #     self.project_cache = None

    def count(self):
        wd = self.app.wd
        self.open_projects_page()
        return len(wd.find_elements(By.CSS_SELECTOR, "body > table:nth-child(26) > tbody > tr")[2:])

    # def exist(self, group_name):
    #     wd = self.app.wd
    #     self.open_projects_page()
    #     if group_name != "":
    #         xpath = "//*[@id='content']//span[@class='group' and text()='%s']/input" % group_name
    #     else:
    #         xpath = "//*[@id='content']//span[@class='group' and not(text())]/input"
    #     return len(wd.find_elements(By.XPATH, xpath)) > 0

    def get_project_list(self):

        if self.project_cache is None:
            wd = self.app.wd
            self.open_projects_page()
            self.project_cache = []
            rows = wd.find_elements(By.CSS_SELECTOR, "body > table:nth-child(26) > tbody > tr")[2:]
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                project_link = cells[0].find_element(By.TAG_NAME, "a")
                id = project_link.get_attribute('href').replace("manage_proj_edit_page.php?project_id=", "")
                name = project_link.text
                status = cells[1].text
                enabled = True if cells[2].text == "X" else False
                view_state = cells[3].text
                description = cells[4].text
                self.project_cache.append(
                    Project(
                        id=id
                        , name=name
                        , status=status
                        , enabled=enabled
                        , view_state=view_state
                        , description=description
                    )
                )
        return list(self.project_cache)
