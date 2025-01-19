from sqlite3 import connect, Error
def insertkino(id1, kino, izoh):
    try:
        create = connect('dp.sqlite3')
        cursor = create.cursor()
        cursor.execute("""INSERT INTO kino(id, kino, izoh) VALUES (?,?, ?)""", (id1,kino, izoh))
        create.commit()
    except (Exception, Error) as error:
        print('xato_creat_teble', error)
    finally:
        if create:
            cursor.close()
            create.close()

def readkino():
    try:
        create = connect('dp.sqlite3')
        cursor = create.cursor()
        cursor.execute("""Select * from kino""")
        a = cursor.fetchall()
        return a
    except (Exception, Error) as error:
        print('xato_creat_teble', error)
    finally:
        if create:
            cursor.close()
            create.close()

def deleteKino(kod):
    try:
        create = connect('dp.sqlite3')
        cursor = create.cursor()
        cursor.execute("DELETE FROM kino WHERE id = ?",  (kod,))
        create.commit()
    except (Exception, Error) as error:
        print('xato_delete_teble', error)
    finally:
        if create:
            cursor.close()
            create.close()

def insertuser(user_id):
    try:
        create = connect('dp.sqlite3')
        cursor = create.cursor()
        cursor.execute("""INSERT INTO user(user) VALUES (?)""", (user_id,))
        create.commit()
    except (Exception, Error) as error:
        print('xato_insert_teble', error)
    finally:
        if create:
            cursor.close()
            create.close()

def readuser():
    try:
        create = connect('dp.sqlite3')
        cursor = create.cursor()
        cursor.execute("""Select * from user""")
        a = cursor.fetchall()
        return a
    except (Exception, Error) as error:
        print('xato_creat_teble', error)
    finally:
        if create:
            cursor.close()
            create.close()