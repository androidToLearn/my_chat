from flask import Flask, render_template, redirect, jsonify, request, send_from_directory, redirect, url_for, jsonify
from dal.Sql_message import Sql_message
from objects.Message import Message
app = Flask(__name__)

users = []
messages = []


@app.route('/', methods=['get'])
def index():
    return render_template('page1.html')


isWasInAdd_User = False


@app.route('/add_user', methods=['get', 'post'])
def add_user():
    print('add_user')
    # keep to files
    contact = None
    try:
        json = request.get_json()
        contact = json['contact']
        with open('name_user.txt', 'r', encoding='utf-8') as file:
            name_user = file.read()
    except Exception:
        name_user = request.form.get('name')
        contact = name_user
        with open('name_user.txt', 'w', encoding='utf-8') as file:
            file.write(name_user)
        if not name_user in users:
            users.append(name_user)

    with open('contact.txt', 'w', encoding='utf-8') as file:
        file.write(contact)
    isWasInAdd_User = True
    return redirect(url_for('update_chat', name=name_user, contact=contact))


@app.route('/update_chat/<name>/<contact>', methods=['get'])
def update_chat(name, contact):
   # if isWasInAdd_User:
    #    isWasInAdd_User = False
    #    return render_template('page2.html', messages=getAllMessagesFromSql(contact, name), user_name=name, contact=contact, users=users)

    print('update_chat')
    currentName = None
    currentContact = None
    print('name:', name, 'contact: ' + contact)
    with open('contact.txt', 'r', encoding='utf-8') as file:
        currentContact = file.read()
    with open('name_user.txt', 'r', encoding='utf-8') as file:
        currentName = file.read()

    addRlevantMessagesToSql(name)
    print(len(getAllMessagesFromSql(contact, name)))
    return render_template('page2.html', messages=notReturn(getAllMessagesFromSql(currentContact, currentName)), user_name=currentName, contact=currentContact, users=users)


def notReturn(messages):
    messagesr = []
    names = []
    for m in messages:
        nameM = str(m.sendTo) + str(m.sendFrom) + str(m.message)
        if not nameM in names:
            names.append(nameM)
            messagesr.append(m)
    return messagesr


@app.route('/add_message/<name>/<contact>', methods=['post'])
def add_message(name, contact):
    print('add_message')
    #    def __init__(self, message: str, sendTo: str, sendFrom: str, id: int, filename: str, isFrom_get: bool, isTo_get: bool):
    message = request.form.get('message')
    print(message)
    messages.append(Message(message, contact, name, -1, '', False, False))
    return redirect(url_for('update_chat', name=name, contact=contact))


def addRlevantMessagesToSql(name):
    sql_message = Sql_message()
    print('------------------------------inserting: name', name,
          '------------------------------------------------')
    for message in messages:
        if message.sendTo == name and message.isTo_get == False:
            print('insert: ' + message.message, 'from',
                  message.sendFrom, 'to', message.sendTo)
            sql_message.insertOne(message)
            message.isTo_get = True

        if message.sendFrom == name and message.isFrom_get == False:
            print('insert: ' + message.message, 'from',
                  message.sendFrom, 'to', message.sendTo)
            sql_message.insertOne(message)
            message.isFrom_get = True

        if message.isTo_get == True and message.isFrom_get == True:
            print(message)
            messages.remove(message)


def getAllMessagesFromSql(contact, name):
    sql_messages = Sql_message()
    messages = sql_messages.getAllByNameChatWith(contact, name)
    print('-------------------------------------', name,
          '-----------------------------------------')
    for m in messages:
        print('message:', m.message, 'sendTo',
              m.sendTo, 'sendFrom', m.sendFrom)
    print('---------------------------------all messages----',
          name, '-----------------------------------------')
    for m in sql_messages.getAllMessages():
        print('message:', m.message, 'sendTo',
              m.sendTo, 'sendFrom', m.sendFrom)
    return messages


if __name__ == '__main__':
    app.run(debug=True)
