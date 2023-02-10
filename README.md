# it-company-task-manager
I have a team of Developers, Designers, Project Managers & QA specialists. Also i have a lot of tasks connected with IT-sphere. But somehow i still haven't heard anything about Trello or ClickUp. So, i implemented my own Task Manager, which will handle all possible problems during product development in my team. Everyone from the team can create Task, assign this Task to team-members, and mark the Task as done (of course, better before the deadlines)

  Important!!! The database structure can be viewed here: "/static/assets/img/It_Company_Task_Manager_a8510d162c.png"



1.Read this guideline before start.
 
- Prepare the project
  - Fork the repo (GitHub repository)
  - Clone the forked repo
    - git clone the-link-from-your-forked-repo (you can get the link by clicking the Clone or download button in your repo)
  - Open the project folder in your IDE
  - Open a terminal in the project folder. If you are using PyCharm - it may propose you to automatically create venv for your project and install requirements in it, but if not:
    - python -m venv venv
    - venv\Scripts\activate (on Windows)
    - source venv/bin/activate (on macOS)
    - pip install -r requirements.txt
      
2.Use the following command to load prepared data from fixture to test and debug your code:

  ```python manage.py loaddata it_company_task_manager_db_data.json```

3.After loading data from fixture you can use following superuser (or create another one by yourself):
  - Login: `admin`
  - Password: `vovk0763`
