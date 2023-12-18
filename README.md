# Final project for 2023's 219114/115 Programming I
* Starting files for part 1
  - database.py
  - project_manage.py
  - persons.csv

<br/>

### A list of files

| File                | Method           |  Class   | Description                                   |
|---------------------|------------------|:--------:|-----------------------------------------------|
| database.py         | read_csv         |    -     | read .csv file to list of dict                |
|                     | update_csv       |    -     | change list of dict to .csv file              |
|                     | insert           | Database | insert table into database                    |
|                     | search           | Database | search for the table in database              |
|                     | join             |  Table   | join two table                                |
|                     | filter           |  Table   | filter table with given condition             |
|                     | update           |  Table   | update given key in table with given value    |
| project_manage.py   | initializing     |    -     | read the data from .csv file                  |
|                     | log_in           |    -     | check username and password                   |
|                     | send_sign_up     |    -     | send sign up request to admin                 |
|                     | change_password  |    -     | change password                               |
|                     | waiting_room     |    -     | room for waiting sign up process              |
|                     | get_option       |    -     | get the option that only in the given list    |
|                     | get_info         |    -     | get info that needed to create new account    |
|                     | (Project method) | Project  | method to change/check project detail         |
|                     | (Admin method)   |  Admin   | method for admin                              |
|                     | (Student method) | Student  | method for student, member, lead              |
|                     | (Faculty method) | Faculty  | method for faculty, advisor                   |
|                     | update_lead      |    -     | update lead notification and number request   |
|                     | search_project   |    -     | search for Project object in project database |
|                     | search_student   |    -     | search for Student object in student database |
|                     | search_faculty   |    -     | search for Faculty object in faculty database |
|                     | processing       |    -     | get id and role to process which menu to go   |
|                     | update_and_exit  |    -     | update all .csv file and exit the program     |
| persons.csv         | -                |    -     | collect person data                           |
| login.csv           | -                |    -     | collect data that use for login               |
| Admin.csv           | -                |    -     | collect data for admin process                |
| Student.csv         | -                |    -     | collect data for student/member/lead process  |
| Faculty.csv         | -                |    -     | collect data for faculty/advisor process      |
| Project.csv         | -                |    -     | collect data of all project                   |
| Pending_member.csv  | -                |    -     | collect data for pending member process       |
| Pending_advisor.csv | -                |    -     | collect data for pending advisor process      |
| send_proposal.csv   | -                |    -     | collect data for sending proposal process     |
| send_project.csv    | -                |    -     | collect data for sending project process      |
| sign_up.csv         | -                |    -     | collect data for request and approve sign up  |

<br/>

### How to compile
    - open project_manage.py
    - run the program (1 person/time)
    - enter username and password in login.csv file
    - choose the option to perform that task
    - log out from the program

##### Step to Approve the project
1. Student create project and become Lead
2. Lead request two more Member
3. all Member accept the request
4. Lead request an advisor
5. Advisor accept request
6. Lead send the proposal(project detail) to Advisor
7. Advisor approve the proposal
8. Lead send the project to three random committee (faculty/advisor that not involve in this project)
9. all of the committees approve the project
10. project is approved

##### Change Role:
  - STUDENT  =>  accept request  =>  MEMBER
  - FACULTY  =>  accept request  =>  ADVISOR
  - STUDENT  =>  create project  =>   LEAD
  -   LEAD   =>  cancel project  =>  STUDENT

##### Change password/ Sign up
- if the username not in login.csv file
  - the program will ask if you want to sign up
  - enter needed information and waiting for the admin to approve
  - during the process you can log in with username and password(id) to waiting room, checking if it is approved or not
  - if admin approve, you will log in and see new password
- if the username in login.csv file
  - the program will ask if you forget the password
  - enter needed information to check 
  - get new password after enter correct information

##### Reset the program
- login as an admin
- choose option 3 to reset


<br/>

### Table detailing each role and its actions

