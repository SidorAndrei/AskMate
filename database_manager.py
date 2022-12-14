import datetime

import database_connection


@database_connection.connection_handler
def add_question(cursor, title, message, image, user_id):
    submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    query = """
            INSERT INTO question(title, message, image,user_id, submission_time) 
            VALUES (%(title)s, %(message)s, %(image)s, %(user_id)s, %(submission_time)s);"""
    cursor.execute(
        query,
        {
            "title": title,
            "message": message,
            "image": image,
            "user_id": user_id,
            "submission_time": submission_time,
        },
    )


@database_connection.connection_handler
def add_answer(cursor, question_id, message, image, user_id):
    submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    query = """
            INSERT INTO answer(question_id, message, image, user_id, submission_time) 
            VALUES (%(question_id)s, %(message)s, %(image)s, %(user_id)s, %(submission_time)s);"""
    cursor.execute(
        query,
        {
            "question_id": question_id,
            "message": message,
            "image": image,
            "user_id": user_id,
            "submission_time": submission_time,
        },
    )


@database_connection.connection_handler
def get_questions(cursor):
    query = """
            SELECT question.id as id, submission_time, view_number, vote_number, title, message, image, user_id, username, password, registration_date, reputation
            FROM question,users
            WHERE users.id=question.user_id
            ORDER BY question.id DESC
            ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_question_by_id(cursor, id):
    query = """
            SELECT question.id as id, submission_time, view_number, vote_number, title, message, image, user_id, username, password, registration_date, reputation
            FROM question,users
            WHERE users.id=question.user_id
                AND question.id = %(id)s;
            """
    cursor.execute(query, {"id": int(id)})
    return cursor.fetchone()


@database_connection.connection_handler
def update_question(cursor, question):
    query = """
               UPDATE question
               SET vote_number = %(vote_number)s,
                   view_number = %(view_number)s, 
                   message = %(message)s, 
                   title = %(title)s
               WHERE id = %(id)s
               ;"""
    cursor.execute(query, question)


@database_connection.connection_handler
def get_answers_for_question(cursor, question):
    query = """
            SELECT answer.id as id, submission_time, vote_number, question_id, message, image, user_id, accepted, username, password, registration_date, reputation
            FROM answer, users
            WHERE question_id = %(id)s AND users.id = user_id
            ;"""
    cursor.execute(query, {"id": int(question["id"])})
    return cursor.fetchall()


@database_connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    query = """
            SELECT answer.id as id, submission_time, vote_number, question_id, message, image, user_id, accepted, username, password, registration_date, reputation
            FROM answer, users
            WHERE answer.id = %(id)s AND users.id = user_id
                ;"""
    cursor.execute(query, {"id": int(answer_id)})
    return cursor.fetchone()


@database_connection.connection_handler
def update_answer(cursor, answer):
    query = """
               UPDATE answer
               SET message = %(message)s,
                vote_number = %(vote_number)s,
                accepted = %(accepted)s
               WHERE id=%(id)s;"""
    cursor.execute(query, answer)


@database_connection.connection_handler
def delete_question(cursor, question_id):
    delete_answers_for_question(question_id)
    query = """
                   DELETE FROM question
                   WHERE id=%(id)s
                   ;"""
    cursor.execute(query, {"id": int(question_id)})


@database_connection.connection_handler
def delete_answers_for_question(cursor, question_id):
    query = """
                   DELETE FROM answer
                   WHERE question_id=%(id)s
                   ;"""
    cursor.execute(query, {"id": int(question_id)})


@database_connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """
                   DELETE FROM answer
                   WHERE id=%(id)s
                   ;"""
    cursor.execute(query, {"id": int(answer_id)})


@database_connection.connection_handler
def get_question_seq_value(cursor):
    query = """
            SELECT last_value 
            FROM question_id_seq
            ;"""
    cursor.execute(query)
    return cursor.fetchone()


@database_connection.connection_handler
def get_answer_seq_value(cursor):
    query = """
            SELECT last_value 
            FROM answer_id_seq
            ;"""
    cursor.execute(query)
    return cursor.fetchone()


@database_connection.connection_handler
def add_comment_question(cursor, message, question_id, user_id):
    submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    query = """
            INSERT INTO comment(message, question_id, user_id, submission_time) 
            VALUES (%(message)s, %(question_id)s, %(user_id)s, %(submission_time)s);"""
    cursor.execute(
        query,
        {
            "message": message,
            "question_id": question_id,
            "user_id": user_id,
            "submission_time": submission_time,
        },
    )


@database_connection.connection_handler
def add_comment_answer(cursor, message, answer_id, user_id):
    submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    query = """
            INSERT INTO comment(message, answer_id, user_id, submission_time) 
            VALUES (%(message)s, %(answer_id)s, %(user_id)s, %(submission_time)s);"""
    cursor.execute(
        query,
        {
            "message": message,
            "answer_id": answer_id,
            "user_id": user_id,
            "submission_time": submission_time,
        },
    )


@database_connection.connection_handler
def delete_comment(cursor, comment):
    query = """
          DELETE FROM comment
          WHERE id = %(id)s
           ;"""
    cursor.execute(query, comment)


@database_connection.connection_handler
def update_comment(cursor, comment):
    query = """
            UPDATE comment
            SET 
            message = %(message)s,
            edited_count = %(edited_count)s
            WHERE id=%(id)s
            ;"""
    cursor.execute(query, comment)


@database_connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    query = """
                    SELECT * 
                    FROM comment
                    WHERE id = %(id)s
                    ;"""
    cursor.execute(query, {"id": int(comment_id)})
    return cursor.fetchone()


@database_connection.connection_handler
def get_question_by_search(cursor, search_term):
    query = """
        SELECT *
        FROM question
        WHERE LOWER(title) LIKE LOWER(%(search_term)s)
        OR LOWER(message) LIKE LOWER(%(search_term)s)
        ORDER BY submission_time
            ;"""
    cursor.execute(query, {"search_term": ("%" + search_term + "%")})
    return cursor.fetchall(), search_term


@database_connection.connection_handler
def get_latest_five_questions(cursor):
    query = """
        SELECT question.id, submission_time, view_number, vote_number, title, message, image, user_id, username, password, registration_date, reputation
        FROM question, users
        WHERE user_id=users.id  
        ORDER BY id DESC  
            ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_answer_comments(cursor, answer):
    query = """
            SELECT comment.id as id, question_id, answer_id, message, submission_time, edited_count, user_id, username, password, registration_date, reputation
            FROM comment, users
            WHERE answer_id = %(id)s AND comment.user_id = users.id
            ;"""
    cursor.execute(query, answer)
    return cursor.fetchall()


