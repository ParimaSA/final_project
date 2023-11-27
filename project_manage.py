# import database module
from database import read_csv, Database, Table
from random import randint

# define a funcion called initializing

my_DB = Database()


def initializing():
    persons = read_csv('persons.csv')
    logins = read_csv('login.csv')
    persons_table = Table('persons', persons)
    login_table = Table('login', logins)
    student_table = Table('student', [Student(person['ID'], person['username']) for person in login_table.table if person['role'] == 'student'])
    advisor_table = Table('faculty', [Faculty(person['ID'], person['username']) for person in login_table.table if person['role'] == 'faculty'])
    request_member_table = Table('pending_member', [])
    request_advisor_table = Table('pending_advisor', [])
    all_project = Table('project', [])
    my_DB.insert(persons_table)
    my_DB.insert(login_table)
    my_DB.insert(student_table)
    my_DB.insert(advisor_table)
    my_DB.insert(request_member_table)
    my_DB.insert(request_advisor_table)
    my_DB.insert(all_project)


# here are things to do in this function:
# create an object to read all csv files that will serve as a persistent state for this program
# create all the corresponding tables for those csv files
# see the guide how many tables are needed
# add all these tables to the database

# define a function called login

def login():
    print()
    print('Login')
    username = input('Enter Username: ')
    password = input('Enter Password: ')
    my_login = my_DB.search('login')
    this_data = my_login.filter(lambda x: x['username'] == username and x['password'] == password)
    this_data = this_data.table
    if not this_data:
        print('Invalid username or password')
        return None
    return [this_data[0]['ID'], this_data[0]['role']]


# here are things to do in this function:
# add code that performs a login task
# ask a user for a username and password
# returns [ID, role] if valid, otherwise returning None


def get_option(sentence, list_option):
    option = input(sentence)
    while option not in list_option:
        print('Invalid input, try again.')
        option = input(sentence)
    return option


class Project:
    def __init__(self, title, lead):
        self.ProjectID = str(randint(66000, 66999))
        self.Title = title
        self.Keyword = None
        self.Lead = lead
        self.Member1 = None
        self.Member2 = None
        self.Advisor = None
        self.Status = 'Processing'
        self.num_member_requesting = 0
        self.num_member = 0
        self.num_advisor = 0

    def get_table(self):
        return {'ProjectID': self.ProjectID,
                'Title': self.Title,
                'Keyword': self.Keyword,
                'Lead': self.Lead,
                'Member1': self.Member1,
                'Member2': self.Member2,
                'Advisor': self.Advisor,
                'Status': self.Status}

    @staticmethod
    def get_full_name(check_id):
        if check_id is None:
            return None
        persons_table = my_DB.search('persons')
        person = persons_table.filter(lambda x: x['ID'] == check_id)
        person = person.table[0]
        return f'{person["first"]} {person["last"]}'

    def check_project_detail(self):
        print()
        print('Project Detail')
        print(f'\tProjectID: {self.ProjectID}')
        print(f'\tTitle: {self.Title}')
        print(f'\tKeyword: {self.Keyword}')
        print(f'\tMember and Advisor')
        print(f'\t\tLead: {self.get_full_name(self.Lead)}')
        print(f'\t\tMember1: {self.get_full_name(self.Member1)}')
        print(f'\t\tMember2: {self.get_full_name(self.Member2)}')
        print(f'\t\tAdvisor: {self.get_full_name(self.Advisor)}')
        print(f'Status: {self.Status}\n')

    def change_project_detail(self):
        option = get_option('Which detail you want to change title/keyword(t/k)? ', ['t', 'k'])
        if option == 't':
            new_title = input('New title: ')
            check = get_option(f'You want to change your title to {new_title}(y/n)? ', ['y', 'n'])
            if check == 'y':
                self.Title = new_title
                print(f'Your project title has changed to {new_title}')
        else:
            new_keyword = input('New Keyword: ')
            check = get_option(f'You want to change your keyword to {new_keyword}(y/n)? ', ['y', 'n'])
            if check == 'y':
                self.Keyword = new_keyword
                print(f'Your project keyword has changed to {new_keyword}')
        input('Back to project detail(enter): ')
        self.check_project_detail()


