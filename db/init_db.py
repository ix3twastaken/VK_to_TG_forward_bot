from models import get_connection

con = get_connection()
cursor = con.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS last_url (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT)
    """
)

# cursor.execute(
#     """
#     DROP TABLE last_url
#     """
# )

con.commit()
cursor.close()
con.close()