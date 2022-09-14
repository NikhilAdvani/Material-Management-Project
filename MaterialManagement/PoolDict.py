import pymysql as mysql
def ConnectionPool():
    db = mysql.connect(host="campusshala.com", port=3306, user="campussh_mm", password="sandeep123@", db="campussh_mm")
    cmd=db.cursor(mysql.cursors.DictCursor)
    return (db,cmd)