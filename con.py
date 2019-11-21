import pymysql

con = pymysql.connect('localhost', 'test_user', 'password', 'ssd_sample_database')
c = con.cursor()
c.execute('SELECT * FROM pt_deid')

breakpoint()


