# **Final Project**

Class:
- create a class call Student (have method for all role of the student, student/member/lead)
- create a class call Faculty (have method for faculty/advisor)

Table in the database:
- persons (from csv file)
- login (from csv file)
- member_pending_request
- advisor_pending_request
- all_project
- student (have a student data in Student class to use the method)
- faculty (have a faculty data in Advisor class to use the method)

if login successful, find that person in object version of Student/Faculty class, then use the method in that class

TO evaluate the project:
- can send the project after the advisor approve the proposal
- send the project to 3 random faculty/advisor that is not the advisor of this project
  - if all of the committee approve the project -> project is Approve
  - if one of the committee deny the project -> project is Deny
