import sqlite3 as sl
con = sl.connect('projectAnodes.db')
with con:
    con.execute("""
    CREATE TABLE Rows (
        Litera VARCHAR (1) PRIMARY KEY,
        CellsAmmount INT,
        Serial INT
    );
    """)