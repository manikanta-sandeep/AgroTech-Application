from flask import render_template, redirect, request, session
from flask import current_app as app
from .database import db 

from .userfunctions import *
from .update import *
from .role_functions import *
from .item_functions import *
from .address_functions import *
from .inventory_functions import *
from .clocation import *
from .analysis import *
from .order_functions import *
from .graphs import *


@app.route("/", methods=["GET","POST"])
def index_page():
    db.session.execute("select * from user")
    if request.method=="GET":
        return render_template("index_page.html")
    else:
        return render_template("index_page.html")


@app.route("/login",methods=["GET","POST"])
def login_page():
    session.clear()
    db.session.commit()
    session['user_id']=None
    session["email"]=None
    session["username"]=None
    session["on"]=1
    if request.method=="POST" or request.method=="GET":
        return render_template("login.html",option=1,invalid=0)

@app.route("/create_account/send_verification",methods=["GET","POST"])
def create_account():
    if request.method=="GET":
        return render_template("login.html",option=5, invalid=0)

@app.route("/create_account/verify_code", methods=["GET","POST"])
def verify_code():
    if request.method=="POST":
        session["email"]=request.form["email"]
        uf=userfunctions()
        if uf.user_status(session["email"])==1:
            return render_template("login.html", option=8, key=1)
        else:
            uf.send_verification(session["email"])
            return render_template("login.html",option=6,inavlid=0)


@app.route("/create_account/check_code", methods=["GET","POST"])
def check_code():
    if request.method=="POST":
        passcode=request.form["verification_code"]
        uf=userfunctions()
        if uf.check_user(session["email"],passcode)==1:
            #continuing to creating account
            return render_template("login.html",option=7, mail=session["email"], invalid=0 )
        else:
            #redirecting to enter verification code correctly
            return render_template("login.html",option=6, invalid=1)

@app.route("/account_created", methods=["GET","POST"])
def account_created():
    #(username,name,dob,pp,p,cp,g)
    l=[request.form["name"],request.form["name"], request.form["dob"], request.files["profile_picture"].read(), request.form["password"], request.form["confirm_password"], request.form["flexRadioDefault"]]  
    uf=userfunctions()
    
    if l[4]==l[5]:
        uf.join_user(session["email"],l[0],l[1],l[2],l[4],l[3],l[6])
        return render_template("index_page.html",option=8)
    else:
        return render_template("index_page.html",option=7,invalid=1)
            
@app.route("/forgot_password",methods=["GET","POST"])
def forgot_password():
    if request.method=="GET":
        return render_template("login.html",option=2)

@app.route("/forgot_password/verify_code", methods=["GET","POST"])
def fp_send_verification():
    if request.method=="POST":
        mail=request.form["email"]
        session["email"]=mail
        uf=userfunctions()
        code=uf.forgot_send_verification(mail)
        if code==-1:
            return render_template("login.html",option=2,invalid=1)
        else:
            return render_template("login.html",option=3,invalid=0)
        

@app.route("/forgot_password/check_code", methods=["GET","POST"])
def fp_verify_code():
    if request.method=="POST":
        passcode=request.form["verification_code"]
        uf=userfunctions()
        if uf.check_user(session["email"],passcode)==1:
            #continue to resetting password
            return render_template("login.html",option=9, invalid=0)
            
        else:
            #verification code not matched 
            return render_template("login.html",option=3, inavlid=1)
            
@app.route("/forgot_password/check_password",methods=["GET","POST"])
def check_rp_password():
    if request.method=="POST":
        p=request.form["password"]
        cp=request.form["confirm_password"]
        if p==cp:
            uf=userfunctions()
            uf.fp_update_password(session["email"],p)
            session.clear()
            return render_template("login.html",option=4,invalid=0)
            #update password
        else:
            return render_template("login.html",option=9, invalid=1)



