import sqlite3

def connectDbFile(dbFile):
    con =sqlite3.connect(dbFile)
    cur = con.cursor()
    return con, cur



def get_password_manager(account):
    cau_truy_van = '''Select password
    From QuanLy
    where account = '{}'
    ''' .format(account)
    try:
        reusult = cur.execute(cau_truy_van).fetchone()[0]
        return reusult
    except :
        return None
        
def add_user(id,name,gmail,phone) ->str:
    cau_truy_van = '''Insert into NhanVien
    Values ('{}','{}','{}','{}')
    '''.format(id,name,gmail,phone)
    try:
        result = cur.execute(cau_truy_van)
        con.commit()
        return True
    except Exception as e :
        return e


def show_user_id() -> list :
    cau_truy_van = '''Select id
    From NhanVien'''
    try:
        result =  cur.execute(cau_truy_van)
        return result.fetchall()
    except:
        return None


con, cur = connectDbFile('chamCong.db')

