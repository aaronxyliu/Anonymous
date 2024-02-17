import MySQLdb

class ConnDatabase:
    def __init__(self, database_name: str):
        self.connection = MySQLdb.connect(
            host= '127.0.0.1',
            user='root',
            passwd= '12345678',
            db= database_name,
            autocommit = True
        )
        self.cursor = self.connection.cursor()
    
    def close(self):
        self.connection.close()
    
    def create_if_not_exist(self, table_name: str, statement: str):
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS `{table_name}` ({statement});''')
        self.connection.commit()
    
    def insert(self, table_name: str, fields: list, values: tuple):
        if len(fields) == 0:
            return
        if len(fields) != len(values):
            print('[Warning] The number of fields and values are not equal.')
            return
        
        fields_str = "`, `".join(fields)
        placeholder_str = ", ".join(["%s"] * len(fields))
        sql = f"INSERT INTO `{table_name}` (`{fields_str}`) VALUES ({placeholder_str});"
        self.cursor.execute(sql, values)
        self.connection.commit()
        

    def selectAll(self, table_name: str, fields: list) -> list:
        if len(fields) == 0:
            return []
        fields_str = "`, `".join(fields)
        self.cursor.execute(f"SELECT `{fields_str}` FROM `{table_name}`;")
        res = self.cursor.fetchall()
        return res
    
    def fetchone(self, cmd: str) -> list:
        self.cursor.execute(cmd)
        return self.cursor.fetchone()
    
    def fetchall(self, cmd: str) -> list:
        self.cursor.execute(cmd)
        return self.cursor.fetchall()