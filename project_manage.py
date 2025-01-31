# import database module
import os.path
import random
import sys

from database import read_csv, update_csv, Database, Table
from random import randint


my_DB = Database()

# key of all table in the database
persons_key = ['ID', 'first', 'last', 'type']
login_key = ['ID', 'username', 'password', 'role']
admin_key = ['id', 'name', 'num_request']
student_key = ['id', 'name', 'num_answer']
faculty_key = ['id', 'name', 'num_project', 'num_request', 'num_submit', 'num_approve']
project_key = ['ProjectID', 'Title', 'Keyword', 'Lead', 'Member1', 'Member2', 'Advisor', 'Status', 'Committee1',
               'Committee2', 'Committee3', 'num_member_requesting', 'num_member', 'num_advisor', 'num_submit',
               'num_approve']
pending_member_key = ['ProjectID', 'to_be_member', 'status']
pending_advisor_key = ['ProjectID', 'to_be_advisor', 'status']
sign_up_key = ['ID', 'first', 'last', 'role', 'status']
send_proposal_key = ['ProjectID', 'advisor', 'status']
send_project_key = ['ProjectID', 'committee', 'status']


def initializing():
    persons_table = Table('persons', read_csv('persons.csv'))
    login_table = Table('login', read_csv('login.csv'))
    if os.path.exists('Student.csv'):
        request_member_table = Table('pending_member', read_csv('Pending_member.csv'))
        request_advisor_table = Table('pending_advisor', read_csv('Pending_advisor.csv'))
        request_sign_up = Table('sign_up', read_csv('Sign_up.csv'))
        send_proposal = Table('send_proposal', read_csv('Send_proposal.csv'))
        send_project = Table('send_project', read_csv('Send_project.csv'))

        project = read_csv('Project.csv')  # create object in class Project using data from project.csv file
        project_table = []
        for row in project:
            v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16 = row.values()
            project_table.append(Project(v1, v2, v4, v3, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16))
        project_table = Table('project', project_table)

        student = read_csv('Student.csv')  # create object in class Student using data from Student.csv file
        student_table = []
        for row in student:
            this_pro = project_table.filter(lambda x: row['id'] in [x.Lead, x.Member1, x.Member2])
            if this_pro.table:
                my_pro = this_pro.table[0]  # modify data for .project if this student involve in some project
            else:
                my_pro = None
            student_table.append(Student(row['id'], row['name'], my_pro, row['num_answer']))
        student_table = Table('student', student_table)

        faculty = read_csv('Faculty.csv')  # create object in class Faculty using data from Faculty.csv file
        faculty_table = []
        for row in faculty:
            v1, v2, v3, v4, v5, v6 = row.values()
            faculty_table.append(Faculty(v1, v2, v3, v4, v5, v6))
        faculty_table = Table('faculty', faculty_table)

        admin = read_csv('Admin.csv')
        admin_table = []
        for row in admin:
            v1, v2, v3 = row.values()
            admin_table.append(Admin(v1, v2, v3))
        admin_table = Table('admin', admin_table)
    else:
        admin_table = []
        student_table = []
        faculty_table = []
        for row in login_table.table:
            if row['role'] == 'admin':
                admin_table.append(Admin(row['ID'], row['username']))
            elif row['role'] == 'student':
                student_table.append(Student(row['ID'], row['username']))
            else:
                faculty_table.append(Faculty(row['ID'], row['username']))

        admin_table = Table('admin', admin_table)
        student_table = Table('student', student_table)
        faculty_table = Table('faculty', faculty_table)
        project_table = Table('project', [])
        request_member_table = Table('pending_member', [])
        request_advisor_table = Table('pending_advisor', [])
        request_sign_up = Table('sign_up', [])
        send_proposal = Table('send_proposal', [])
        send_project = Table('send_project', [])

    # insert all the table into the database
    my_DB.insert(persons_table)
    my_DB.insert(login_table)
    my_DB.insert(student_table)
    my_DB.insert(faculty_table)
    my_DB.insert(admin_table)
    my_DB.insert(request_member_table)
    my_DB.insert(request_advisor_table)
    my_DB.insert(request_sign_up)
    my_DB.insert(project_table)
    my_DB.insert(send_proposal)
    my_DB.insert(send_project)


def login():
    print()
    print('Login')
    username = input('Enter Username: ')
    password = input('Enter Password: ')
    logins = my_DB.search('login')
    persons = my_DB.search('persons')
    check1 = logins.filter(lambda x: x['username'] == username and x['password'] == password)
    check2 = logins.filter(lambda x: x['username'] == username and x['ID'] == password and x['role'] == 'new')
    check = check1.table + check2.table  # user match password / new account
    if not check:
        cor_user = logins.filter(lambda x: x['username'] == username)
        incor_pass_new = logins.filter(lambda x: x['username'] == username and x['role'] in ['waiting', 'new'])
        if not cor_user.table:  # username in database
            check = get_option('Sign Up(y/n)? ', ['y', 'n'])
            if check == 'y':
                send_sign_up()
            update_and_exit()
        elif incor_pass_new.table:
            print('Incorrect Password')
        else:  # have username in login table but incorrect password, not a signing up
            check = get_option('Forget Password(y/n)? ', ['y', 'n'])
            if check == 'y':
                change_password()
            update_and_exit()
    else:  # user match password / new account
        check_status = check1.filter(lambda x: x['role'] == 'new')
        this_login = check[0]
        if check_status.table:  # if status = new
            this_role = persons.filter(lambda x: x['ID'] == this_login['ID']).table[0]['type']
            logins.update(lambda x: x['ID'] == this_login['ID'], 'role', this_role)
        return [this_login['ID'], this_login['role']]


def send_sign_up():
    print()
    print('Create New Account')
    print('******************************')
    new_info = get_info()  # get the info that needed
    if new_info is None:
        print('This ID has already taken, can not create new account.')
    else:
        user_id, first, last, role = new_info  # separate value in the list
        sign_table = my_DB.search('sign_up').table
        login_table = my_DB.search('login').table
        admin = my_DB.search('admin').table[0]
        admin.num_request += 1  # send notification to admin
        # append the data in sign_up (for admin approve), login (for check status of sign up)
        sign_table.append({'ID': user_id, 'first': first, 'last': last, 'role': role, 'status': 'waiting'})
        login_table.append({'ID': user_id, 'username': first + '.' + last[0], 'password': user_id, 'role': 'waiting'})
        print()
        print('Successfully, send the request to admin.')  # inform the username and password for now
        print(f'\tYour Username: {first}.{last[0]}')
        print(f'\tYour Password: {user_id}')
        print('We are in the process to get your account.')
        print('Please log in again to get your username and password, after admin approve your request.')
    input('Back to Log in Menu(enter): ')


def change_password():
    print()
    print('Change your password')  # get the info for security
    user_id = input('ID: ')
    first = input('First Name: ').capitalize()
    last = input('Last Name: ').capitalize()

    persons = my_DB.search('persons')
    person_fil = persons.filter(lambda x: x['first'] == first and x['last'] == last and x['ID'] == user_id)
    if not person_fil:  # check if the information is correct or not
        print('Incorrect Information')
        input('Back to Log in Menu(enter): ')
    else:
        logins = my_DB.search('login')
        all_pass = [row['password'] for row in logins.table]  # find all password in the database
        new_password = str(random.randint(1000, 9000))
        while new_password in all_pass:  # random new password until it not in the database
            new_password = str(random.randint(1000, 9000))
        logins.update(lambda x: x['ID'] == user_id, 'password', new_password)  # update new password in login database
        print('Successfully, change your password.')  # inform new password
        print(f'\tYour Username: {first}.{last[0]}')
        print(f'\tYour Password: {new_password}')
        input('Back to Log in Menu(enter): ')


