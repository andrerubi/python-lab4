from sys import argv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pymysql


hello_msg = "Welcome in AmI Task List 237031 bot!\nHere's a list of commands you can use:\n" \
            "/showTasks - show all the existing tasks in alphabetic order\n" \
            "/newTask - insert a new task\n" \
            "/removeTask - remove a task (by typing its content, exactly)\n" \
            "/removeAllTasks - remove all the existing tasks that contain a provided string\n" \
            "/help - read again this message\n\n" \
            "All the commands are executed on a local based database (id, task)"

# getting list from db
index=0
sql = "select task from todo"
conn = pymysql.connect(user="root", password="", host="localhost", database="taskslist")
cursor = conn.cursor()
cursor.execute(sql)
result = cursor.fetchall()
todo = [i[0] for i in result]
cursor.close()
conn.close()


def start(bot, update):
    update.message.reply_text(hello_msg)


def echo(bot, update):
    update.message.reply_text("I'm sorry. I can't do that.")


def show_task(bot, update):
    update.message.reply_text("Here's the list of to do tasks:\n")
    output_msg = "Nothing to do, here!"

    if len(todo) != 0:
        output_msg = ""
        for task in todo:
            output_msg = output_msg + task + "\n"

    update.message.reply_text(output_msg)


def new_task(bot, update, args):
    task = " ".join(args)

    if task != "":
        todo.append(task)

        sql = "insert into todo(task) values (%s)"
        conn = pymysql.connect(user="root", password="", host="localhost", database="taskslist")
        cursor = conn.cursor()
        cursor.execute(sql, task)
        conn.commit()
        cursor.close()
        conn.close()

        update.message.reply_text("'" + task + "' insert in the list.")
    else:
        update.message.reply_text("You must write a task to be added in the list.")


def delete_from_db(task=''):
    sql = "delete from todo where task=%s"
    conn = pymysql.connect(user="root", password="", host="localhost", database="taskslist")
    cursor = conn.cursor()
    cursor.execute(sql, task)
    conn.commit()
    cursor.close()
    conn.close()


def remove_task(bot, update, args):
    task = " ".join(args)
    removed = False

    for t in todo:
        if t == task:  # task to be deleted
            todo.remove(task)
            delete_from_db(task)
            update.message.reply_text("'" + task + "' removed")
            removed = True

    if not removed:
        update.message.reply_text("Can't find '" + task + "' in the list")


def remove_all(bot, update, args):
    task = " ".join(args)
    cont = 0  # count of deleted tasks
    remove_list = []

    for t in todo:
        if task in t:  # task to be deleted
            delete_from_db(t)
            remove_list.append(t)
            cont = cont + 1

    for t in remove_list:
        if t in todo:
            todo.remove(t)

    update.message.reply_text(str(cont) + " task(s) containing '" + task + "' removed\n")


def main():
    if __name__ == '__main__':
        updater = Updater(token='TOKEN')  # insert your token instead of TOKEN

        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", start))
        dp.add_handler(CommandHandler("showTasks", show_task))
        dp.add_handler(CommandHandler("newTask", new_task, pass_args=True))
        dp.add_handler(CommandHandler("removeTask", remove_task, pass_args=True))
        dp.add_handler(CommandHandler("removeAllTasks", remove_all, pass_args=True))
        dp.add_handler(MessageHandler(Filters.text, echo))

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    main()
