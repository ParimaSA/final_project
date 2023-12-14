# **Final Project**
### TO evaluate the project:
- can send the project after the advisor approve the proposal
- send the project to 3 random faculty/advisor that is not the advisor of this project
  - if all of the committee approve the project -> project is Approve
  - if one of the committee deny the project -> project is Deny
    - if project is deny and have to send project again, committee will always be the same group

#### Class:

- create a class call Admin
- create a class call Student (have method for all role of the student, student/member/lead)
- create a class call Faculty (have method for faculty/advisor
- create a class call Project (have all attribute about project detail)

Table in the database:
- persons (from csv file)
- login (from csv file)
- member_pending_request
- advisor_pending_request
- all_project (have a project data in Project class to use the method)
- admin (have an admin data in Admin class to use the method)
- student (have a student data in Student class to use the method)
- faculty (have a faculty data in Advisor class to use the method)
- sign_up
- send_proposal
- send_project
- request_cancel

if login successful, find that person in object version of Admin/Student/Faculty class, then use the method in that class