def waiting_room(user_id):  # for people wait for approve sign up or account that just created
    print()
    sign = my_DB.search('sign_up')
    logins = my_DB.search('login')
    persons = my_DB.search('persons')
    check = sign.filter(lambda x: x['ID'] == user_id).table
    account = logins.filter(lambda x: x['ID'] == user_id).table[0]
    if not check:  # check if the request status still waiting or not
        this_role = persons.filter(lambda x: x['ID'] == user_id).table[0]['type']  # actual role in person
        logins.update(lambda x: x['ID'] == user_id, 'role', this_role)  # change role in database to be the real one
        print('Admin has created your account: ')  # inform new password
        print(f'\tYour Username: {account["username"]}')
        print(f'\tYour Password: {account["password"]}')
        input('Go to Log in Menu(enter): ')
    else:
        print('Waiting for admin to approve the request.')  # inform that the request has not been answered
        print('Please log in again later.')
        input('Back to Log in Menu(enter): ')


def get_option(sentence, list_option):  # input loop until get the option that in list_option
    option = input(sentence)
    while option not in list_option:
        print('Invalid Input, try again.')
        option = input(sentence)
    return option


def get_info():  # get the info that needed for create new account
    persons = my_DB.search('persons')
    new_id = input('ID: ')
    while len(new_id) != 7:  # input id must have 7 digits
        print('**ID must have 7 digits**')
        new_id = input('ID: ')
    all_id = [row['ID'] for row in persons.table]  # if this id already in the database, return None
    if new_id in all_id:
        return None
    new_first = input('First: ').capitalize()
    new_last = input('Last: ').capitalize()
    new_type = get_option('Type(student/faculty): ', ['student', 'faculty'])
    return [new_id, new_first, new_last, new_type]


def update_lead(update_table, function, key, num_change):  # update notification to lead that get denied
    if function is not None:
        update_table = update_table.filter(function)
    if update_table.table:
        if key == 'member':  # get deny from request member
            for row in update_table.table:
                project = search_project(row['ProjectID'])
                lead = search_student(project.Lead)
                project.num_member_requesting += num_change  # subtract this request, can request new member
                lead.num_answer += 1  # send notification to lead
        elif key == 'advisor':  # get deny from request advisor
            for row in update_table.table:
                project = search_project(row['ProjectID'])
                lead = search_student(project.Lead)
                project.num_advisor += num_change  # subtract this request, can request new advisor
                lead.num_answer += 1  # send notification to lead


class Project:
    def __init__(self, pro_id, title, lead, key=None, mem1=None, mem2=None, adv=None, status='Processing',
                 com1=None, com2=None, com3=None, n_r=0, n_m=0, n_a=0, n_s=0, n_ap=0):
        self.ProjectID = pro_id
        self.Title = title
        self.Keyword = key
        self.Lead = lead
        self.Member1 = mem1
        self.Member2 = mem2
        self.Advisor = adv
        self.Status = status
        self.Committee1 = com1
        self.Committee2 = com2
        self.Committee3 = com3
        self.num_member_requesting = int(n_r)  # for request new member
        self.num_member = int(n_m)  # for check if project ready for request advisor or not
        self.num_advisor = int(n_a)  # for check if project already request for advisor or not
        self.num_submit = int(n_s)  # for submit proposal process, check and notification
        self.num_approve = int(n_ap)  # for send project process

    def get_table(self):
        return {'ProjectID': self.ProjectID,
                'Title': self.Title,
                'Keyword': self.Keyword,
                'Lead': self.Lead,
                'Member1': self.Member1,
                'Member2': self.Member2,
                'Advisor': self.Advisor,
                'Status': self.Status,
                'Committee1': self.Committee1,
                'Committee2': self.Committee2,
                'Committee3': self.Committee3,
                'num_member_requesting': self.num_member_requesting,
                'num_member': self.num_member,
                'num_advisor': self.num_advisor,
                'num_submit': self.num_submit,
                'num_approve': self.num_approve}

    @staticmethod
    def get_full_name(check_id):  # return full name of person that have id == check_id
        persons_table = my_DB.search('persons')
        person = persons_table.filter(lambda x: x['ID'] == check_id)
        if not person.table:  # if there not have this person
            return None
        person = person.table[0]
        return f'{person["first"]} {person["last"]}'

    def check_project_detail(self):
        print()
        print('Project Detail')
        print(f'\tProjectID: {self.ProjectID}')
        print(f'\tTitle: {self.Title}')
        print(f'\tKeyword: {self.Keyword}')
        print(f'\tMember and Advisor')  # use full name
        print(f'\t\tLead: {self.get_full_name(self.Lead)}')
        print(f'\t\tMember1: {self.get_full_name(self.Member1)}')
        print(f'\t\tMember2: {self.get_full_name(self.Member2)}')
        print(f'\t\tAdvisor: {self.get_full_name(self.Advisor)}')
        print(f'Status: {self.Status}\n')

    def change_project_detail(self):
        option = get_option('Which detail you want to change title/keyword(t/k)? ', ['t', 'k'])
        if option == 't':
            new_title = input('New title: ').capitalize()
            check = get_option(f"You want to change your title to '{new_title}'(y/n)? ", ['y', 'n'])
            if check == 'y':
                self.Title = new_title
                print(f"Your project title has changed to '{new_title}'.")
        else:
            new_keyword = input('New Keyword: ').capitalize()
            check = get_option(f"You want to change your keyword to '{new_keyword}'(y/n)? ", ['y', 'n'])
            if check == 'y':
                self.Keyword = new_keyword
                print(f"Your project keyword has changed to '{new_keyword}'.")