@database_connection.connection_handler
def get_question_comments(cursor, question):
    query = """
            SELECT comment.id as id, question_id, answer_id, message, submission_time, edited_count, user_id, username, password, registration_date, reputation
            FROM comment, users
            WHERE question_id = %(id)s  AND comment.user_id=users.id
            ;"""
    cursor.execute(query, question)
    return cursor.fetchall()


@database_connection.connection_handler
def add_tag(cursor, name):
    query = """
        INSERT INTO tag (name)
        VALUES  (
                LOWER(%(name)s)
                )   
            ;"""
    cursor.execute(query, {"name": name})


@database_connection.connection_handler
def add_tag_relation(cursor, question_id, tag_id):
    query = """
        INSERT INTO question_tag
        VALUES  (
                %(question_id)s,
                %(tag_id)s
                )   
            ;"""
    cursor.execute(query, {"question_id": question_id, "tag_id": tag_id})


@database_connection.connection_handler
def get_tag_by_name(cursor, tag_name):
    query = """
            SELECT *
            FROM tag 
            WHERE name = LOWER(%(name)s) 
                ;"""
    cursor.execute(query, {"name": tag_name})
    return cursor.fetchone()


@database_connection.connection_handler
def get_tag_by_id(cursor, tag_id):
    query = """
            SELECT *
            FROM tag 
            WHERE id = %(id)s
                ;"""
    cursor.execute(query, {"id": tag_id})
    return cursor.fetchone()


@database_connection.connection_handler
def get_sorted_questions(cursor, sort_by, order_direction):
    query = f"""
                SELECT *
                FROM question 
                order by {sort_by} {order_direction}
                    ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_tag_relation(cursor, question_id):
    query = """
                SELECT *
                FROM question_tag 
                WHERE question_id = %(question_id)s 
                    ;"""
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()


@database_connection.connection_handler
def delete_tag_relation(cursor, question_id, tag_id):
    query = """
            DELETE FROM question_tag
            WHERE 
                question_id = %(question_id)s
            AND
                tag_id = %(tag_id)s
            ;"""
    cursor.execute(query, {"question_id": question_id, "tag_id": tag_id})


@database_connection.connection_handler
def delete_all_question_tags_relation(cursor, question_id):
    query = """
              DELETE FROM question_tag
              WHERE 
                  question_id = %(question_id)s
              ;"""
    cursor.execute(query, {"question_id": question_id})


@database_connection.connection_handler
def get_user(cursor, username):
    query = """
            SELECT *
            FROM users
            WHERE username=%(username)s
            ;"""
    cursor.execute(query, {"username": username})
    return cursor.fetchone()


@database_connection.connection_handler
def get_all_users_questions(cursor):
    query = """
            SELECT username,   
            DATE(registration_date) AS registration_date,
            COUNT(question.id) AS questions,
            COUNT(answer.id) AS answers,
            COUNT(comment.id) AS comments
            FROM users
            INNER JOIN question on users.id = question.user_id
            INNER JOIN answer on users.id = answer.user_id
            INNER JOIN comment on users.id = comment.user_id
            GROUP BY username, DATE(registration_date)
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def insert_user(cursor, username, password, reputation):
    registration_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    query = """
                INSERT INTO users(username, password, reputation, registration_date)
                VALUES(%(username)s, %(password)s, %(reputation)s, %(registration_date)s )
                ;"""
    cursor.execute(
        query,
        {
            "username": username,
            "password": password,
            "reputation": reputation,
            "registration_date": registration_date,
        },
    )


