# it-company-task-manager
Description:

I have a team of Developers, Designers, Project Managers & QA specialists. Also i have a lot of tasks connected with IT-sphere. So, i implemented my own Task Manager, which will handle all possible problems during product development in my team. Everyone from the team can create Task, assign this Task to team-members, and mark the Task as done (of course, better before the deadlines)

  


  ![Database structure](/static/assets/img/It_Company_Task_Manager_a8510d162c.png)

  ## Installation

Python3 must be already installed

```shell
git clone https://github.com/Paul-Starodub/it-company-task-manager
cd it-company-task-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver # starts Django Server
```

## Features

- Authentication for Worker/User
- Managing workers, positions, task types and tasks directly from the website interface
- Powerful admin panel for advanced managing 

## Demo

Use the following command to load prepared data from fixture to get demo access to the system:

  `python manage.py loaddata it_company_task_manager_db_data.json`.

After loading data from fixture you can use following superuser (or create another one by yourself):
  - Login: `admin`
  - Password: `vovk0763`

After cloning, you need to create your `.env` file and register your variables in it. After that, everything will work. For an example, see the file `.env.sample`

![Website interface](/static/assets/img/demo.png)