class Admin:
    def __init__(self, user_id, name, num_request=0):
        self.id = user_id
        self.name = name
        self.num_request = int(num_request)  # for notification

    def get_table(self):
        return {'id': self.id, 'name': self.name, 'num_request': self.num_request}

    def admin_menu(self):
        print()
        print('Admin Menu')
        print('******************************')
        print('1.Edit Database')
        if self.num_request == 0:  # inform about the notification
            print('2.Check Request: No request')
        else:
            print(f'2.Check Request: {self.num_request} request!')
        print('3.Reset')
        print('0.Log Out')
        print('******************************')
        option = get_option('Your Option: ', [str(n) for n in range(0, 4)])
        if option == '1':
            self.edit_database()
        elif option == '2':
            self.admin_check_request()
        elif option == '3':
            self.reset()
        elif option == '0':
            update_and_exit()
        self.admin_menu()

    def edit_database(self):
        print()
        persons = my_DB.search('persons')
        logins = my_DB.search('login')
        merge = persons.join(logins, 'ID')  # merge two database persons and logins to get role
        print('                            DATABASE                             ')
        print('*****************************************************************')
        print('ID          First          Last          Type         Role       ')
        print('----------  -------------  ------------  -----------  -----------')
        for row in merge.table:
            if row['role'] == 'new':  # if this account still not log in, use role from persons database
                role = row['type']
            else:  # otherwise just use role
                role = row['role']
            print(f'{row["ID"]:<12}{row["first"]:<15}{row["last"]:<15}{row["type"]:<12}{role}')
        print('----------  -------------  ------------  -----------  -----------')
        print()
        print('Edit Database')
        print('******************************')
        print('1.Add Data')
        print('2.Delete Data')
        print('3.Change Data')
        print('0.Admin Menu')
        print('******************************')
        option = get_option('Your Option: ', [str(n) for n in range(0, 4)])
        if option == '1':
            print()
            print('Create New Account')
            new_info = get_info()
            if new_info is None:  # get_info return None if id already in the database
                print('This ID already in the database.')
            else:
                self.add_database(new_info)
                print('Successfully add this data to the database.')
                input('Back to Edit Database Menu(enter): ')
        elif option == '2':
            self.delete_database()
        elif option == '3':
            self.change_database()
        else:
            self.admin_menu()
        self.edit_database()

    def add_database(self, new_info):
        persons = my_DB.search('persons')
        logins = my_DB.search('login')
        student = my_DB.search('student')
        faculty = my_DB.search('faculty')
        new_id, new_first, new_last, new_type = new_info  # separate all the value in list
        new_username = new_first + '.' + new_last[0]  # get the username from first+last
        all_password = [row['password'] for row in logins.table]  # find all the password in the database
        new_password = str(random.randint(1000, 9999))
        while new_password in all_password:
            new_password = str(random.randint(1000, 9999))  # get new password that not in the database

        person_data = {'ID': new_id, 'first': new_first, 'last': new_last, 'type': new_type}
        login_data = {'ID': new_id, 'username': new_username, 'password': new_password, 'role': new_type}
        if new_type == 'student':  # add data between last student and first faculty
            persons.table.insert(len(student.table) + 1, person_data)
            logins.table.insert(len(student.table) + 1, login_data)
            student.table.append(Student(new_id, new_username))  # append data in Student object form to the database
        else:  # add data after last faculty
            persons.table.append(person_data)
            logins.table.append(login_data)
            faculty.table.append(Faculty(new_id, new_username))  # append data in Faculty object form to the database
        logins.update(lambda x: x['ID'] == new_id, 'role', 'new')  # update role to new, use to inform new password

    def delete_database(self):
        logins = my_DB.search('login')
        persons = my_DB.search('persons')
        print()
        print('Delete Data')
        user_id = input('AccountID you want to delete: ')
        all_id = [row['ID'] for row in logins.table]  # find all the id in the database
        if user_id not in all_id:  # check if input id can answer or not
            print('Invalid ID')
        else:
            this_person = [row for row in persons.table if row['ID'] == user_id][0]  # find request in persons
            if this_person['type'] in ['member', 'lead']:  # inform in this person involve in any project
                print('Can not delete this data, this student involve in some project.')
            elif this_person['type'] == 'faculty' and search_faculty(user_id).num_approve != 0:
                print('Can not delete this data, this faculty involve in some project.')
            else:
                option = get_option('Are you sure to delete this account(y/n)? ', ['y', 'n'])
                if option == 'y':
                    pending_member = my_DB.search('pending_member')
                    pending_advisor = my_DB.search('pending_advisor')
                    if this_person['type'] == 'student':
                        students = my_DB.search('student')
                        for i in range(len(students.table)):  # delete data that collect in Student class in database
                            if students.table[i] == search_student(user_id):
                                del students.table[i]
                                break  # break after find and delete that data
                        # change status of all the request to be Deny and send notification to lead
                        pending_member.update(lambda x: x['to_be_member'] == user_id, 'status', 'Deny')
                        update_lead(pending_member, lambda x: x['to_be_member'] == user_id, 'member', -1)
                    else:
                        faculty = my_DB.search('faculty')
                        for i in range(len(faculty.table)):  # delete data that collect in Faculty class in database
                            if faculty.table[i] == search_faculty(user_id):
                                del faculty.table[i]
                                break
                        # change status of all the request to be Deny and send notification to lead
                        pending_advisor.update(lambda x: x['to_be_advisor'] == user_id, 'status', 'Deny')
                        update_lead(pending_advisor, lambda x: x['to_be_advisor'] == user_id, 'advisor', -1)
                    for i in range(len(persons.table)):  # delete data in persons and login database
                        if persons.table[i]['ID'] == user_id:
                            del persons.table[i]
                            del logins.table[i]
                            break
                    print('Successfully delete this data.')
        input('Back to Edit Database Menu(enter): ')
        self.edit_database()

    def change_database(self):
        print()
        print('Change Data')
        logins = my_DB.search('login')
        user_id = input('AccountID you want to change: ')
        all_id = [row['ID'] for row in logins.table]  # get all the id in the database
        if user_id not in all_id:  # check if id input can not answer
            print('Invalid ID')
        else:
            print('******************************')
            print('There are 3 details you can change')
            print('1.ID')
            print('2.First Name')
            print('3.Last Name')
            print('0.None')
            print('******************************')
            option = get_option('Your Option: ', [str(n) for n in range(0, 4)])
            # get the old value that has not changed
            user_id, username, password, role = logins.filter(lambda x: x['ID'] == user_id).table[0].values()
            this_key = None
            new_val = None
            if option == '0':  # change None, so return back
                return
            elif option == '1':
                this_key = 'id'
                new_val = input('New ID: ')
                while len(new_val) != 7 or new_val in all_id:  # input until password not in database and has 7 digit
                    if len(new_val) != 7:  # check if password input has 7 digit or not
                        print('**ID must have 7 digits**')
                    else:
                        print('This ID has already taken.')
                    new_val = input('New ID: ')
            elif option == '2':
                this_key = 'first'
                new_val = input('New First Name: ').capitalize()
                username = new_val + '.' + username[-1]  # change first part of username to be new first
            elif option == '3':
                this_key = 'last'
                new_val = input('New Last Name: ').capitalize()
                username = username[:-2] + '.' + new_val[0]  # change last part of username to be new last
            check = get_option('Are you sure you want to change this data(y/n)? ', ['y', 'n'])
            if check == 'y':
                logins.update(lambda x: x['ID'] == user_id, 'username', username)  # update new username
                self.update_all(user_id, this_key, new_val)

    def update_all(self, user_id, key, new_value):
        if key == 'id':
            # update all table in database, since all of them has id
            this_id = [row for row in my_DB.search('persons').table if row['ID'] == user_id][0]
            my_DB.search('persons').update(lambda x: x['ID'] == user_id, key.upper(), new_value)
            my_DB.search('login').update(lambda x: x['ID'] == user_id, key.upper(), new_value)
            my_DB.search('pending_member').update(lambda x: x['to_be_member'] == user_id, 'to_be_member', new_value)
            my_DB.search('pending_advisor').update(lambda x: x['to_be_advisor'] == user_id, 'to_be_advisor', new_value)
            my_DB.search('sign_up').update(lambda x: x['ID'] == user_id, key.upper(), new_value)
            project = my_DB.search('project')  # change data in Project class
            lead = [row.Lead for row in project.table]  # find all Lead
            member1 = [row.Member1 for row in project.table]  # find all Member1
            member2 = [row.Member2 for row in project.table]  # find all Member2
            advisor = [row.Advisor for row in project.table]  # find all Advisor
            if user_id in lead + member1 + member2 + advisor:  # check if this id in project or not
                for row in project.table:  # if in find which project
                    all_id = [row.Lead, row.Member1, row.Member2, row.Advisor]
                    if user_id in all_id:  # if in this project, find which role it takes
                        if user_id in lead:
                            row.Lead = new_value
                        elif user_id in member1:
                            row.Member1 = new_value
                        elif user_id in member2:
                            row.Member2 = new_value
                        else:
                            row.Advisor = new_value
                        break
            if this_id['type'] == 'admin':  # change data that collect in Admin/Student/Faculty class
                my_DB.search('admin').table[0].id = new_value
            elif this_id['type'] == 'student':
                search_student(user_id).id = new_value
            else:
                search_faculty(user_id).id = new_value
        else:  # if change name, only change persons table
            my_DB.search('persons').update(lambda x: x['ID'] == user_id, key, new_value)

        print('Successfully, change the data.')
        input('Back to Edit Database Menu(enter): ')
        self.edit_database()

    def admin_check_request(self):
        print()
        print('Check Request Menu')
        print('******************************')
        print('1.Check Cancel Request')
        print('2.Check Sign Up Request')
        print('0.Admin Menu')
        print('******************************')
        option = get_option('Your Option: ', [str(n) for n in range(0, 4)])
        if option == '1':
            self.check_cancel()
        elif option == '2':
            self.check_sign_up()
        else:
            self.admin_menu()
        self.admin_check_request()

    def check_cancel(self):
        print()
        print('CANCEL PROJECT REQUEST')
        all_project = my_DB.search('project')  # find cancel that still waiting
        project_cancel = [row for row in all_project.table if row.Status == 'request_cancel']
        if not project_cancel:  # inform if there is none cancel request
            print('There is no requesting.')
            input('Back to Menu(enter): ')
        else:
            print('ProjectID           Title               Leader         ')
            print('------------------  ------------------  ----------------------')
            for pro in project_cancel:
                print(f'{pro.ProjectID:<20}{pro.Title:<20}{pro.get_full_name(pro.Lead)}')
            print('------------------  ------------------  ----------------------')
            print()
            option = get_option('Do you want to approve any cancel(y/n)? ', ['y', 'n'])
            if option == 'y':
                self.cancel_project(project_cancel)

    def cancel_project(self, all_pro):
        id_request = input('ProjectID you want to approve: ')
        all_pro_id = [row.ProjectID for row in all_pro]  # find all ProjectID that can answer
        if id_request not in all_pro_id:  # check if ProjectID input can answer or not
            print('Invalid ProjectID')
        else:
            lead_id = None
            project = my_DB.search('project').table
            for i in range(len(project)):  # delete data that collect in Project class from the database
                if project[i].ProjectID == id_request:
                    lead_id = project[i].Lead  # keep lead id to change the attribute project
                    del project[i]
                    break  # break after delete the data
            lead = search_student(lead_id)
            lead.project = None  # change attribute project to be None again
            self.num_request -= 1  # subtract notification that just answer
            print(f'Successfully cancel this project (id:{id_request}).')
        self.check_cancel()

    def check_sign_up(self):
        print()
        print('SIGN UP REQUEST')
        sign = my_DB.search('sign_up')
        all_sign = [row for row in sign.table if row['status'] == 'waiting']  # find all sing up that still waiting
        if not all_sign:
            print('There is no requesting.')
            input('Back to Menu(enter): ')
        else:
            print('ID             Name                     Type        ')
            print('-------------  -----------------------  ------------')
            for row in all_sign:
                print(f'{row["ID"]:<15}{row["first"] + " " + row["last"]:<25}{row["role"]:<12}')
            print('-------------  -----------------------  ------------')
            print()
            option = get_option('Do you want to answer any sign up(y/n)? ', ['y', 'n'])
            if option == 'y':
                self.answer_sign_up(all_sign)

    def answer_sign_up(self, all_sign):
        id_request = input('AccountID you want to answer: ')
        all_id = [row["ID"] for row in all_sign]  # get all id that can answer
        logins = my_DB.search('login')
        if id_request not in all_id:  # check if id input can answer or not
            print('Invalid ID')
        else:
            this_id = [row for row in all_sign if row['ID'] == id_request][0]  # get the sign_up for this request
            option = get_option('Accept or Deny this request(a/d): ', ['a', 'd'])
            for i in range(len(logins.table)):  # delete old login data that add when sign up
                if logins.table[i]['ID'] == id_request:
                    del logins.table[i]
                    break
            if option == 'a':
                new_id, new_first, new_last, new_type, status = this_id.values()
                self.add_database([new_id, new_first, new_last, new_type])  # add new data to all the database
                print(f'Successfully accept this sign up (id:{id_request}).')
            else:
                print(f'Successfully deny this sign up (id:{id_request}).')
            sign_up = my_DB.search('sign_up').table
            for i in range(len(sign_up)):  # delete this sign_up in the database
                if sign_up[i] == this_id:
                    del sign_up[i]
                    break  # break after find and delete
            self.num_request -= 1  # subtract notification that just answer
        self.check_sign_up()

    def reset(self):
        option = get_option('Do you want to reset the program(y/n)? ', ['y', 'n'])
        if option == 'y':
            logins = my_DB.search('login')
            logins.update(lambda x: x['role'] in ['student', 'member', 'lead'], 'role', 'student')
            logins.update(lambda x: x['role'] in ['faculty', 'advisor'], 'role', 'faculty')
            update_csv('login.csv', login_key, logins.table)
            if os.path.exists('Student.csv'):
                os.remove('Admin.csv')
                os.remove('Student.csv')
                os.remove('Faculty.csv')
                os.remove('Pending_member.csv')
                os.remove('Pending_advisor.csv')
                os.remove('Project.csv')
                os.remove('Send_proposal.csv')
                os.remove('Send_project.csv')
                os.remove('Sign_up.csv')
            print('Successfully reset the program.')
            sys.exit()
        self.admin_menu()