class Student:
    def __init__(self, get_id, get_name):
        self.id = get_id
        self.name = get_name
        self.project = None
        self.num_answer = 0

    @staticmethod
    def check_available(role):
        logins = my_DB.search('login')
        logins = logins.filter(lambda x: x['role'] == role)
        for i in logins.table:
            print(f'{i["ID"]}\t\t\t\t{i["username"]}')

    def student_menu(self):
        print()
        print('Student Menu')
        logins = my_DB.search('login')
        pending = my_DB.search('pending_member')
        if self.num_answer == 0:
            print(f'1.Check Request: No request')
        else:
            print(f'1.Check Request: {self.num_answer} request!')
        print('2.Create your project')
        print('0.Log Out')
        option = get_option('Your Option: ', [str(n) for n in range(0, 3)])
        if option == '1':
            self.student_check_request()
        elif option == '2':
            check = get_option('Are you sure to create your project(y/n)? ', ['y', 'n'])
            if check == 'n':
                self.student_menu()
            title = input('Your project title: ')
            pending.update(lambda x: x['to_be_member'] == self.id, 'status', 'Deny')  # deny all project
            logins.update(lambda x: x['ID'] == self.id, 'role', 'lead')  # change role to lead
            self.num_answer = 0
            self.project = Project(title, self.id)
            project_table = my_DB.search('project')
            project_table.table.append(project_table)
            print('Creating your project...')
            input('Go to your project menu(enter): ')
            self.lead_menu()

    def student_answer_request(self):
        pending = my_DB.search('pending_member')
        logins = my_DB.search('login')
        pro_id = input('ProjectID you want to answer: ')
        if pending.filter(lambda row: row['id'] == pro_id and row['to_be_member'] == self.id).table:
            answer = get_option('Accept or Deny this project(a/d)? ', ['a', 'd'])
            all_project = pending.filter(lambda x: x['to_be_member'] == self.id)
            my_project = None
            if answer == 'a':
                pending.update(lambda x: x['to_be_member'] == self.id, 'status', 'Deny')
                for pro in all_project.table:
                    lead = search_student(pro['project'].Lead)
                    lead.num_answer += 1
                    if pro['id'] != pro_id:
                        pro['project'].num_member_requesting -= 1
                    else:
                        my_project = pro['project']
                pending.update(lambda x: x['to_be_member'] == self.id and x['id'] == pro_id, 'status', 'Accept')
                print(f'Successfully Accept, now you are member of project {pro_id}.')
                input('Go to your project menu (enter):')
                self.num_answer = 0
                logins.update(lambda x: x['ID'] == self.id, 'role', 'member')  # change role to lead
                self.num_answer = 0
                # modify project detail
                my_project.num_member += 1
                if my_project.num_member == 1:
                    my_project.Member1 = self.id
                else:
                    my_project.Member2 = self.id
                self.project = my_project
                self.member_menu()
            else:
                pending.update(lambda x: x['to_be_member'] == self.id and x['id'] == pro_id, 'status', 'Deny')
                all_project = all_project.filter(lambda x: x['id'] == pro_id)
                for pro in all_project.table:
                    lead = search_student(pro['project'].Lead)
                    lead.num_answer += 1
                    pro['project'].num_member_requesting -= 1
                print(f'Successfully Deny, project {pro_id}.\n')
                self.num_answer -= 1
        else:
            print('Invalid projectID')
        self.student_check_request()

    def student_check_request(self):
        if self.num_answer == 0:
            print('There is no request from any project')
            input('Back to Menu(enter):')
            self.student_menu()
        pending = my_DB.search('pending_member')
        print()
        print('ProjectID\t\tTitle\t\t\tLeader')
        for row in pending.table:
            if row['to_be_member'] == self.id:
                print(f'{row["id"]}\t\t\t{row["title"]}\t\t\t{row["lead"]}')
        print('\n')
        option = get_option('Do you want to accept or deny any request(y/n)? ', ['y', 'n'])
        if option == 'y':
            self.student_answer_request()
        self.student_menu()

    def lead_menu(self):
        print()
        print('Project Menu')
        if self.num_answer == 0:
            print('1.Check Answer Request')
        else:
            print(f'1.Check Answer Request: new {self.num_answer} answer!')
        print('2.Project Detail')
        print('3.Request new member')
        print('4.Request new advisor')
        print('5.Send project')
        print('6.Cancel project')
        print('0.Log out')
        option = get_option('Your Option: ', [str(n) for n in range(0, 7)])
        if option == '1':
            self.check_request()
        elif option == '2':
            self.project.check_project_detail()
            if self.project.Status == 'Processing':
                option = get_option('Do you want to change any detail(y/n)? ', ['y', 'n'])
                if option == 'y':
                    self.project.change_project_detail()
        elif option == '3':
            self.request_new_member()
        elif option == '4':
            self.request_new_advisor()
        elif option == '0':
            run_login()
        self.lead_menu()

    def check_request(self):
        self.check_request_member()
        print()
        self.check_request_advisor()
        print()
        input('Back to Menu (enter): ')
        self.num_answer = 0

    def request_new_advisor(self):
        pending = my_DB.search('pending_advisor')
        if self.project.num_member < 2:
            print('Not enough member, can not send request to any advisor')
        elif self.project.num_advisor == 1:
            print('Already request advisor.')
        else:
            check = get_option('Check available advisor(y/n)? ', ['y', 'n'])
            if check == 'y':
                print('FacultyID\t\t\tUsername')
                self.check_available('faculty')
            id_request = input('Request Faculty ID: ')
            advisor = search_faculty(id_request)
            if not advisor or advisor.num_project == 3:
                print('Not valid ID or this faculty advise maximum project')
            else:
                print(f'Successfully, send request to {advisor.name} (id:{id_request}).')
                advisor.num_request += 1
                pending.table.append({'project': self.project, 'id': self.project.ProjectID, 'title': self.project.Title,
                                      'lead': self.name, 'to_be_advisor': id_request, 'status': 'waiting'})
                self.project.num_advisor += 1
        input('Back to Menu (enter)')

    def check_request_advisor(self):
        print('Advisor Requesting')
        pending = my_DB.search('pending_advisor')
        all_request = [i for i in pending.table if i['id'] == self.project.ProjectID]
        if not all_request:
            print('There is no requesting.')
        else:
            print('Request Advisor\t\tStatus')
            for i in all_request:
                print(f'{i["to_be_advisor"]}\t\t\t\t{i["status"]}')

    def request_new_member(self):
        pend = my_DB.search('pending_member').table
        if self.project.num_member_requesting == 2:
            print('Max requesting member, can not add more.')
            input('Back to Menu (enter)')
            self.lead_menu()
        print(f'Can request {2 - self.project.num_member_requesting} more member')
        check = get_option('Check available student(y/n)? ', ['y', 'n'])
        if check == 'y':
            print('StudentID\t\t\tUsername')
            self.check_available('student')
        id_request = input('Request Member ID: ')
        fil = my_DB.search('login').filter(lambda x: x['ID'] == id_request and x['role'] == 'student')
        inbox = my_DB.search('pending_member').filter(lambda x: x['to_be_member'] == id_request and
                                                                x['lead'] == self.name and x['status'] == 'waiting')
        # print(fil)
        if not fil.table:
            print('Not valid ID or this student is in some project')
        if inbox.table:
            print('You have already send request to this student.')
        else:
            member = search_student(id_request)
            print(f'Successfully, send request to {member.name} (id:{id_request}).')
            member.num_answer += 1
            pend.append({'project': self.project, 'id': self.project.ProjectID, 'title': self.project.Title,
                         'lead': self.name, 'to_be_member': id_request, 'status': 'waiting'})
            self.project.num_member_requesting += 1
        more = get_option('Do you want to request more member(y/n): ', ['y', 'n'])
        if more == 'y':
            self.request_new_member()
        self.lead_menu()

    def check_request_member(self):
        print()
        print('Member Requesting')
        pending = my_DB.search('pending_member')
        all_request = [i for i in pending.table if i['id'] == self.project.ProjectID]
        if not all_request:
            print('There is no requesting.')
        else:
            print('StudentID\t\tUsername\t\tStatus')
            for i in all_request:
                print(f'{i["to_be_member"]}\t\t\t{search_student(i["to_be_member"]).name}\t\t{i["status"]}')

    def member_menu(self):
        print()
        print('Project Menu')
        print('1.Project Detail')
        print('2.Check Requesting status')
        print('0.Log out')
        option = get_option('Your Option: ', [str(n) for n in range(0, 3)])
        if option == '1':
            self.project.check_project_detail()
            if self.project.Status == 'Processing':
                option = get_option('Do you want to change any detail(y/n)? ', ['y', 'n'])
                if option == 'y':
                    self.project.change_project_detail()
        elif option == '2':
            self.check_request()
        else:
            run_login()
        self.member_menu()


