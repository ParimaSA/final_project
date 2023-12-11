Menu for each role after log in:
- Admin 
    - Edit the database
        - Check database (person.csv)
            - Add data
                - get all the info add to person and login table
                - let status in login to be 'new', to make them know their password when first login
            - Delete data, only if he/she not involve in any project
                - check if he/she not involve
                - change all request to be 'deny', just requesting
                - delete row from person and login
            - Change data
                - ask for which id and which detail
                - change detail in both file
    - Check request 
      - Sign up Account
        - check in pending_sign (status = waiting)
        - Accept
          - add data to person and login
        - Deny
          - delete row for login 
      - Cancel Project
          - check in pending_cancel (status = waiting)
          - clear lead.project = None
          - change project status to be 'Cancel'
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

## Additional:

#### - Login

  - if username and password match -> processing menu
  - if username not in the database -> ask if want to sign up
  - if username in the database -> ask if forget password
    - special case: (can not change the password) 
        - if a new account (password = id) -> waiting room
          - sign up and waiting for approve 
          - get approve for sign up
          - admin create new account 

#### - Project  
  - Status: Processing, Sending, Approve
    - processing = get when create the project
    - sending = get when send the project to 3 random committee
    - approve = get when 3 committee approve the project

#### - Database
  - Dict
    - **persons** = ['ID', 'first', 'last', 'type']
    - **login** = ['ID', 'username', 'password', 'role']
    - **pending_member**  = ['ProjectID', 'to_be_member', 'status']
    - **pending_advisor** = ['ProjectID', 'to_be_advisor', 'status']
    - **sign_up** = ['ID', 'first', 'last', 'row', 'status']
    - **send_proposal** = ['ProjectID', 'advisor', 'status']
    - **send_ project** = ['ProjectID', 'committee', 'status']
    + DETAIL
      - to_be_member, to_be_advisor, advisor, committee = user_id (str)
      - status:
            - pending = waiting, Accept, Deny
            - sign_up, send = waiting, Approve, Deny
  - Object
    - **project** = ['ProjectID', 'Title', 'Keyword', 'Lead', 'Member1', 'Member2', 'Advisor', 'Status', 'num_member_requesting', 'num_member', 'num_advisor', 'num_submit', 'num_approve']
    - **admin** = [id, name, num_request]
    - **student** = [id, name, project, num_answer] 
    - **advisor** = ['id', 'name', 'num_project', 'num_request', 'num_submit', 'num_approve']
    + DETAIL
      - Lead, Member1, Member2, Advisor = user_id (str)
      - Number
        - num_request, num_answer = number of request/answer when asking for involve in the project
        - num_project = number of project that advisor advise (max=3)
        - num_member = number to check request member process
          - num_member_requesting => check how many member that can request (max=2) add when requested, sub when deny
          - num_member => check number of member in the group use when check for send advisor request
        - num_advisor = number of the advisor => use to check if can request advisor or not (max=1)
        - num_submit = number to check sending proposal process 
          - project => check status of the proposal (0=can send, 1=wait approve, 2=already approve, 3=new approve, -1 = deny)
          - advisor => check if there is any proposal to answer
        - num_approve = number to check sending project process
          - project => num==3 change project status to Approve
          - advisor => check if there is any project to answer