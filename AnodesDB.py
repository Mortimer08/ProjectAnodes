import sqlite3 as sl
con = sl.connect('projectAnodes.db')
with con:
    data = con.execute(
        "select count (*) from sqlite_master where type='table' and name='Rows'")
    for row in data:
        if row[0] == 0:
            with con:
                con.execute("""
                CREATE TABLE Rows (
                    Litera VARCHAR (1) PRIMARY KEY,
                    CellsAmmount INTEGER,
                    Serial INTEGER
                );
                """)
    data = con.execute(
        "select count (*) from sqlite_master where type='table' and name='Cells'")
    for row in data:
        if row[0] == 0:
            with con:
                con.execute("""
                CREATE TABLE Cells (
                    Number INTEGER PRIMARY KEY
                );
                """)
    data = con.execute(
        "select count (*) from sqlite_master where type='table' and name='Takes'")
    for row in data:
        if row[0] == 0:
            with con:
                con.execute("""
                CREATE TABLE Takes (
                    Number INTEGER PRIMARY KEY,
                    AnodesAmount INTEGER
                );
                """)
    data = con.execute(
        "select count (*) from sqlite_master where type='table' and name='Teams'")
    for row in data:
        if row[0] == 0:
            with con:
                con.execute("""
                CREATE TABLE Teams (
                    Number INTEGER PRIMARY KEY
                );
                """)

    data = con.execute(
        "select count (*) from sqlite_master where type='table' and name='CellsInRow'")
    for row in data:
        if row[0] == 0:
            with con:
                con.execute("""
                CREATE TABLE CellsInRow (
                    CellUniqueID INTEGER AUTO_INCREMENT PRIMARY KEY,
                    RowsID VARCHAR (1),
                    CellsID INTEGER,
                    FOREIGN KEY (RowsID) REFERENCES Rows (Litera),
                    FOREIGN KEY (CellsID) REFERENCES Cells (Number)
                );
                """)


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

# sql = 'INSERT INTO Teams (Number) values(?)'
# data = [(1,)(2,),(3,),(4,),(5,)]
# with con:
#     con.executemany(sql,data)

# sql = 'INSERT INTO Takes (Number,AnodesAmount) values(?,?)'
# data = [
#     (1,21),
#     (2,20),
#     (3,20),
#     (4,20)
#     ]
# with con:
#     con.executemany(sql,data)

with con:

    # data = con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    # for row in data:
    #     print(row,end=' ')

    # data = con.execute("SELECT * FROM Rows")
    # for row in data:
    #     print(row)

    # data = con.execute("SELECT * FROM Cells")
    # for row in data:
    #     print(*row)

    # data = con.execute("SELECT * FROM Takes")
    # for row in data:
    #     print(row)

    # data = con.execute("SELECT * FROM Teams")
    # for row in data:
    #     print(*row)

    data = con.execute("SELECT * FROM CellsInRow")
    for row in data:
        print(*row)
