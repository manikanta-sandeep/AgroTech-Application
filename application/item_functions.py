from .database import db
from .local_time import *


class itemfunctions:

    def some_more(self):
        t=time_calc().time()
        agr = {
    "Grains (A grade) 1880": 1880,
    "Chilli": 7000,
    "Turmeric": 6850,
    "Red Gram": 6000,
    "Green Gram": 7196,
    "Onion": 770,
    "Corn": 1850,
    "Millets": 2150,
    "Sorghum": 2640,
    "Coconut (baal)": 10300,
    "Coconut (Mara)": 9960,
    "Mozambi": 1400,
    "Chana": 5100,
    "Banana": 800,
    "Soyabeans": 3880,
    "Black Gram": 6000,
    "Peanuts": 5275,
    "Sun Flower": 5885,
    "Small Grains": 2500,
    "Sorghum (Hybrid)": 2620,
    "Finger Millet (Ragi)": 3250
}
        for i in agr:
            db.session.execute("insert into item(item_name, item_type_id, item_category, description, joined_time, last_update, immediate) values (:n,:t,:c,:d,:j,:j,:i)",{"n":i,"t":1,"c":0,"d":"Minimum supporting price from the government is "+str(agr[i])+" per quintal","j":t,"i":0})
            db.session.commit()
        return


    def all_items(self):
        a=db.session.execute("select item_name from item")
        a=a.fetchall()
        p=''
        for i in a:
            p+=str(i[0])+', '
        #print(p[:-2])
        return p[:-2]

    def all_item_types(self):
        a=db.session.execute("select type_name from item_type")
        a=a.fetchall()
        p=''
        for i in a:
            p+=str(i[0])+', '
        #print(p[:-2])
        return p[:-2]
    
    def add_an_item(self,details):
        time=time_calc().time()
        db.session.execute("insert into item(item_name, item_type_id, item_category, description, joined_time, last_update, immediate) values (:n, :tid, :c, :d, :t, :l, :i)",{"n":details[0],"tid":details[1], "c":details[2], "d":details[3], "t":time, "l":time, "i":details[4]})
        db.session.commit()
        return

    def all_item_types(self):
        a=db.session.execute("select item_type_id,type_name from item_type")
        a=a.fetchall()
        return a