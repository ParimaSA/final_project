## Overall Process:
    - student create project => lead
    - lead request 2 member
    - those request student accept => member
    - lead request 1 advisor
    - that request faculty accept => advisor
    project have 2 members and 1 faculty
    - lead send the proposal(project detail) to advisor
    - advisor approve the proposal
    - lead send the project to the committee
    - all committee approve project
    - project Approve

## Role Menu:
- ### Admin 
    - #### edit database (see database persons.csv)
      - Add data
        - get all the info add to person and login table
        - change login role='new', to make them know their password when first login
      - Delete data: can delete only if he/she not involve in any project
        - check if he/she not involve, must be a student or faculty but can have some request
        - update pending_member/pending_advisor status='Deny'
        - inform lead and update number that can request
          - project num_member_requesting/num_advisor-1, 
          - lead num_answer+1
        - delete data row from person and login
      - Change data
        - ask for which id and which detail
        - change detail in all file that have those detail
          - id = all database
          - name = login(username) + persons
    - #### Check request 
      - Sign up Account
        - check in pending_sign (status='waiting')
        - delete this sign up and log in from the database
        - Accept
          - add new data to login and persons database
          - change password to 4 random digits
          - change login role='new' to inform new password to user
      - Cancel Project
          - check in pending_cancel (status='waiting')
          - clear lead. project = None
          - delete project from project database
          - delete request role from cancel database
    - #### Exit: exit from the program to get all the csv file


- ### Student
    - ##### check the request to join the project
        - see the request detail: search in pending_member that still waiting and id=self.id
        - answer the request: input ProjectID that want to answer
            - Accept = become the member of that project 
              - change role in login to 'member'
              - change project detail Member1/Member2
              - add self. project
              - update pending member of accept project and send notification to that lead
                - pending status='Accept', lead num_answer+1
              - update pending_member of other project and send notification to all other lead that request
                - pending status='Deny', project num_member_requesting-1, lead num_answer+1 
            - Deny = deny only that project
              - update pending_member of that project and send notification to lead that request
                - pending status='Deny', project num_member_requesting-1, lead num_answer+1
    - ##### create project
        - change role in login to 'lead'
        - update pending_member of all project and send notification to all other lead that request
          - pending status='Deny', num_member_requesting-1, lead num_answer+1 
        - ask for needed information
        - create new project
        - add project to project table and self. project


- ### Lead
    - ##### check and change project detail
      - can change only if status='Processing'
        - ask for key and value to change => change project table
    - ##### request member (2 members)
        - can request if role is 'student'
        - add data to pending_member
        - send notification to that student. num_answer+1
    - ##### request advisor (1 advisor)
        - can request if that faculty advise less than 3 project
        - add data to pending_advisor
        - send notification to that faculty/advisor. num_request+1
    - ##### check answer of the requesting (waiting/accept/deny)
      - print all the request in pending_member and pending_advisor that has the same ProjectID
    - ##### send proposal to advisor
        - can send if there is 2 members and 1 advisor => check num_member and advisor
        - add data to send_proposal
        - num_submit = 0 : can send the proposal
        - num_submit = 1 : already send the proposal
        - num_submit = 2 : proposal is approved 
        - num_submit = 3 : proposal is approved (notification) => after see the result change back to 2
        - num_submit = -1 : proposal is denied, send again (notification) => after see the result change to 0
    - ##### send project
        - can send if in processing and already send the proposal
        - change status to 'Sending'
        - add data in send_project
    - ##### cancel the project 
        - send request to admin can send only if there is no member
        - add data to cancel_project
        - change status to 'request_cancel'
        - update all in request in pending_member to 'Deny' and subtract all the notification to that student 

- ### Member
    - #### check and change the project detail
      - can change only if status='Processing'
      - ask for key and value to change => change project table
    - #### see the answer of the requesting
      - print all the request in pending_member and pending_advisor that has the same ProjectID