class Student:
    def __init__(self, get_id, get_name, project=None, num_answer=0):
        self.id = get_id
        self.name = get_name
        self.project = project
        self.num_answer = int(num_answer)  # for notification

    def get_table(self):
        return {'id': self.id, 'name': self.name, 'num_answer': self.num_answer}

    @staticmethod
    def check_available(role):
        logins = my_DB.search('login')
        if role == 'student':  # print all student that not involve in any project
            logins = logins.filter(lambda x: x['role'] in ['student', 'new'])  # check role (new can be student/faculty)
            for row in logins.table:
                student = search_student(row['ID'])
                if student is not None:  # check type (search will return only if type is student)
                    print(f'{student.id:<18}{student.name}')
        else:
            logins = logins.filter(lambda x: x['role'] in ['faculty', 'advisor', 'new'])  # check role
            for row in logins.table:
                faculty = search_faculty(row['ID'])
                if faculty is not None and faculty.num_project < 3:  # check type and free for being advisor or not
                    print(f'{faculty.id:<18}{faculty.name}')

    # ALL Student Method
    def student_menu(self):
        print()
        print('Student Menu')
        print('******************************')
        logins = my_DB.search('login')
        pending = my_DB.search('pending_member')
        projects = my_DB.search('project')
        if self.num_answer == 0:
            print(f'1.Check Request: No request')
        else:
            print(f'1.Check Request: {self.num_answer} request!')
        print('2.Create Project')
        print('0.Log Out')
        print('******************************')
        option = get_option('Your Option: ', [str(n) for n in range(0, 3)])
        if option == '1':
            self.student_check_request()
        elif option == '2':
            check = get_option('Are you sure to create your project(y/n)? ', ['y', 'n'])
            if check == 'y':  # create project
                title = input('Your project title: ').capitalize()
                all_request = pending.filter(lambda x: x['to_be_member'] == self.id and x['status'] == 'waiting')
                update_lead(all_request, None, 'member', -1)  # send notification to all lead that deny
                pending.update(lambda x: x['to_be_member'] == self.id, 'status', 'Deny')  # deny all project
                self.num_answer = 0  # clear all the notification
                logins.update(lambda x: x['ID'] == self.id, 'role', 'lead')  # change role to lead
                all_project_id = [row.ProjectID for row in projects.table]
                project_id = str(randint(66000, 66999))
                while project_id in all_project_id:
                    project_id = str(randint(66000, 66999))  # get ProjectID that never exist
                self.project = Project(project_id, title, self.id)  # create new project
                projects.table.append(self.project)  # add project to database
                print('Creating your project...')
                input('Go to your project menu(enter): ')
                self.lead_menu()
        elif option == '0':
            update_and_exit()
        self.student_menu()

    def student_check_request(self):
        if self.num_answer == 0:
            print('There is no request from any project')
            input('Back to Menu(enter): ')
            self.student_menu()
        pending = my_DB.search('pending_member')
        print()
        print('ProjectID         Title               Leader            ')
        print('----------------  ------------------  ------------------')
        for row in pending.table:
            if row['to_be_member'] == self.id and row['status'] == 'waiting':
                pro = search_project(row['ProjectID'])
                print(f'{pro.ProjectID:<18}{pro.Title:<20}{pro.get_full_name(pro.Lead)}')
        print()
        option = get_option('Do you want to answer any request(y/n)? ', ['y', 'n'])
        if option == 'y':
            self.student_answer_request()
        self.student_menu()

    def student_answer_request(self):
        pending = my_DB.search('pending_member')
        logins = my_DB.search('login')
        all_request = pending.filter(lambda row: row['to_be_member'] == self.id and row['status'] == 'waiting')
        all_pro = [row['ProjectID'] for row in all_request.table]
        pro_id = input('ProjectID you want to answer: ')
        if pro_id not in all_pro:
            print('Invalid ProjectID')
        else:
            answer = get_option('Accept or Deny this project(a/d)? ', ['a', 'd'])
            this_request = all_request.filter(lambda x: x['ProjectID'] == pro_id).table[0]
            if answer == 'a':
                my_project = search_project(pro_id)
                update_lead(all_request, lambda x: x['ProjectID'] != pro_id, 'member', -1)  # send notification
                my_lead = search_student(my_project.Lead)
                my_lead.num_answer += 1
                pending.update(lambda x: x['to_be_member'] == self.id and x['status'] == 'waiting', 'status', 'Deny')
                this_request['status'] = 'Accept'  # deny others and accept this project
                my_project.num_member += 1  # change number of member in project
                if my_project.num_member == 1:  # check if this is Member1 or Member2
                    my_project.Member1 = self.id
                else:
                    my_project.Member2 = self.id
                logins.update(lambda x: x['ID'] == self.id, 'role', 'member')  # change role to member
                self.project = my_project  # add this project to self attribute
                self.num_answer = 0  # clear all the answer
                print(f'Successfully Accept, now you are a member of project {pro_id}.')
                input('Go to Project Menu(enter): ')
                self.member_menu()
            else:
                pending.update(lambda x: x['to_be_member'] == self.id and x['ProjectID'] == pro_id, 'status', 'Deny')
                this_pro = search_project(pro_id)
                lead = search_student(this_pro.Lead)
                lead.num_answer += 1  # send notification to lead
                this_pro.num_member_requesting -= 1  # subtract project requesting member number
                self.num_answer -= 1  # remove notification that just answer
                print(f'Successfully Deny, project {pro_id}.\n')
        self.student_check_request()

    # Lead and Member Method
    def member_menu(self):
        print()
        print('Project Menu')
        print('******************************')
        print(f'Status: {self.project.Status}')
        if self.project.Status == 'Deny':  # inform about not approve sending project
            print('!!!This project has denied, please edit and send it again.!!!')
            self.project.Status = 'Processing'  # change status back to Processing
        print('1.Project Detail')
        print('2.Check Requesting Status')
        print('0.Log Out')
        print('******************************')
        option = get_option('Your Option: ', [str(n) for n in range(0, 3)])
        if option == '1':
            self.project.check_project_detail()
            if self.project.Status == 'Processing':  # if status is Processing, can change project detail
                option = get_option('Do you want to change any detail(y/n)? ', ['y', 'n'])
                if option == 'y':
                    self.project.change_project_detail()
            input('Back to Menu(enter): ')
        elif option == '2':
            self.check_request()
        else:
            update_and_exit()
        self.member_menu()

    def lead_menu(self):
        print()
        print('Project Menu')
        print('******************************')
        if self.project is None:  # inform about successful cancel project
            print('Admin has canceled your project.')
            login_table = my_DB.search('login')
            login_table.update(lambda x: x['ID'] == self.id, 'role', 'student')  # change role to student
            input('Back to Student Menu(enter): ')
            self.student_menu()
        print(f'Status: {self.project.Status}')
        if self.project.Status == 'Deny':  # inform about not approve sending project
            print('!!!This project has denied, please edit and send it again.!!!')
            self.project.Status = 'Processing'  # change status back to Processing
        if self.num_answer == 0:  # inform about number of notification
            print('1.Check Answer Request')
        else:
            print(f'1.Check Answer Request: new {self.num_answer} answer!')
        print('2.Project Detail')
        print('3.Request new Member')
        print('4.Request new Advisor')
        if self.project.num_submit in [-1, 3]:  # inform about approve/deny sending proposal
            print('5.Send Proposal: new message!')
        else:
            print('5.Send Proposal')
        print('6.Send Project')
        print('7.Cancel Project')
        print('0.Log Out')
        print('******************************')
        option = get_option('Your Option: ', [str(n) for n in range(0, 8)])
        if option == '1':
            self.check_request()
        elif option == '2':
            self.project.check_project_detail()
            if self.project.Status == 'Processing':  # if status is Processing, can change project detail
                option = get_option('Do you want to change any detail(y/n)? ', ['y', 'n'])
                if option == 'y':
                    self.project.change_project_detail()
            input('Back to Menu(enter): ')
        elif option == '3':
            self.request_new_member()
        elif option == '4':
            self.request_new_advisor()
        elif option == '5':
            self.send_proposal()
        elif option == '6':
            self.send_project()
        elif option == '7':
            self.cancel_project()
        elif option == '0':
            update_and_exit()
        self.lead_menu()

    def check_request(self):
        print()
        print('                   REQUESTING                   ')
        print('************************************************')
        self.check_request_member()
        print()
        self.check_request_advisor()
        print('************************************************')
        input('Back to Menu(enter): ')
        self.num_answer = 0

    def check_request_member(self):
        print('MEMBER')
        pending = my_DB.search('pending_member')
        all_request = [row for row in pending.table if row['ProjectID'] == self.project.ProjectID]
        if not all_request:
            print('There is no requesting.')
        else:
            print('StudentID         Username        Status')
            print('----------------  --------------  --------------')
            for request in all_request:
                student = search_student(request["to_be_member"])
                if student is None:
                    print('This student account has deleted by admin.')
                else:
                    print(f'{student.id:<18}{student.name:<16}{request["status"]}')

    def check_request_advisor(self):
        print('ADVISOR')
        pending = my_DB.search('pending_advisor')
        all_request = [i for i in pending.table if i['ProjectID'] == self.project.ProjectID]
        if not all_request:
            print('There is no requesting.')
        else:
            print('AdvisorID         Username        Status        ')
            print('----------------  --------------  --------------')
            for row in all_request:
                faculty = search_faculty(row["to_be_advisor"])
                print(f'{faculty.id:<18}{faculty.name:<16}{row["status"]}')

    # Lead ONLY method
    def request_new_member(self):
        print()
        if self.project.Status == 'request_cancel':  # if send cancel project, can not request
            print('You are in canceling project process, can not request any member.')
        elif self.project.num_member_requesting == 2:  # can request most 2 student for each time
            print('Max requesting member, can not add more.')
        else:
            print(f'Can request {2 - self.project.num_member_requesting} more member')
            check = get_option('Check available student(y/n)? ', ['y', 'n'])
            if check == 'y':
                print('StudentID         Username')
                print('----------------  --------------')
                self.check_available('student')
            id_request = input('Request Member ID: ')
            pend = my_DB.search('pending_member')
            logins = my_DB.search('login')
            check_stu = search_student(id_request)  # check if type is student
            all_pending = pend.filter(lambda x: x['ProjectID'] == self.project.ProjectID and x['status'] == 'waiting')
            available_id = logins.filter(lambda x: x['ID'] == id_request and x['role'] in ['student', 'new'])
            history = all_pending.filter(lambda x: x['to_be_member'] == id_request)  # check if not requesting before
            if not available_id.table or check_stu is None:
                print('Invalid ID or this student is in some project.')
            elif history.table:
                print('You have already sent request to this student.')  # that student has not answered yet
            else:
                member = search_student(id_request)
                member.num_answer += 1
                pend_data = {'ProjectID': self.project.ProjectID, 'to_be_member': id_request, 'status': 'waiting'}
                pend.table.append(pend_data)  # add new pending data to database
                self.project.num_member_requesting += 1  # update number of requesting member (max=2)
                print(f'Successfully, send request to {member.name} (id:{id_request}).')
            more = get_option('Do you want to request more member(y/n): ', ['y', 'n'])
            if more == 'y':
                self.request_new_member()
        input('Back to Menu(enter): ')
        self.lead_menu()

    def request_new_advisor(self):
        pending = my_DB.search('pending_advisor')
        if self.project.num_member < 2:  # can request after have all members in group
            print('Not enough member, can not send request to any advisor')
        elif self.project.num_advisor == 1:  # check if there is requesting before
            print('Already request advisor.')
        else:
            check = get_option('Check available advisor(y/n)? ', ['y', 'n'])
            if check == 'y':
                print('FacultyID         Username')
                print('----------------  --------------')
                self.check_available('faculty')
            id_request = input('Request Faculty ID: ')
            advisor = search_faculty(id_request)
            if advisor is None or advisor.num_project == 3:  # check if this is advisor and still free or not
                print('Invalid ID or this faculty advise maximum project')
            else:
                advisor.num_request += 1
                pend_data = {'ProjectID': self.project.ProjectID, 'to_be_advisor': id_request, 'status': 'waiting'}
                pending.table.append(pend_data)  # add new pending data to database
                self.project.num_advisor += 1  # update number of advisor that requesting
                print(f'Successfully, send request to {advisor.name} (id:{id_request}).')
        input('Back to Menu(enter): ')

    def send_proposal(self):
        if self.project.Advisor == '':  # can send proposal after have an advisor
            print('Your project does not have an advisor.')
        elif self.project.num_submit == 1:  # check if send the proposal before
            print('You have already send the project, waiting for your advisor to approve.')
        elif self.project.num_submit == -1:  # inform about the denied
            print('Your proposal has denied by the advisor, please edit and send it again.')
            self.project.num_submit = 0  # change back to not sending proposal
        elif self.project.num_submit >= 2:  # 3 = inform about the approved
            print('Your proposal has approved by the advisor.')
            self.project.num_submit = 2  # change back to not inform again
        else:
            option = get_option('Are you sure to send this proposal to your advisor(y/n)? ', ['y', 'n'])
            if option == 'y':
                send = my_DB.search('send_proposal')
                my_pro = self.project
                send_data = {'ProjectID': my_pro.ProjectID, 'advisor': my_pro.Advisor, 'status': 'waiting'}
                send.table.append(send_data)  # add sending data to the database
                advisor = search_faculty(my_pro.Advisor)
                advisor.num_submit += 1  # send notification to the advisor
                self.project.num_submit = 1  # update submit number, use for check if already submit or not
                print('Successfully send the proposal to your advisor.')
        input('Back to Menu(enter): ')

    def send_project(self):
        if self.project.num_submit == 0:  # check if sending proposal or not
            print('Send the proposal to your advisor before send the project to the committee.')
        elif self.project.num_submit == 1:  # check if proposal approved or not
            print('Your proposal is waiting for your advisor to approve.')
        elif self.project.Status == 'Processing':
            print('During evaluate your project, you can not change any information.')
            option = get_option('Are you sure to send this project(y/n)? ', ['y', 'n'])
            if option == 'y':
                faculty = my_DB.search('faculty')
                send_project = my_DB.search('send_project')
                my_pro = self.project
                if my_pro.Committee1 == '':  # check if first time of sending project
                    all_faculty = [row.id for row in faculty.table if row.id != my_pro.Advisor]
                    commit_list = []
                    for _ in range(3):  # random the committees that not include this project advisor
                        commit_choice = random.randint(0, len(all_faculty)-1)  # random position of the committee
                        commit_list.append(all_faculty[commit_choice])  # append that committee of that position
                        del all_faculty[commit_choice]  # delete faculty from the choice
                    my_pro.Committee1 = commit_list[0]  # add committee to project attribute
                    my_pro.Committee2 = commit_list[1]
                    my_pro.Committee3 = commit_list[2]
                all_committee = [my_pro.Committee1, my_pro.Committee2, my_pro.Committee3]
                for committee in all_committee:
                    sending_data = {'ProjectID': my_pro.ProjectID, 'committee': committee, 'status': 'waiting'}
                    send_project.table.append(sending_data)  # add sending data to the database
                    this_com = search_faculty(committee)
                    this_com.num_approve += 1  # send notification to the committee
                self.project.Status = 'Sending'  # change project status to Sending
                print('Successfully send this project, wait for the committees to approve.')
        else:
            print('You have already send this project.')
        input('Back to Menu(enter): ')

    def cancel_project(self):
        if self.project.num_member != 0:  # can cancel the project, only if there is none of the member
            print('Can not cancel this project.')
        else:
            if self.project.Status == 'request_cancel':  # check if already send the cancel or not
                print('Waiting for admin to approve your canceling')
            else:
                print('All of your requesting will be delete and can not add more member during waiting for cancel.')
                option = get_option('Are you sure to cancel this project(y/n)? ', ['y', 'n'])
                if option == 'y':
                    pending = my_DB.search('pending_member').table
                    for row in pending:
                        this_pro = search_project(row['ProjectID'])
                        if this_pro == self.project and row['status'] == 'waiting':  # change requesting status
                            student = search_student(row['to_be_member'])
                            student.num_answer -= 1  # subtract notification of student that request
                            row['status'] = 'cancel'  # change status to cancel
                    admin = my_DB.search('admin').table[0]
                    admin.num_request += 1  # send notification to admin
                    self.project.Status = 'request_cancel'  # change project status to request_cancel
                    print('Successfully, send request to admin.')
        input('Back to Menu(enter): ')


