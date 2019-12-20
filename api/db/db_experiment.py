import pymysql


### Testing db functions
def test_con():  # pragma: no cover
    return pymysql.connect("localhost", "test_user", "password", "ssd_sample_database")


def test_execute(cmd):  # pragma: no cover
    db = test_con()
    cursor = db.cursor()
    cursor.execute(cmd)
    res = cursor.fetchall()
    cursor.close()
    db.close()
    return res