- ### Faculty
    - #### approve sending project
      - print all in send_project that has same id and status='waiting'
      - Approve
        - update send_project status = 'Approve'
        - update project detail .num_approve +=1 if num_approve==3 change status to 'Approve'
      - Deny
        - update send_project status = 'Deny', also other committee that not answer
        - subtract the notification to other committee
        - change project status = 'Deny' => notify project status => change back to 'Processing' after inform
        - change project detail num_approve = 0
    - #### check request to be advisor of the project (can advise at most 3projects/ 1faculty)
      - print all request in pending_advisor that still waiting and id==self. id
    - #### answer request to be the advisor
      - Accept
        - change login role to 'advisor'
        - add project table .Advisor
        - change pending_advisor status = 'Accept'
        - send notification to lead num_answer+1
        - if this is the last project that can advise
          - update pending_advisor of that project and send notification to lead that request
            - pending status='Deny', num_advisor-1, lead num_answer+1 
      - Deny
        - update pending_advisor of that project and send notification to lead that request
            - pending status='Deny', num_advisor-1, lead num_answer+1 


- ### Advisor
    - #### approve sending project
      - print all in send_project that has same id and status='waiting'
      - Approve
        - update send_project status = 'Approve'
        - update project detail .num_approve +=1 if num_approve==3 change status to 'Approve'
      - Deny
        - update send_project status = 'Deny', also other committee that not answer
        - subtract the notification to other committee
        - change project status = 'Deny' => notify project status => change back to 'Processing' after inform
        - change project detail num_approve = 0
    - #### check request to be advisor of the project (can advise at most 3projects/ 1faculty)
      - print all request in pending_advisor that still waiting and id==self. id
    - #### answer request to be the advisor
      - Accept
        - change login role to 'advisor'
        - add project table .Advisor
        - change pending_advisor status = 'Accept'
        - send notification to lead num_answer+1
        - if this is the last project that can advise
          - update pending_advisor of that project and send notification to lead that request
            - pending status='Deny', num_advisor-1, lead num_answer+1 
      - Deny
        - update pending_advisor of that project and send notification to lead that request
            - pending status='Deny', num_advisor-1, lead num_answer+1 
    - #### check detail of the project that being an advisor
      - search in project table that .Advisor has same id
    - #### approve proposal
      - Approve
        - change send_proposal status = 'Approve'
        - change project num_submit = 3 to send notification and inform about the approval
      - Deny
        - change send_proposal status = 'Deny'
        - change project num_submit = -1 to send notification and inform about deny

### Change Role:
    + STUDENT  =>  accept request  =>  MEMBER
    + FACULTY  =>  accept request  =>  ADVISOR
    + STUDENT  =>  create project  =>   LEAD
    +   LEAD   =>  cancel project  =>  STUDENT
        

## Additional:

#### - How to get object from database 
    get id/ProjectID -> send to search function -> return object of that class
  - create function for searching object of each class
    - search_student : same id in student database
    - search_faculty : same id in faculty database
    - search_project : same ProjectID in project database

#### - Send notification to lead
  - search project object => search lead from project attribute

#### - Login

  - if username and password match -> processing menu
  - if username not in the database -> ask if want to sign up
  - if username in the database -> ask if forget password
    - special case: (can not change the password) 
        - if a new account (password = id) -> waiting room
          - sign up and waiting for approve 
          - get approve for sign up
          - admin create new account 
  
#### - Sign up
  - ask for all the needed info, id must be different
  - add data in sign_up table for admin to approve
  - add login in login table status=waiting (username=first.last, password=user_id) to inform about approve process
  - during waiting : login status = 'waiting'
    - if password = id: waiting_room => inform that admin still not answer request
    - if password = new password => user still use the id to password (password=id, status='new') 
    => inform new password and change status to the actual role (actual role set in persons)

#### - Forget password
  - ask for some info to check the security
  - random new password 4 digits that not in the database
  - change password in login and inform in password

#### - Project  
  - Status: Processing, Sending, Approve, Deny
    - Processing = get when create the project
    - Sending = get when send the project to 3 random committee
    - Approve = get when 3 committee approve the project
    - Deny = get when one of the committee deny

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
          - num_member_requesting => check how many member that can request (max=2) 
            - add when requested, sub when deny
          - num_member => check number of member in the group use when check for send advisor request
        - num_advisor = number of the advisor => use to check if can request advisor or not (max=1)
        - num_submit = number to check sending proposal process 
          - project => check status of the proposal (0=can send, 1=waiting, 2=already approve, 3=new approve, -1 = deny)
          - advisor => check if there is any proposal to answer
        - num_approve = number to check sending project process
          - project => num==3 change project status to Approve
          - advisor => check if there is any project to answer