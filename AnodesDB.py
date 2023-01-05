import sqlite3 as sl
con = sl.connect('projectAnodes.db')
with con:
    data = con.execute("select count (*) from sqlite_master where type='table' and name='Rows'")
    for row in data:
        if row[0]==0:
            with con:
                con.execute("""
                CREATE TABLE Rows (
                    Litera VARCHAR (1) PRIMARY KEY,
                    CellsAmmount INTEGER,
                    Serial INTEGER
                );
                """)
    data = con.execute("select count (*) from sqlite_master where type='table' and name='Cells'")
    for row in data:
        if row[0]==0:
            with con:
                con.execute("""
                CREATE TABLE Cells (
                    Number INTEGER PRIMARY KEY
                );
                """)
    data = con.execute("select count (*) from sqlite_master where type='table' and name='Takes'")
    for row in data:
        if row[0]==0:
            with con:
                con.execute("""
                CREATE TABLE Takes (
                    Number INTEGER PRIMARY KEY,
                    AnodesAmmount INTEGER
                );
                """)
    data = con.execute("select count (*) from sqlite_master where type='table' and name='Teams'")
    for row in data:
        if row[0]==0:
            with con:
                con.execute("""
                CREATE TABLE Teams (
                    Number INTEGER PRIMARY KEY
                );
                """)          

    # data = con.execute("select count (*) from sqlite_master where type='table' and name='CellsInRow'")
    # for row in data:
    #     if row[0]==0:
    #         with con:
    #             con.execute("""
    #             CREATE TABLE Rows (
    #                 Litera VARCHAR (1) PRIMARY KEY,
    #                 CellsAmmount INTEGER,
    #                 Serial INTEGER
    #             );
    #             """)      
                
# sql = 'INSERT INTO Rows (Litera, CellsAmmount, Serial) values(?,?,?)'
# data = [
#     ('A', 51, 1),
#     ('B', 51, 1),
#     ('C', 51, 2),
#     ('D', 51, 2)
# ]

# for CellNumber in range(1,52):
#     sql = f'INSERT INTO Cells VALUES ({CellNumber})'
#     with con:
#         con.execute(sql)



with con:

    data = con.execute("SELECT * FROM Rows")
    for row in data:
        print(row)

    data = con.execute("SELECT * FROM Cells")
    for row in data:
        print(row)
