import sqlite3

db_name = "quiz.sqlite"
conn =None
cursor  = None
def open():
        global conn, cursor
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

def close():
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        

def do(query):
        cursor.execute(query)
        conn.commit()

def clear_db():
        open()
        query = '''DROP TABLE IF EXISTS quiz'''
        do(query)
        query = '''DROP TABLE IF EXISTS quiz_content'''
        do(query)
        query = '''DROP TABLE IF EXISTS question'''
        do(query)
        close()

def create_db():
        open()
        cursor.execute('''PRAGMA foreign_keys=on''')
        query =''' CREATE TABLE IF NOT EXISTS quiz
                (
                    id  INTEGER PRIMARY KEY,
                    name VARCHAR
                )'''
        do(query)
        query = '''CREATE TABLE IF NOT EXISTS question(
            id INTEGER PRIMARY KEY,
            question VARCHAR,
            answer VARCHAR,
            wrong1 VARCHAR, 
            wrong2 VARCHAR, 
            wrong3 VARCHAR
        )'''
        do(query)
        query = ''' CREATE TABLE IF NOT EXISTS quiz_content(
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER,
        question_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz (id),
        FOREIGN KEY (question_id) REFERENCES question (id))'''
        do(query)
        close()

def add_question():
        questions = [
            ('Скільки місяців на рік мають 28 днів?', 'Всі', 'Один', 'Жодного', 'Два'),
            ('Яким стане зелена скеля, якщо впаде в Червоне море?', 'Мокрим', 'Червоним', 'Не зміниться', 'Фіолетовим'),
            ('Якою рукою краще розмішувати чай?', 'Ложкою', 'Правою', 'Лівою', 'Любою'),
            ('Що не має довжини, глибини, ширини, висоти, а можна виміряти?', 'Час', 'Дурність', 'Море', 'Повітря')
        ]
        open()
        cursor.executemany('''INSERT INTO question (question,answer,wrong1,wrong2,wrong3) VALUES (?,?,?,?,?)''',questions)
        conn.commit()
        close()

def add_quiz():
    quizes =[
        ('LOGIKA',),
        ('Нова Пошта',),
        ('Блок Петра Порошетка',)
        ]
    open()
    cursor.executemany("INSERT INTO quiz (name) VALUES (?)" , quizes    )
    conn.commit()
    close()
def add_links():
    open()
    cursor.execute(''' PRAGMA foreign_keys =on''')
    query = ''' INSERT INTO quiz_content(quiz_id,question_id) VALUES (?,?)'''
    answer = input("Додати зв'язок(y/n)")
    while answer != "n":
        quiz_id = int(input("id quiz:"))
        question_id  = int(input("id question"))
        cursor.execute(query,[quiz_id,question_id])
        answer = input("Додати зв'язок(y/n)")
    close()
def get_question_after(question_id = 0, quiz_id=1):
    ''' повертає наступне питання після запитання з переданим id
     для першого запитання передається значення за замовчуванням '''
    open()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id '''
    cursor.execute(query, [question_id, quiz_id] )
    result = cursor.fetchone()
    close()
    return result
def show(name_table):
        query = 'SELECT * FROM ' + name_table
        open()
        cursor.execute(query)
        print(cursor.fetchall())
        close()
def show_tables():
        print("QUIZ")
        show('quiz')
        print("QUESTION")
        show("question")
        print("CONTENT")
        show("quiz_content")

def main():
        clear_db()
        create_db()
        add_question()
        add_quiz()
        add_links()
        show_tables()

main()