class Faculty:
    def __init__(self, get_id, get_name, num_p=0, num_r=0, num_s=0, num_a=0):
        self.id = get_id
        self.name = get_name
        self.num_project = int(num_p)  # max=3 projects for each faculty
        self.num_request = int(num_r)  # for notification
        self.num_submit = int(num_s)   # for proposal
        self.num_approve = int(num_a)  # for approve project

    def get_table(self):
        return {'id': self.id,
                'name': self.name,
                'num_project': self.num_project,
                'num_request': self.num_request,
                'num_submit': self.num_submit,
                'num_approve': self.num_approve}

    def faculty_menu(self):
        print()
        print('Faculty Menu')
        print('******************************')
        if self.num_approve == 0:  # inform about the notification
            print('1.Approve Project')
        else:
            print(f'1.Approve Project: {self.num_approve} project')
        if self.num_request == 0:
            print(f'2.Check Request')
        else:
            print(f'2.Check Request: {self.num_request} new request!')
        print('0.Log Out')
        print('******************************')
        option = get_option('Your Option: ', [str(n) for n in range(0, 3)])
        if option == '1':
            self.approve_project()
        elif option == '2':
            self.faculty_check_request()
            input('Back to Menu(enter): ')
        else:
            update_and_exit()
        self.faculty_menu()

    def advisor_menu(self):
        option_num = 3  # choice if number of project is maximum
        print()
        print('Advisor Menu')
        print('******************************')
        if self.num_approve == 0:
            print('1.Approve Project')
        else:
            print(f'1.Approve Project: {self.num_approve} project')
        print('2.Check Project')
        if self.num_submit == 0:
            print('3.Check Submit Proposal')
        else:
            print(f'3.Check Submit Proposal: {self.num_submit} new submit!')
        if self.num_project < 3:  # if num of the project is not maximum, can have the request
            option_num += 1  # add choice to be 4
            if self.num_request == 0:  # inform about the notification
                print(f'4.Check Request')
            else:
                print(f'4.Check Request: {self.num_request} new request!')
        print('0.Log Out')
        print('******************************')
        option = get_option('Your Option: ', [str(n) for n in range(0, option_num + 1)])
        if option == '1':
            self.approve_project()
        elif option == '2':
            self.check_project()
        elif option == '3':
            self.check_proposal()
        elif option == '4':
            self.faculty_check_request()
            input('Back to Menu(enter):')
        else:
            update_and_exit()
        self.advisor_menu()

    def approve_project(self):
        print()
        send = my_DB.search('send_project')
        my_approve = send.filter(lambda x: x['committee'] == self.id and x['status'] == 'waiting')
        if not my_approve.table:  # check if there is any project that waiting to approve
            print('There is no project you have to approve.')
        else:
            print('ProjectID         Title               ')
            print('----------------  --------------------')
            for row in my_approve.table:
                this_pro = search_project(row['ProjectID'])  # get detail from attributes in Project object
                print(f'{this_pro.ProjectID:<18}{this_pro.Title}')
            print()
            option = get_option('Do you want to answer any project(y/n)? ', ['y', 'n'])
            if option == 'y':
                my_approve_id = [row['ProjectID'] for row in my_approve.table]  # all ProjectID that can answer
                pro_id = input('ProjectID you want to answer: ')
                if pro_id not in my_approve_id:  # check if input in ProjectID can answer or not
                    print('Invalid ProjectID')
                else:
                    this_pro = search_project(pro_id)  # get Project object that will answer
                    check = get_option('Do you want to see this project detail(y/n): ', ['y', 'n'])
                    if check == 'y':  # ask if the faculty want to check the proposal or not
                        this_pro.check_project_detail()
                    approve = get_option('Approve or Deny this project(a/d)? ', ['a', 'd'])
                    if approve == 'a':
                        approved = my_approve.filter(lambda x: x['ProjectID'] == pro_id)  # find this send_proposal
                        approved.table[0]['status'] = 'Accept'  # change status to Accept
                        this_pro.num_approve += 1  # update num approved
                        if this_pro.num_approve == 3:  # if all committee approve
                            this_pro.Status = 'Approve'  # change project status to Approve
                        self.num_approve -= 1  # subtract the notification
                        print('Successfully Approve this project.')
                    else:
                        all_committee = send.filter(lambda x: x['ProjectID'] == pro_id and x['status'] == 'waiting')
                        for row in all_committee.table:  # delete sending to other committees if they have not answered
                            faculty = search_faculty(row['committee'])  # get committee in Faculty obj form
                            faculty.num_approve -= 1  # subtract the notification
                        this_pro = search_project(pro_id)
                        this_pro.Status = 'Deny'  # change project status to Deny and update status in sending database
                        this_pro.num_approve = 0  # reset number of approve back to 0
                        send.update(lambda x: x['ProjectID'] == pro_id and x['status'] == 'waiting', 'status', 'Deny')
                        print('Successfully Deny this project.')
        input('Back to Menu(enter): ')

    def check_project(self):
        projects = my_DB.search('project')
        all_project = projects.filter(lambda x: x.Advisor == self.id)
        num = 1  # the number that use in the table NO.
        print()
        print('PROJECT')
        print('NO. ProjectID      Title          Leader          ')
        print('--- -------------  -------------  ----------------')
        for row in all_project.table:
            print(f'{str(num) + "." :<4}{row.ProjectID:<15}{row.Title:<15}{row.get_full_name(row.Lead)}')
            num += 1  # update NO. for the next project
        print()
        option = get_option('Do you want to check any project detail(y/n)? ', ['y', 'n'])
        if option == 'y':
            pro_num = int(get_option('Which project you want to check? ', [str(n) for n in range(1, num + 1)]))
            this_project = all_project.table[pro_num - 1]  # search the project from NO. that received
            this_project.check_project_detail()
        input('Back to Menu(enter): ')

    def check_proposal(self):
        print()
        if self.num_submit == 0:  # check if there is
            print('None of the project proposal have submitted.')
        else:
            send = my_DB.search('send_proposal')
            my_proposal = send.filter(lambda x: x['advisor'] == self.id and x['status'] == 'waiting')
            print('ProjectID         Title')
            print('----------------  --------------------')
            for row in my_proposal.table:  # all in sending if status still waiting
                this_pro = search_project(row['ProjectID'])  # get the info from attribute in Project object
                print(f'{this_pro.ProjectID:<18}{this_pro.Title}')
            print()
            option = get_option('Do you want to answer any project proposal(y/n)? ', ['y', 'n'])
            if option == 'y':
                my_proposal = [row['ProjectID'] for row in my_proposal.table]  # all ProjectID that can answer
                pro_id = input('ProjectID you want to answer: ')
                if pro_id not in my_proposal:  # inform if ProjectID not in list that can answer
                    print('Invalid ProjectID')
                else:
                    answer = get_option('You want to approve or deny this proposal(a/d)? ', ['a', 'd'])
                    this_pro = search_project(pro_id)  # search for this project
                    self.num_submit -= 1  # subtract notification that just answer
                    if answer == 'a':
                        this_pro.num_submit = 3  # send notification to lead menu about the approving
                        send.update(lambda x: x['ProjectID'] == pro_id and x['status'] == 'waiting', 'status', 'Accept')
                        print('Successfully approve this project proposal.')
                    else:
                        this_pro.num_submit = -1  # send notification to lead menu about the denying
                        send.update(lambda x: x['ProjectID'] == pro_id, 'status', 'Deny')
                        print('Successfully deny this project proposal.')
        input('Back to Menu(enter): ')

    def faculty_check_request(self):
        print()
        print('PROJECT REQUESTING')
        if self.num_request == 0:  # check if there is not requested
            print('There is no request from any project')
        else:
            pending = my_DB.search('pending_advisor')
            print('ProjectID         Title               Leader            ')
            print('----------------  ------------------  ------------------')
            for row in pending.table:
                this_pro = search_project(row['ProjectID'])  # get the detail from attributes in Project object
                if row['to_be_advisor'] == self.id and row['status'] == 'waiting':
                    print(f'{this_pro.ProjectID:<18}{this_pro.Title:<20}{this_pro.get_full_name(this_pro.Lead)}')
            print()
            option = get_option('Do you want to answer any request(y/n)? ', ['y', 'n'])
            if option == 'y':
                self.faculty_answer_request()

    def faculty_answer_request(self):
        pend = my_DB.search('pending_advisor')
        logins = my_DB.search('login')
        all_request = pend.filter(lambda row: row['to_be_advisor'] == self.id and row['status'] == 'waiting')
        all_pro = [row['ProjectID'] for row in all_request.table]  # filter all ProjectID that can answer
        pro_id = input('ProjectID you want to answer: ')
        if pro_id not in all_pro:  # check if ProjectID can answer or not
            print('Invalid ProjectID')
        else:
            answer = get_option('Accept or Deny this project(a/d)? ', ['a', 'd'])
            this_request = all_request.filter(lambda x: x['ProjectID'] == pro_id).table[0]  # search for pending project
            my_project = search_project(this_request['ProjectID'])  # get the project in Project object form
            if answer == 'a':
                self.num_project += 1  # update number of the project that advice
                if self.num_project == 3:  # update notification to other lead and change the status to Deny
                    update_lead(all_request, lambda x: x['ProjectID'] != pro_id, 'advisor', -1)
                    pend.update(lambda x: x['to_be_advisor'] == self.id and x['status'] == 'waiting', 'status', 'Deny')
                this_request['status'] = 'Accept'  # change only this project status to Accept
                lead = search_student(my_project.Lead)
                lead.num_answer += 1  # send notification to lead that accept
                my_project.Advisor = self.id  # add id to the project
                print(f'Successfully Accept, now you are an advisor of project {pro_id}.')
                self.num_request -= 1  # subtract the notification that just answer
                if self.num_project == 1:  # if the first time to accept the project request
                    logins.update(lambda x: x['ID'] == self.id, 'role', 'advisor')  # change role to advisor
                    input('Go to Advisor Menu(enter): ')
                    self.advisor_menu()
                elif self.num_project == 3:  # if accept the last project
                    self.num_request = 0  # clear all the notification
                    input('Back to Menu(enter): ')
                    self.advisor_menu()
            else:
                pend.update(lambda x: x['to_be_advisor'] == self.id and x['ProjectID'] == pro_id, 'status', 'Deny')
                lead = search_student(my_project.Lead)
                lead.num_answer += 1  # send notification to lead
                my_project.num_advisor = 0  # update number of the advisor of that project, can add new advisor
                print(f'Successfully Deny, project {pro_id}.')
                self.num_request -= 1  # subtract notification that just answer
        self.faculty_check_request()


