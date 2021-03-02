import mysql.connector

class SqlQueryBuilder():
    conn = mysql.connector.connect(host='127.0.0.1', user='root', passwd='*********', database='audiofileserverdb')
    cursor = conn.cursor()

    def __init__(self):
        try:
            self.conn =mysql.connector.connect(host='127.0.0.1', user='root', passwd='***********', database='audiofileserverdb')
            self.cursor = self.conn.cursor()
        except BaseException as e:
            print(str(e))


    def readProcedureJson(self, query, querParam):
        dataResult = []
        dataset = []
        if querParam is None:
            self.cursor.callproc(query)
        else:

            self.cursor.callproc(query, querParam)
        for result in self.cursor.stored_results():
            columns = result.column_names
            dataset = result.fetchall()

        for row in dataset:
            dataResult.append(dict(zip(columns, row)))

        return dataResult

    def dispose(self):
        try:
            self.conn.commit()
            self.cursor.close()
        except BaseException as e:
            print(str(e))
            try:
                self.cursor.close()
            except BaseException as e:
                print(str(e))

    def closeConnection(self):
        try:
            self.cursor.close()
        except BaseException as e:
            print(str(e))

    def commit(self):
        try:
            self.conn.commit()
        except BaseException as e:
            print(str(e))

    def readMultipleProcedureJson(self, query, querParam):
        dataResult = []
        dataset = []
        data = []
        if querParam is None:
            self.cursor.callproc(query)
        else:

            self.cursor.callproc(query, querParam)
        for result in self.cursor.stored_results():
            columns = result.column_names
            dataset = result.fetchall()
            
            for row in dataset:
                dataResult.append(dict(zip(columns, row)))
            data.append(dataResult)
            dataResult = []
        return data
            
        
       
            
        
                

        
       