|  Role   | Action                                       | Method                 |  Class  | Completion<br/>Percentage |
|:-------:|----------------------------------------------|------------------------|:-------:|--------------------------:|
|  Admin  | Menu                                         | admin_menu             |  Admin  |                      100% |
|  Admin  | check database (sub-menu)                    | edit_database          |  Admin  |                      100% |
|         | add data = add new account                   | add_database           |  Admin  |                      100% |
|         | delete data = delete account                 | delete_database        |  Admin  |                      100% |
|         | change data = change id/name                 | change_database        |  Admin  |                      100% |
|         | (sub) update all file that involve with data | update_all             |  Admin  |                      100% |
|  Admin  | check request (sub_menu)                     | admin_check_request    |  Admin  |                      100% |
|         | check cancel request                         | check_cancel           |  Admin  |                      100% |
|         | delete project                               | cancel_project         |  Admin  |                      100% |
|         | check sign up request                        | check_sign_up          |  Admin  |                      100% |   
|         | approve/deny sign up request                 | answer_sign_up         |  Admin  |                      100% |
|  Admin  | reset program                                | reset                  |  Admin  |                      100% |
|         |                                              |                        |         |                           |
|         |                                              |                        |         |                           |
| Student | Menu                                         | student_menu           | Student |                      100% |
| Student | check student/faculty that can request       | check_available        | Student |                      100% |
| Student | student check request to join project        | student_check_request  | Student |                      100% |
|         | student accept/deny the request              | student_answer_request | Student |                      100% |
| Member  | Menu                                         | member_menu            | Student |                      100% |
| Member  | check project request status                 | check_request          | Student |                      100% |           
|         | (sub) check request member                   | check_request_member   | Student |                      100% |
|         | (sub) check request advisor                  | check_request_advisor  | Student |                      100% |
| Member  | check project proposal                       | check_project_detail   | Project |                      100% |
|         | change project proposal                      | change_project_detail  | Project |                      100% |
|  Lead   | Menu                                         | lead_menu              | Student |                      100% |
|  Lead   | check project request status                 | check_request          | Student |                      100% |           
|         | (sub) check request member                   | check_request_member   | Student |                      100% |
|         | (sub) check request advisor                  | check_request_advisor  | Student |                      100% |    
|  Lead   | check project proposal                       | check_project_detail   | Project |                      100% |
|         | change project proposal                      | change_project_detail  | Project |                      100% |
|  Lead   | request new member                           | request_new_member     | Student |                      100% |
|  Lead   | request new advisor                          | request_new_advisor    | Student |                      100% |
|  Lead   | send proposal to advisor                     | send_proposal          | Student |                      100% |
|  Lead   | send project to committee                    | send_project           | Student |                      100% |
|  Lead   | send cancel project request to admin         | cancel_project         | Student |                      100% |
|         |                                              |                        |         |                           |
|         |                                              |                        |         |                           |
| Faculty | Menu                                         | faculty_menu           | Faculty |                      100% |
| Faculty | approve project                              | approve_project        | Faculty |                      100% |
| Faculty | check request to be an advisor               | faculty_check_request  | Faculty |                      100% |
|         | answer request                               | faculty_answer_request | Faculty |                      100% | 
| Advisor | Menu                                         | advisor_menu           | Faculty |                      100% |
| Advisor | approve project                              | approve_project        | Faculty |                      100% |
| Advisor | check request to be an advisor               | faculty_check_request  | Faculty |                      100% |
|         | answer request                               | faculty_answer_request | Faculty |                      100% |       
| Advisor | check all the project that be an advisor     | check_project          | Faculty |                      100% |
|         | (sub) check project proposal in all project  | check_project_detail   | Project |                      100% |
| Advisor | approve/deny the proposal                    | check_proposal         | Faculty |                      100% |
|         |                                              |                        |         |                           |
|         |                                              |                        |         |                           |

<br/>

### Outstanding Bug
- I think there is none of the outstanding bug in the program to approve the project.
- There is none of the case that will make program raise error, but there may be some of the mistake that I did not find out.

### Missing Feature
- I think it should have more feature for advisor or committee to comment the project, make the member and lead know what to fix
- More detail for the project ex. report 