def update_and_exit():
    persons = my_DB.search('persons')
    logins = my_DB.search('login')
    admin = my_DB.search('admin')
    student = my_DB.search('student')
    faculty = my_DB.search('faculty')
    project = my_DB.search('project')
    pending_member = my_DB.search('pending_member')
    pending_advisor = my_DB.search('pending_advisor')
    sign_up = my_DB.search('sign_up')
    send_proposal = my_DB.search('send_proposal')
    send_project = my_DB.search('send_project')
    # update all the data to the csv file
    update_csv('persons.csv', persons_key, persons.table)
    update_csv('login.csv', login_key, logins.table)
    update_csv('Admin.csv', admin_key, [row.get_table() for row in admin.table])
    update_csv('Student.csv', student_key, [row.get_table() for row in student.table])
    update_csv('Faculty.csv', faculty_key, [row.get_table() for row in faculty.table])
    update_csv('Project.csv', project_key, [pro.get_table() for pro in project.table])
    update_csv('Pending_member.csv', pending_member_key, pending_member.table)
    update_csv('Pending_advisor.csv', pending_advisor_key, pending_advisor.table)
    update_csv('Sign_up.csv', sign_up_key, sign_up.table)
    update_csv('Send_proposal.csv', send_proposal_key, send_proposal.table)
    update_csv('Send_project.csv', send_project_key, send_project.table)
    sys.exit()


