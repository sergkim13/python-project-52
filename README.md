# Task manager

[![Actions Status](https://github.com/sergkim13/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/sergkim13/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/fce77e785df35408d49f/maintainability)](https://codeclimate.com/github/sergkim13/python-project-52/maintainability)
[![Linters check](https://github.com/sergkim13/python-project-52/actions/workflows/linters_check.yml/badge.svg)](https://github.com/sergkim13/python-project-52/actions/workflows/linters_check.yml)
[![Tests check](https://github.com/sergkim13/python-project-52/actions/workflows/tests_check.yml/badge.svg)](https://github.com/sergkim13/python-project-52/actions/workflows/tests_check.yml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/fce77e785df35408d49f/test_coverage)](https://codeclimate.com/github/sergkim13/python-project-52/test_coverage)

### Description:
A task management web application built with Python, Django, Bootstrap and PostgreSQL. It allows you to set tasks, assign performers and change their statuses. Registration and authentication are required to work with the system.

✅ Deployed on Railway:https://python-project-52-production-6a60.up.railway.app/

✅ Deployd on Render: https://task-manager-tyin.onrender.com/

### Usage:
| Steps        | Description                                                                                                                                                               |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Registration | First you need to register in the app using the provided form of registration.                                                                                            |
| Log in       | Then you have to log in using the information you've filled in the registration form.                                                                                     |
| User         | You can see all users on the relevant page. You can change the information only about yourself. If the user is an author or an executor of the task he cannot be deleted. |
| Statuses     | You can add, update, delete statuses of the tasks, if you are logged in. The statuses which correspond with any tasks cannot be deleted.                                  |
| Labels       | You can add, update, delete labels of the tasks, if you are logged in. The label which correspond with any tasks cannot be deleted.                                       |
| Tasks        | You can add, update, delete tasks, if you are logged in. You can also filter tasks on the relevant page with given statuses, exetutors and labels.
___
### Requirements:
1. MacOS (prefer) / Linux / Windows10
2. `Docker`
3. `Make` utily for MacOS, Linux.

### Install:
1. Clone repository: https://github.com/sergkim13/python-project-52
2. Create `.env` and fill it up according to `.env.example`.
3. Type `make install` (`Poetry`) or `pip install -r requirements.txt`  to install dependencies to your virtual environment.
4. Type `make compose` for running application in docker container. Type `make stop` to stop app container.
5. Type `make compose-test` for running tests in docker container. Type `make stop-test` to stop test container.