@app.route("/check", methods=["GET","POST"])
def check_login():
    print(request.method)
    if request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        a=userfunctions().check_username(email)
        if a==-1:
            print("value of a",a)
            return render_template("login.html",option=1, invalid=1, nr=1)
        else:
            print("value of a",a)
            if a[1]==password:
                session["email"]=email
                if a[0]==None:
                    return render_template("login.html",option=7, key=1, data=a)
                else:
                    session["user_id"]=a[2]
                    session["username"]=a[0]
                    return redirect("/home")
            else:
                return render_template("login.html",option=1, invalid=1) 



@app.route("/account_modified", methods=["GET","POST"])
def account_modified():
    if session["on"]!=1:
        return redirect("/login")
    if request.method=="POST":
        email=session["email"]
        name=request.form["name"]
        dob=request.form["dob"]
        gender=request.form["flexRadioDefault"]
        pp=request.files["profile_picture"].read()
        session["user_id"]=userfunctions().modify_account(session["email"],name,dob,gender,pp)
        session["username"]=name
        session["on"]=1
        return redirect("/home")



@app.route("/logout", methods=["GET","POST"])
def logout():
    session.clear()
    return redirect("/login") 


@app.route("/home", methods=["GET","POST"])
def home():
    return render_template("home.html", option=1, un=session['username'])



@app.route("/dashboard", methods=["GET","POST"])
def menu():
    return render_template("dashboard.html", un=session['username'], option=1)


@app.route("/settings", methods=["GET","POST"])
def settings():
    return render_template("home.html",option=2, un=session['username'])


@app.route("/settings/add_a_role", methods=["GET", "POST"])
def add_role():
    roles=rolefunctions().allroles()
    return render_template("home.html", option=3, key=0, un=session['username'], roles=roles)

@app.route("/settings/update_role", methods=["GET", "POST"])
def update_role():
    role_name=request.form['role_name']
    k=update().insert_role(role_name)
    if k:
        m=role_name+" role added successfully"
    else:
        m="Error: "+role_name+"role has not been added!"
    return render_template("home.html", option=4, msg=m,k=k, key=0,un=session['username'])

@app.route("/add_an_item", methods=["GET","POST"])
def add_item():
    items=itemfunctions().all_items()
    item_types=itemfunctions().all_item_types()
    return render_template("home.html", option=5, types=items,type2=item_types ,un=session['username'])

@app.route("/update_item", methods=["GET","POST"])
def update_item():
    msg="Item has been added successfully."
    details=[request.form['item_name'],request.form['type_id'],request.form['category'],request.form['description'],request.form['immediate']]
    itemfunctions().add_an_item(details)
    return render_template("home.html", option=4, msg=msg, k=1, un=session['username'])


@app.route("/settings/add_a_item_type", methods=["GET","POST"])
def add_item_type():
    items=itemfunctions().all_item_types()
    return render_template("home.html", option=3, key=1, un=session['username'], roles=items)

@app.route("/settings/add_item_type_name", methods=["GET","POST"])
def add_type_name():
    role_name=request.form['role_name']
    k=update().insert_item_type(role_name)
    if k:
        m=role_name+" item type added successfully"
    else:
        m="Error: "+role_name+" item type has not been added!"
    return render_template("home.html", option=4, msg=m,k=k, key=1, un=session['username'])

@app.route("/update_account", methods=["GET","POST"])
def update_account():
    d=addressfunctions().all()
    user_details=userfunctions().account_details(session["user_id"])
    address_details=userfunctions().address_details(session["user_id"])
    if address_details==0:
        key=0
    else:
        key=1
    return render_template("home.html",option=6, d=d,key=key,data=user_details, a_data=address_details, un=session['username'])

