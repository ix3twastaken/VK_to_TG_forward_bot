import sqlite3

def get_connection():
    return sqlite3.connect("last_urls.db")

def last_url_db():
    con = get_connection()
    cursor = con.cursor()

    cursor.execute(
        """
        SELECT url FROM last_url
        """
    )

    rows = cursor.fetchone()
    url = rows
    # print(url)
    
    con.commit()
    cursor.close()
    con.close()
    return url

def add_last_url_to_db(id: int, url: str):
    con = get_connection()
    cursor = con.cursor()

    cursor.execute(
        """
        INSERT INTO last_url (id, url)
        VALUES (?, ?)
        ON CONFLICT(id) DO UPDATE SET url=excluded.url
        """,
        (id, url,)
    )

    con.commit()
    cursor.close()
    con.close()


