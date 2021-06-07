from sqlite3 import connect
from datetime import datetime

class Database:

    @staticmethod
    def insert(name, text, time):
        try:
            my_con = connect('messagebox.db')
            my_cursor = my_con.cursor()
            time = datetime.now()
            time = time.strftime('%y/%m/%d - %H:%M')
            my_cursor.execute(f"INSERT INTO messages(name, text, time) VALUES('{name}' , '{text}', '{time}')")
            my_con.commit()
            my_con.close()
            return True
        except:
            return False

    @staticmethod
    def select():
        try:
            my_con = connect('messagebox.db')
            my_cursor = my_con.cursor()
            my_cursor.execute("SELECT * FROM messages")
            result = my_cursor.fetchall()
            my_con.close()
            return  result
        except:
            return []

    @staticmethod
    def delete_all():
        try:
            my_con = connect('messagebox.db')
            my_cursor = my_con.cursor()
            my_cursor.execute('DELETE FROM messages')
            my_con.commit()
            # my_con.close()
            return True
        except:
            return False


    @staticmethod
    def delete(id):
        try:
            my_con = connect('messagebox.db')
            my_cursor = my_con.cursor()
            my_cursor.execute(f'DELETE FROM messages WHERE id ={id}')
            my_con.commit()
            my_con.close()
            return True
        except:
            return False