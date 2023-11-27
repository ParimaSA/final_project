Menu for each role after log in:
- Admin 
    - check request if any lead ask for canceling their project 
    - exit from the program to get all the csv file


- Student
    - check the request to join the project
        - see the request detail (lead, title)
        - answer the request (accept/deny)
            - accept = become the member of that project => change role to 'member', all others request = deny
    - create their own project => change role to 'lead', create new project, deny all request


- Lead
    - check and change project detail
    - request member (2 members)
        - can request if role is 'student'
    - request advisor (1 advisor)
        - can request if that faculty advise less than 3 project
    - check answer of the requesting (waiting/accept/deny)
    - cancel the project 
        - send request to admin can send only if there is no member
    - send the project to advisor
        - can send if there is 2 members and 1 advisor


- Member
    - check and change the project detail
    - see the answer of the requesting


- Faculty/Advisor
    - Check request to be advisor of the project (can advise at most 3 project/ faculty)
    - Answer request to be the advisor
    - Check detail of the project that being an advisor
    - Send the project to other faculty to get the approval