@app.route("/update_account/update", methods=["GET","POST"])
def account_update():
    #print(request.form.keys)
        
    n=request.form['name']
    dob=request.form["dob"]
    a=request.form['a_number']
    m=request.form['m_number']
    g=int(request.form["flexRadioDefault"])
    pp=request.files["profile_picture"].read()
    pd=request.form['p_description']
    r=request.form['role']

    userfunctions().update_profile(session['email'],n,dob,g,pp,a,m,pd,r)

    am=request.form['am_number']
    a1=request.form['address1']
    a2=request.form['address2'] 
    
    z=request.form['zip']
    d=request.form['district']
    city=request.form['city']


    address_details=userfunctions().address_details(session["user_id"])
    if address_details==0:
        key=0
        addressfunctions().add_address([a1,a2,d,city,z,am],session['user_id'],0,0)
    else:
        key=1
        addressfunctions().update_address(a1,a2,d,city,z,am,session['user_id'],k=0)

    session['username']=userfunctions().get_username(session['user_id'])

    return redirect("/settings")



@app.route("/dashboard/buy_a_product",methods=["GET","POST"])
def buy_a_product():
    data=inventoryfunctions().buy_inventories(session['user_id'])
    #print(data)
    #print(session['user_id'])
    return render_template("dashboard.html",un=session['username'],data=data, option=3,  sid=session['user_id'])



@app.route("/dashboard/sell_a_product",methods=["GET","POST"])
def sell_a_product():
    data=inventoryfunctions().all_inventories(session['user_id'])
    return render_template("dashboard.html",un=session['username'], data=data, option=2, sid=session['user_id'])


@app.route("/dashboard/transport_a_product",methods=["GET","POST"])
def transport_a_product():
    td=orderfunctions().transport_details(session['user_id'])
    return render_template("dashboard.html",un=session['username'], option=5, key=1, td=td)



@app.route("/dashboard/process_a_product",methods=["GET","POST"])
def process_a_product():
    td=orderfunctions().transport_details(session['user_id'])
    return render_template("dashboard.html",un=session['username'], option=5,key=2, td=td)



@app.route("/dashboard/verify_a_product",methods=["GET","POST"])
def verify_a_product():
    td=orderfunctions().transport_details(session['user_id'])
    return render_template("dashboard.html",un=session['username'], option=5,key=3, td=td)


@app.route("/make_an_inventory",methods=["GET","POST"])
def make_an_inventory():
    ad=addressfunctions().all()
    od=addressfunctions().all2()
    return render_template("home.html",un=session['username'], option=7, items=od[0], units=od[1], d=ad)


@app.route("/make_an_inventory/update", methods=["GET","POST"])
def inventory_add():
    i=request.form['item']
    p=request.files['inventory_picture'].read()
    pd=request.form['p_description']
    d=request.form['due_d']
    v=request.form['view']
    q=request.form['unit']
    quant=request.form['quantity']
    price=request.form['price']
    tr=request.form['transport']
    pr=request.form['process']

    am=request.form['am_number']
    a1=request.form['address1']
    a2=request.form['address2'] 
    
    z=request.form['zip']
    di=request.form['district']
    city=request.form['city']
    aid=addressfunctions().add_address([a1,a2,di,city,z,am],session['user_id'],0,0)

    inventoryfunctions().add_inventory([i,price,aid,d,p,pd,v,q,quant,tr,pr],session['user_id'],0,0)

    m="Inventory has been added successfully!"
    return render_template("home.html", option=4, msg=m,k=1, key=-1, un=session['username'])


@app.route("/view_product/<iid>", methods=["GET","POST"])
def view(iid):
    p_details=inventoryfunctions().pr_details(int(iid))
    #print(p_details[0])
    u_details=userfunctions().u_details(p_details[0])
    #print(p_details[-5:])
    return render_template("dashboard.html",un=session['username'], sid=session['user_id'], option=4, pd=p_details, ud=u_details)


@app.route("/location", methods=["GET", "POST"])
def locate():
    d=locat().current_location()
    return redirect("/home")