@database_connection.connection_handler
def get_comment_number(cursor, id_user):
    query = """
            SELECT 
                COUNT(comment.id) as number_of_comment
            FROM comment
            WHERE 
                comment.user_id = %(id_user)s
        ;"""
    cursor.execute(query, {"id_user": id_user})
    return cursor.fetchone()


@database_connection.connection_handler
def get_answer_number(cursor, id_user):
    query = """
            SELECT 
                COUNT(answer.id) as number_of_answers
            FROM answer
            WHERE user_id = %(id_user)s
        ;"""
    cursor.execute(query, {"id_user": id_user})
    return cursor.fetchone()


@database_connection.connection_handler
def get_question_number(cursor, id_user):
    query = """
            SELECT COUNT(question.id) as number_of_questions
            FROM question
            WHERE user_id = %(id_user)s
        ;"""
    cursor.execute(query, {"id_user": id_user})
    return cursor.fetchone()


@database_connection.connection_handler
def get_user_by_id(cursor, user_id):
    query = """
            SELECT *
            FROM users
            WHERE id=%(user_id)s
            ;"""
    cursor.execute(query, {"user_id": user_id})
    return cursor.fetchone()


@database_connection.connection_handler
def get_questions_user(cursor, user_id):
    query = """
            SELECT *
            FROM question
            WHERE user_id=%(user_id)s
            ;"""
    cursor.execute(query, {"user_id": user_id})
    return cursor.fetchall()


@database_connection.connection_handler
def get_answers_user(cursor, user_id):
    query = """
            SELECT *
            FROM answer
            WHERE user_id=%(user_id)s
            ;"""
    cursor.execute(query, {"user_id": user_id})
    return cursor.fetchall()


@database_connection.connection_handler
def get_comments_user(cursor, user_id):
    query = """
            SELECT *
            FROM comment
            WHERE user_id=%(user_id)s
            ;"""
    cursor.execute(query, {"user_id": user_id})
    return cursor.fetchall()


@database_connection.connection_handler
def get_tags(cursor):
    query = """
                SELECT id, name, COUNT(question_id)
                FROM tag, question_tag
                WHERE id=tag_id
                GROUP BY id
                ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_users(cursor):
    cursor.execute(
        "select u.id, u.username, DATE(u.registration_date) AS registration_date, reputation from users u;"
    )
    users = cursor.fetchall()
    cursor.execute(
        "select count(c.id) as comment, c.user_id from comment c group by c.user_id;"
    )
    comments = cursor.fetchall()
    cursor.execute(
        "select count(a.id) as answer, a.user_id from answer a group by a.user_id;"
    )
    answers = cursor.fetchall()
    cursor.execute(
        "select count(q.id) as question, q.user_id from question q group by q.user_id;"
    )
    questions = cursor.fetchall()
    for i, u in enumerate(users):
        comment = [
            c.get("comment") for c in comments if c.get("user_id") == u.get("id")
        ]
        comment = comment.pop() if len(comment) else 0
        answer = [c.get("answer") for c in answers if c.get("user_id") == u.get("id")]
        answer = answer.pop() if len(answer) else 0
        question = [
            c.get("question") for c in questions if c.get("user_id") == u.get("id")
        ]
        question = question.pop() if len(question) else 0
        users[i].update(
            {
                "comments": comment,
                "answers": answer,
                "questions": question,
            }
        )
    return users


@database_connection.connection_handler
def update_reputation(cursor, user):
    query = """
               UPDATE users
               SET reputation = %(reputation)s
               WHERE id=%(id)s;"""
    cursor.execute(query, user)


@database_connection.connection_handler
def get_answer_for_comment(cursor, comment_id):
    query = """
        SELECT * FROM answer
        WHERE id = (SELECT answer_id FROM comment WHERE comment.id=%(comment_id)s)
            ;"""
    cursor.execute(query, {"comment_id": comment_id})
    cursor.fetchone()


@database_connection.connection_handler
def get_questions_by_tag_id(cursor, tag_id):
    query = """
        SELECT * FROM question
        WHERE id in (SELECT question_id FROM question_tag WHERE tag_id=%(tag_id)s)
            ;"""
    cursor.execute(query, {"tag_id": tag_id})
    return cursor.fetchall()