def search_project(check_id):  # return Project object that has ProjectID == check_id
    project_table = my_DB.search('project')
    project = project_table.filter(lambda x: x.ProjectID == check_id)
    if not project_table.table:
        return None  # return None if not have any project that have this same ProjectID
    else:
        return project.table[0]


def search_student(check_id):  # return Student object that has id == check_id
    student_table = my_DB.search('student')
    student = student_table.filter(lambda x: x.id == check_id)
    if not student.table:
        return None  # return None if there is no student
    else:
        return student.table[0]


def search_faculty(check_id):
    faculty_table = my_DB.search('faculty')
    faculty = faculty_table.filter(lambda x: x.id == check_id)
    if not faculty.table:
        return None  # return None if there is no faculty
    else:
        return faculty.table[0]


def processing(val):
    if val[1] == 'admin':
        admin = my_DB.search('admin').table[0]
        admin.admin_menu()
    if val[1] == 'student':
        student = search_student(val[0])
        student.student_menu()
    elif val[1] == 'member':
        member = search_student(val[0])
        member.member_menu()
    elif val[1] == 'lead':
        lead = search_student(val[0])
        lead.lead_menu()
    elif val[1] == 'faculty':
        faculty = search_faculty(val[0])
        faculty.faculty_menu()
    elif val[1] == 'advisor':
        advisor = search_faculty(val[0])
        advisor.advisor_menu()
    elif val[1] in ['waiting', 'new']:
        waiting_room(val[0])
    update_and_exit()


initializing()
value = login()
processing(value)