class Faculty:
    def __init__(self, get_id, get_name):
        self.id = get_id
        self.name = get_name
        self.num_project = 0
        self.num_request = 0
        self.all_project = []

    def faculty_menu(self):
        option_num = 1
        print()
        print('Menu')
        print('1.Check Project')
        if self.num_project < 3:
            option_num += 1
            if self.num_request == 0:
                print('2.Check Request')
            else:
                print(f'2.Check Request: {self.num_request} new request!')
        print('0.Log out')
        option = get_option('Your Option: ', [str(n) for n in range(0, option_num+1)])
        if option == '1':
            self.check_project()
        elif option == '2':
            self.faculty_check_request()
            input('Back to menu (enter): ')
        else:
            run_login()
        self.faculty_menu()

    def check_project(self):
        print()
        print('Your Project')
        print('ProjectID\t\tTitle\t\tLeader')
        num = 1
        for row in self.all_project:
            print(f'{num}. {row.ProjectID}\t\t\t{row.Title}\t\t\t{row.Lead}')
        option = get_option('Do you want to check any project detail(y/n)? ', ['y', 'n'])
        if option == 'y':
            pro_num = get_option('Which project you want to check? ', [str(n) for n in range(1, num+1)])
            this_project = self.all_project[int(pro_num)-1]
            this_project.check_project_detail()

    def faculty_check_request(self):
        print()
        print('Project Requesting')
        if self.num_request == 0:
            print('There is no request from any project')
            input('Back to Menu(enter):')
            self.faculty_menu()
        pending = my_DB.search('pending_advisor')
        print('ProjectID\t\tTitle')
        for row in pending.table:
            if row['to_be_advisor'] == self.id:
                print(f'{row["id"]}\t\t\t{row["title"]}')
        print('\n')
        option = get_option('Do you want to accept or deny any request(y/n)? ', ['y', 'n'])
        if option == 'y':
            self.faculty_answer_request()

    def faculty_answer_request(self):
        pending = my_DB.search('pending_advisor')
        logins = my_DB.search('login')
        pro_id = input('ProjectID you want to answer: ')
        if pending.filter(lambda row: row['id'] == pro_id and row['to_be_advisor'] == self.id).table:
            answer = get_option('Accept or Deny this project(a/d)? ', ['a', 'd'])
            all_project = pending.filter(lambda x: x['to_be_advisor'] == self.id)
            if answer == 'a':
                self.num_project += 1
                my_project = None
                if self.num_project == 3:
                    pending.update(lambda x: x['to_be_advisor'] == self.id, 'status', 'Deny')
                for pro in all_project.table:
                    lead = search_student(pro['project'].Lead)
                    lead.num_answer += 1
                    if pro['id'] != pro_id:
                        pro['project'].num_advisor_requesting -= 1
                    else:
                        my_project = pro['project']
                        self.all_project.append(my_project)
                pending.update(lambda x: x['to_be_advisor'] == self.id and x['id'] == pro_id, 'status', 'Accept')
                print(f'Successfully Accept, now you are an advisor of project {pro_id}.')
                if self.num_project == 3:
                    self.num_request = 0
                else:
                    self.num_request -= 1
                logins.update(lambda x: x['ID'] == self.id, 'role', 'Advisor')
                # modify project detail
                my_project.Advisor = self.id
                my_project.num_advisor = 1
                input('Back to menu (enter):')
                self.faculty_menu()
            else:
                pending.update(lambda x: x['to_be_advisor'] == self.id and x['id'] == pro_id, 'status', 'Deny')
                project_table = my_DB.search('project')
                project = project_table.filter(lambda x: x.ProjectID == pro_id).table[0]
                lead = search_student(project.Lead)
                lead.num_answer +=1
                print(f'Successfully Deny, project {pro_id}.\n')
                self.num_request -= 1
        else:
            print('Invalid projectID')
        self.faculty_check_request()



