import mysql.connector
from mysql.connector import Error


def insert_articles(articles, company_id):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='techblog',
                                             user='root',
                                             password='2!%vdLcXF6NJrtbE')

        for article in articles:
            print("Inserting article:", article.title)
            try:
                mySql_insert_query = """INSERT INTO blogs (url, title, company_id, date)
                                        VALUES
                                        (%s, %s, %s, %s)"""

                record = (article.url, article.title, company_id, article.date)

                cursor = connection.cursor()
                cursor.execute(mySql_insert_query, record)
                connection.commit()
            except Error as e:
                print("failed to insert", e)

    except Error as e:
        print("failed to load DB", e)

    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
