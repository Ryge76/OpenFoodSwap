"""This file contains necessary information to connect and acces the OFS database"""


def select_user():
    users = ['appadm', 'appuser']
    answer = ''
    while answer not in users:
        answer = input("Sélectionnez un utilisateur parmi {} : ".format(users))
    return answer


# db_access = {
#     'host': 'localhost',
#     'port': '3306',
#     'database': 'ofsdb',
#     'user': select_user(),
#     'password': input("Saisissez le mot de passe pour cet utilisateur:  ")
# }

# for testing access to the database
db_access_testing = {
    'host': 'localhost',
    'port': '3306',
    'database': 'ofsdb',
    'user': 'appadm',
    'password': 'testrole'
}