# define a function called exit
def exit():
    pass


# here are things to do in this function: write out all the tables that have been modified to the corresponding csv
# files By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project,
# you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the
# link below for a tutorial on how to do this:

# https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above

def search_student(check_id):
    student_table = my_DB.search('student')
    student = [stu for stu in student_table.table if stu.id == check_id]
    student = student[0]
    return student


def search_faculty(check_id):
    faculty_table = my_DB.search('faculty')
    faculty = [person for person in faculty_table.table if person.id == check_id]
    faculty = faculty[0]
    return faculty


def processing(val):
    # if val[1] == 'admin':
    # see and do admin related activities
    if val[1] == 'student':
        student = search_student(val[0])
        student.student_menu()
        # see and do student related activities
    elif val[1] == 'member':
        member = search_student(val[0])
        member.member_menu()
    elif val[1] == 'lead':
        lead = search_student(val[0])
        lead.lead_menu()
    elif val[1] == 'faculty':
        faculty = search_faculty(val[0])
        faculty.faculty_menu()
    # elif val[1] == 'advisor':
    #     # see and do advisor related activities


def run_login():
    while True:
        val = login()
        if val is not None:
            processing(val)


initializing()
run_login()


# based on the return value for login, activate the code that performs activities according to the role defined for
# that person_id


# once everything is done, make a call to the exit function
# exit()