@app.route("/account", methods=["GET","POST"])
def account():
    
    #print(db.session.query(order.user_id).all())
    user_details=userfunctions().account_details(session["user_id"])
    address_details=userfunctions().address_details(session["user_id"])
    return render_template("home.html",option=8, data=user_details, a_data=address_details, un=session['username'])

@app.route("/update_view", methods=["GET","POST"])
def upd_view():
    iid=request.form["mv"]
    inventoryfunctions().update_view(int(iid))
    return redirect('/view_product/'+str(iid))


@app.route("/make_an_order/<iid>", methods=["GET","POST"])
def make_an_order(iid):
    ad=addressfunctions().all()
    od=addressfunctions().all2()
    inv=inventoryfunctions().pr_details(int(iid))
    return render_template("home.html", option=9, un=session["username"],items=od[0], units=od[1], d=ad, pd=inv )


@app.route("/make_an_order/update", methods=["GET","POST"])
def insert_order():
    iid=request.form["mp"]
    d=request.form["p_description"]
    q=request.form["quantity"]
    orderfunctions().make_an_order(session["user_id"],int(iid),d,int(q))

    return redirect("/dashboard")


@app.route("/view_order/<oid>",methods=["GET","POST"])
def view_order(oid):
    td=orderfunctions().order_details(int(oid))
    return render_template("dashboard.html",un=session['username'], option=6, pd=td)


@app.route("/add_to_cart", methods=["GET","POST"])
def add_to_cart():

    pass

@app.route("/edit_an_inventory/<iid>", methods=["GET","POST"])
def edit_inventory(iid):
    add=addressfunctions().all()
    od=addressfunctions().all2()
    pd=inventoryfunctions().update_inventory_details(int(iid))
    ad=addressfunctions().t_address(pd[3])
    return render_template("home.html", option=10, un=session['username'], nd=pd, ad=ad, items=od[0], units=od[1], d=add)

@app.route("/edit_an_inventory/update/<iid>", methods=["GET","POST"])
def update_inventory(iid):
    i=request.form['item']
    p=request.files['inventory_picture'].read()
    pd=request.form['p_description']
    d=request.form['due_d']
    v=request.form['view']
    q=request.form['unit']
    quant=request.form['quantity']
    price=request.form['price']
    tr=request.form['transport']
    pr=request.form['process']

    am=request.form['am_number']
    a1=request.form['address1']
    a2=request.form['address2'] 
    
    z=request.form['zip']
    di=request.form['district']
    city=request.form['city']


    aid=addressfunctions().add_address([a1,a2,di,city,z,am],session['user_id'],1,iid)

    inventoryfunctions().add_inventory([i,price,aid,d,p,pd,v,q,quant,tr,pr],session['user_id'],1,iid)


    return redirect("/edit_an_inventory/"+str(iid))





@app.route("/view_my_orders", methods=["GET","POST"])
def view_my_orders():
    td=orderfunctions().my_order_details(session['user_id'])
    return render_template("dashboard.html",un=session['username'], option=5,key=4, td=td)

@app.route("/sales_of_my_products", methods=["GET","POST"])
def make_process():
    td=orderfunctions().my_sales_details(session['user_id'])
    return render_template("dashboard.html",un=session['username'], option=5,key=5, td=td)




@app.route("/view_sales/<oid>",methods=["GET","POST"])
def view_sales(oid):
    td=orderfunctions().order_details(int(oid))
    return render_template("dashboard.html",un=session['username'], option=6,key=1, pd=td)



@app.route("/sales_analysis",methods=["GET","POST"])
def analysis_sales():
    graphs().draw_graphs_of(session["user_id"])
    return render_template("dashboard.html",un=session['username'], option=7)



@app.route("/dashboard/manage_inventory",methods=["GET","POST"])
def manage_inventory():
    data=inventoryfunctions().all_inventories(session['user_id'])
    return render_template("dashboard.html",un=session['username'], data=data, option=2, key=1, sid=session['user_id'])
