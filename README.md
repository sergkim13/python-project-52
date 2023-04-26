# Task manager

[![Actions Status](https://github.com/sergkim13/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/sergkim13/python-project-52/actions)


### Description:
A task management web application built with Python, Django, Bootstrap and PostgreSQL. It allows you to set tasks, assign performers and change their statuses. Registration and authentication are required to work with the system.
Deployed on Railway:https://python-project-52-production-6a60.up.railway.app/

### Usage:
| Steps        | Description                                                                                                                                                               |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Registration | First you need to register in the app using the provided form of registration.                                                                                            |
| Log in       | Then you have to log in using the information you've filled in the registration form.                                                                                     |
| User         | You can see all users on the relevant page. You can change the information only about yourself. If the user is an author or an executor of the task he cannot be deleted. |
| Statuses     | You can add, update, delete statuses of the tasks, if you are logged in. The statuses which correspond with any tasks cannot be deleted.                                  |
| Labels       | You can add, update, delete labels of the tasks, if you are logged in. The label which correspond with any tasks cannot be deleted.                                       |
| Tasks        | You can add, update, delete tasks, if you are logged in. You can also filter tasks on the relevant page with given statuses, exetutors and labels.
