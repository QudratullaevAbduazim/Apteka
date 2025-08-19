import psycopg2
from prettytable import PrettyTable

conn = psycopg2.connect(
    dbname='apteka',
    user='postgres',
    password='abdu1234',
    host='localhost',
    port='5432'
)

cur = conn.cursor()

class Apteka:
    def dorilar(self):
        cur.execute('select * from dorilar')
        t = PrettyTable()
        t.field_names = [i[0] for i in cur.description]
        t.add_rows([list(i) for i in cur.fetchall()])
        print(t)

    def dorini_qidirish(self, nomi):
        cur.execute(f"select * from dorilar where name = '{nomi}'")
        n = cur.fetchall()
        t = PrettyTable()
        t.field_names = [i[0] for i in cur.description]
        for i in n:
            t.add_row(list(i))
        else:
            if len(n) > 0:
                print(t)
            else:
                print("topilmadi")

    def dori_qoshish(self):
        nom = input("nomi: ")
        narx = int(input("narxi: "))
        son = int(input("soni: "))
        cur.execute(f"insert into dorilar(name, price, quantity) values('{nom}', {narx}, {son})")
        conn.commit()
        print("qoshildi")

    def royxatdan_otish(self, ism):
        cur.execute(f"insert into mijoz(name, total_amount) values('{ism}', 0)")
        conn.commit()

    def dori_sotib_olish(self):
        ism = input("ismingiz: ")
        self.royxatdan_otish(ism)
        jami = 0
        a = True
        while a:
            nom = input("dori nomi (0 - tugatish): ")
            if nom == '0':
                a = False
            else:
                cur.execute(f"select id, price, quantity from dorilar where name = '{nom}'")
                d = cur.fetchone()
                if d:
                    idsi, narx, qoldiq = d
                    miqdor = int(input("nechta: "))
                    if miqdor > qoldiq:
                        print("yoq")
                    else:
                        summa = narx * miqdor
                        jami += summa
                        cur.execute(f"update dorilar set quantity = quantity - {miqdor} where id = {idsi}")
                        print(f"{summa} so'm")
                else:
                    print("topilmadi")
        cur.execute(f"update mijoz set total_amount = {jami} where name = '{ism}'")
        conn.commit()
        print("jami:", jami)

    def menyu(self):
        a = True
        while a:
            print("0 - chiqish\n1 - dorilar\n2 - dorini qidirish\n3 - dori qo‘shish\n4 - dori sotib olish\n5 - ro‘yxatdan o‘tish")
            tanla = input("tanla: ")
            if tanla == '0':
                a = False
            elif tanla == '1':
                self.dorilar()
            elif tanla == '2':
                n = input("nom: ")
                self.dorini_qidirish(n)
            elif tanla == '3':
                self.dori_qoshish()
            elif tanla == '4':
                self.dori_sotib_olish()
            elif tanla == '5':
                ism = input("ismingiz: ")
                self.royxatdan_otish(ism)
            else:
                print("xato")

a = Apteka()
a.menyu()

# man telegram bot larni ham yarata olaman hamda SQl boyicha tushuncham bor albatta hozirda Najot talimda oqiyman mani qilgan loyihalarimni korib chiqing