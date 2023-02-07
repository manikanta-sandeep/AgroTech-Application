from .database import db
from .local_time import *
from .models import order, inventory, item, user
from base64 import b64encode



class orderfunctions:
    def make_an_order(self,uid,iid,pd,q):
        t=time_calc().time()

        new=order(user_id=uid,inventory_id=iid,description=pd, quantity_required=q,status=1,discount=1,ordered_time=t,last_updated=t)    
        db.session.add(new)
        db.session.commit()
        db.session.execute("update inventory set quanity_sold=quanity_sold+:q, quantity_remaining=quantity_remaining-:q, quantity_last_updated=:t where inventory_id=:iid",{"iid":iid,"q":q,"t":t,})
        db.session.commit()
        return

    def transport_details(self,uid):
        a=order.query.filter(order.user_id!=uid).all()
        c=[]
        for i in a:
            j=inventory.query.filter(inventory.inventory_id==i.inventory_id).one()
            if j.picture=='' or j.picture=='None' or j.picture==None or j.picture=="b''" or str(j.picture)=="b''":
                k=-1
            else:
                k=b64encode(j.picture).decode("utf-8")
            
            l=item.query.filter(item.item_id==j.item_id).one()

            u=user.query.filter(user.user_id==i.user_id).one()
            c+=[[i.order_id,i.user_id,u.name,k,l.item_name,i.inventory_id,i.quantity_required,i.ordered_time,i.description,j.description]]
        return c

    def my_order_details(self,uid):
        print(uid)
        a=order.query.filter(order.user_id==uid).all()
        c=[]
        for i in a:
            j=inventory.query.filter(inventory.inventory_id==i.inventory_id).one()
            if j.picture=='' or j.picture=='None' or j.picture==None or j.picture=="b''" or str(j.picture)=="b''":
                k=-1
            else:
                k=b64encode(j.picture).decode("utf-8")
            
            l=item.query.filter(item.item_id==j.item_id).one()

            u=user.query.filter(user.user_id==i.user_id).one()
            c+=[[i.order_id,i.user_id,u.name,k,l.item_name,i.inventory_id,i.quantity_required,i.ordered_time,i.description,j.description]]
        print(c)
        return c

    def order_details(self,oid):
        i=order.query.filter(order.order_id==oid).one()
        c=[]
        j=inventory.query.filter(inventory.inventory_id==i.inventory_id).one()
        if j.picture=='' or j.picture=='None' or j.picture==None or j.picture=="b''" or str(j.picture)=="b''":
            k=-1
        else:
            k=b64encode(j.picture).decode("utf-8")
        
        l=item.query.filter(item.item_id==j.item_id).one()

        u=user.query.filter(user.user_id==i.user_id).one()
        if u.profile_picture=='' or u.profile_picture=='None' or u.profile_picture==None or u.profile_picture=="b''" or str(u.profile_picture)=="b''":
            p=-1
        else:
            p=b64encode(u.profile_picture).decode("utf-8")
        
        c+=[i.order_id,i.user_id,u.name,k,l.item_name,i.inventory_id,i.quantity_required,i.ordered_time,i.description,j.description,u.email,u.name,u.dob,u.gender,p,u.profile_description]
        return c

    def my_sales_details(self,uid):
        inv_l=db.session.execute("select inventory_id from inventory where user_id=:uid",{"uid":uid})
        e=inv_l.fetchall()
        p=[]
        if len(e)!=0:
            for i in e:
                p+=[i[0]]
        a=order.query.filter(order.inventory_id.in_(p)).all()
        c=[]
        for i in a:
            j=inventory.query.filter(inventory.inventory_id==i.inventory_id).one()
            if j.picture=='' or j.picture=='None' or j.picture==None or j.picture=="b''" or str(j.picture)=="b''":
                k=-1
            else:
                k=b64encode(j.picture).decode("utf-8")
            
            l=item.query.filter(item.item_id==j.item_id).one()

            u=user.query.filter(user.user_id==i.user_id).one()
            c+=[[i.order_id,i.user_id,u.name,k,l.item_name,i.inventory_id,i.quantity_required,i.ordered_time,i.description,j.description]]
        return c