from .database import db
from .local_time import *
from base64 import b64encode


class inventoryfunctions:
    def add_inventory(self,l,user_id,k,iid):
        t=time_calc().time()
        if k==0:
            db.session.execute('insert into inventory(user_id, item_id, price_per_unit, address, due, picture, description, joined_time, last_updated, view, measured_in, quantity_added, quanity_sold, quantity_remaining, quantity_last_updated, transport_req, process_req, verified) values(:uid, :i, :price, :a, :d, :p, :pd, :t, :t, :v, :q, :qu, 0, :qu, :t, :tr, :pr, :ver)',{"uid":user_id, "i":l[0], "price":l[1], "a":l[2], "d":l[3], "p":l[4], "pd":l[5], "t":t, "v":l[6], "q":l[7], "qu":l[8], "tr":l[9], "pr":l[10], "ver":0})
        else:
            o=db.session.execute("select user_id, item_id, price_per_unit, address, due, picture, description, joined_time, last_updated, view, measured_in, quantity_added, quanity_sold, quantity_remaining, quantity_last_updated, transport_req, process_req, verified from inventory where inventory_id=:iid",{"iid":iid})
            old_data=list(o.fetchall()[0])
            print(old_data)
            if l[1]!='':
                l[1]=l[1]
            else:
                l[1]=old_data[2]

            if l[3]!='':
                l[3]=l[3]
            else:
                l[3]=old_data[4]

            if l[4]!='':
                l[4]=l[4]
            else:
                l[4]=old_data[5]

            if l[5]!='':
                l[5]=l[5]
            else:
                l[5]=old_data[6]

            if l[6]!='':
                l[6]=l[6]
            else:
                l[6]=old_data[9]

            if l[7]!='':
                l[7]=l[7]
            else:
                l[7]=old_data[10]
            
            if l[8]!='':
                l[8]=l[8]
                p=0
            else:
                l[8]=old_data[11]
                p=1

            if l[9]!='':
                l[9]=l[9]
            else:
                l[9]=old_data[15]

            if l[10]!='':
                l[10]=l[10]
            else:
                l[10]=old_data[16]

            if p==0:
                db.session.execute('update inventory set price_per_unit=:price, due=:d, picture=:p, description=:pd, last_updated=:t, view=:v, measured_in=:q, quantity_added=quantity_added+:qu, quantity_remaining=quantity_remaining+:qu, quantity_last_updated=:t, transport_req=:tr, process_req=:pr where inventory_id=:iid',{"uid":user_id, "i":l[0], "price":l[1], "a":l[2], "d":l[3], "p":l[4], "pd":l[5], "t":t, "v":l[6], "q":l[7], "qu":l[8], "tr":l[9], "pr":l[10], "iid":iid})
            else:
                db.session.execute('update inventory set price_per_unit=:price, due=:d, picture=:p, description=:pd, last_updated=:t, view=:v, measured_in=:q, transport_req=:tr, process_req=:pr where inventory_id=:iid',{"uid":user_id, "i":l[0], "price":l[1], "a":l[2], "d":l[3], "p":l[4], "pd":l[5], "t":t, "v":l[6], "q":l[7], "qu":l[8], "tr":l[9], "pr":l[10], "iid":iid})
        db.session.commit()
        return

    def all_inventories(self, uid):
        d=db.session.execute("select i.picture, it.item_name, i.description, it.description, i.price_per_unit, i.quantity_remaining, i.user_id, i.inventory_id, i.view, i.joined_time from inventory i, item it where i.item_id=it.item_id and i.user_id=:uid",{"uid":uid})
        d=list(d.fetchall())
        l=[]
        for i in d:
            temp=list(i)
            if temp[0]=='' or temp[0]=='None' or temp[0]==None or temp[0]=="b''" or str(temp[0])=="b''":
                temp[0]=-1
            else:
                temp[0]=b64encode(temp[0]).decode("utf-8")
            l+=[temp]
        #print(l)
        return l

    def buy_inventories(self, uid):
        d=db.session.execute("select i.picture, it.item_name, i.description, it.description, i.price_per_unit, i.quantity_remaining, i.user_id, i.inventory_id,i.joined_time from inventory i, item it where i.item_id=it.item_id and i.view=1 and i.user_id!=:uid",{"uid":uid})
        d=list(d.fetchall())
        print(len(d))
        l=[]
        for i in d:
            temp=list(i)
            print(uid)
            print(temp[1:])
            if temp[0]=='' or temp[0]=='None' or temp[0]==None or temp[0]=="b''" or str(temp[0])=="b''":
                temp[0]=-1
            else:
                temp[0]=b64encode(temp[0]).decode("utf-8")
            l+=[temp]
        #print(l)
        return l

    def pr_details(self,iid):
        d=db.session.execute("select i.user_id, it.item_name, i.price_per_unit, i.address, i.due, i.picture, i.description, i.joined_time, i.last_updated, i.view, u.unit_name, i.quantity_added, i.quanity_sold, i.quantity_remaining, i.quantity_last_updated, i.transport_req, i.process_req, i.verified, i.view, i.inventory_id from inventory i, item it, units u where i.item_id=it.item_id and i.measured_in=u.unit_id and inventory_id=:iid",{"iid":iid})
        d=d.fetchall()
        if len(d)==0:
            return []
        d=d[0]
        d=list(d)
        if d[5]=='' or d[5]=='None' or d[5]==None or d[5]=="b''" or str(d[5])=="b''":
            d[5]=-1
        else:
            d[5]=b64encode(d[5]).decode("utf-8")

        return d
    def p_details(self,iid):
        d=db.session.execute("select i.user_id, it.item_name, i.price_per_unit, i.address, i.due, i.picture, i.description, i.joined_time, i.last_updated, i.view, u.unit_name, i.quantity_added, i.quanity_sold, i.quantity_remaining, i.quantity_last_updated, i.transport_req, i.process_req, i.verified, i.view, i.inventory_id from inventory i, item it, units u where i.item_id=it.item_id and i.measured_in=u.unit_id and inventory_id=:iid",{"iid":iid})
        d=d.fetchall()
        if len(d)==0:
            return []
        d=d[0]
        d=list(d)
        if d[5]=='' or d[5]=='None' or d[5]==None or d[5]=="b''" or str(d[5])=="b''":
            d[5]=-1
        else:
            d[5]=b64encode(d[5]).decode("utf-8")

        return d
    
    def update_view(self,iid):
        v=db.session.execute("select view from inventory where inventory_id=:iid",{"iid":iid})
        if list(v.fetchall()[0])[0]==0:
            val=1
        else:
            val=0                
        db.session.execute("update inventory set view=:val where inventory_id=:iid",{"iid":iid,"val":val})
        db.session.commit()
        return 
        
    def order_details(self,iid):
        d=db.session.execute("select i.user_id, it.item_name, i.price_per_unit, i.address, i.due, i.picture, i.description, i.joined_time, i.last_updated, i.view, u.unit_name, i.quantity_added, i.quanity_sold, i.quantity_remaining, i.quantity_last_updated, i.transport_req, i.process_req, i.verified, i.view, i.inventory_id from inventory i, item it, units u where i.item_id=it.item_id and i.measured_in=u.unit_id and inventory_id=:iid",{"iid":iid})
        d=d.fetchall()[0]
        d=list(d)
        if d[5]=='' or d[5]=='None' or d[5]==None or d[5]=="b''" or str(d[5])=="b''":
            d[5]=-1
        else:
            d[5]=b64encode(d[5]).decode("utf-8")

        return d

    def update_inventory_details(self,iid):
        invd=db.session.execute("select i.user_id, it.item_id, i.price_per_unit, i.address, i.due, i.picture, i.description, i.joined_time, i.last_updated, i.view, i.measured_in, i.quantity_added, i.quanity_sold, i.quantity_remaining, i.quantity_last_updated, i.transport_req, i.process_req, i.verified,it.item_name,u.unit_name,i.inventory_id from inventory i, item it, units u where u.unit_id=i.measured_in and i.item_id=it.item_id and inventory_id=:iid",{"iid":iid})
        d=invd.fetchall()
        d=list(d[0])
        
        return d


        