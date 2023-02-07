from .database import db
from .email import emailTo
from .local_time import *
from base64 import b64encode



class userfunctions:
    def send_mail_to(self,email,subject,msg):
        e=emailTo()
        e.send_email(subject,email,msg)
        return 1


    def send_verification(self,email):
        e=emailTo()
        password=e.generate_password()
        msg=f'''
Hi ,

Thank you for registering your account on Project AgroTech. Hope you will find it easier to use. Here is the verification code, please verify your account with the below verification code.


{password}

Thanks and Regards
Manikanta Sandeep
Team Project AgroTech.
        '''
        userfunctions().new_user(email,password)
        return userfunctions().send_mail_to(email,"Verification code for account creation",msg)
        
    def forgot_send_verification(self,email):
        a=userfunctions().check_username(email)
        if a==-1:
            return -1
        else:
            e=emailTo()
            password=e.generate_password()
            msg=f'''
Hi ,

You are recently requested for resetting your password for your account on Project AgroTech. Here is the verification code, please reset your account password with the below verification code.


{password}

Thanks and Regards
Manikanta Sandeep
Team Project AgroTech.
        '''
            userfunctions().new_user(email,password)
            return userfunctions().send_mail_to(email,"Verification code for Reset Password",msg)
        


    def user_status(self,user_email):
        a=db.session.execute("select password from user where email=:mail",{"mail":user_email})
        no_of_users=a.fetchall()
        if len(no_of_users)==1:
            return 1
        return 0

    def new_user(self,user_email,password):
        join_time=time_calc().time()
        already_present=db.session.execute("select count(*) from user where email=:mail",{"mail":user_email})
        if int(already_present.fetchall()[0][0])==0:
            db.session.execute("insert into user(email,password,created_time) values (:email,:pwd,:time)",{"email":user_email,"pwd":password, "time":join_time})
        else:
            db.session.execute("update user set password=:password where email=:mail",{"mail":user_email,"password":password})
        db.session.commit()
        return

    def check_user(self,user_email,password):
        a = db.session.execute("select password from user where email=:mail",{"mail": user_email})
        fetched_password = list(a.fetchall())
        print(fetched_password)
        #print(fetched_password,password,fetched_password==password)
        if len(fetched_password) != 0:
            f2=list(fetched_password[0])
            if f2[0]== password:
                return 1
            else:
                return 0
        else:
            return 0

    def join_user(self,email,name1,name,dob,password,profile_picture,gender):
        join_time=time_calc().time()
        gender=int(gender)
        #profile_picture=b64encode(profile_picture).decode("utf-8")
        db.session.execute("update user set name=:n, dob=:dob, password=:pwd, profile_picture=:pp, gender=:g, created_time=:jt where email=:mail",{ "mail":email ,"n":name,"pwd":password, "dob":dob, "pp":profile_picture, "g":gender , "jt":join_time})
        db.session.commit()
        return

    def fp_update_password(self,email,password):
        db.session.execute("update user set password=:pwd where email=:mail",{"mail":email,"pwd":password})
        db.session.commit()
        return

    def user_name(self,email):
        a=db.session.execute("select user_id,name from user where email=:mail",{"mail":email})
        u_id_name=list(a.fetchall())
        print(len(u_id_name),"Length")
        return u_id_name

    def account_details(self,user_id):
        a=db.session.execute("select u.user_id, u.email, u.name, u.dob, u.profile_picture, u.gender, u.created_time, u.last_update, u.aadhar, u.phone, u.profile_description from user u  where u.user_id=:uid",{"uid":user_id})
        details=list(a.fetchall())
        #print(len(details))
        if len(details)!=0:
            details=list(details[0])
            if details[4]=='' or details[4]=='None' or details[4]==None or details[4]=="b''" or str(details[4])=="b''":
                details[4]=-1
            else:
                details[4]=b64encode(details[4]).decode("utf-8")
            details[6]=time_calc().convert(details[6])
            return details
        
    def address_details(self,user_id):
        b=db.session.execute("select u.user_id,a.address, a.address2, a.phone, a.district, a.postal_code, c.city, s.state, cu.country from user u, address a, city c, state s, country cu where user_id=:uid and u.address_id=a.address_id and a.city_id=c.city_id and c.state_id=s.state_id and s.country_id=cu.country_id",{"uid":user_id})
        a=b.fetchall()
        a=list(a)
        print(a)
        if len(a)==0:
            #print(0)
            return 0
        else:
            print(1)
            return a[0]


    def follow_details(self,k,code):
        if k==0:
            user_id=userfunctions().get_uid_from_email(code)
        else:
            user_id=code
        following=db.session.execute("select count(*) from follows where follower_id=:id",{"id":user_id})
        followers=db.session.execute("select count(*) from follows where user_id=:id",{"id":user_id})
        posts=db.session.execute("select count(*) from blogs where user_id=:id",{"id":user_id})
        followers,following,posts=followers.fetchall()[0][0],following.fetchall()[0][0],posts.fetchall()[0][0]
        return [followers,following,posts]



    def delete_account(self,email):
        db.session.execute("delete from user where email=:mail",{"mail":email})
        db.session.commit()
        return

    def update_profile(self,email,n,dob,g,pp,a,m,pd,r):
        w=db.session.execute("select email,name,dob,gender,profile_picture,aadhar,phone, profile_description,role from user where email=:mail",{"mail":email})
        old_data=w.fetchall()[0]
        t=time_calc().time()
        if n!='':
            n1=n
        else:
            n1=old_data[1]
        if dob!='':
            dob1=dob
        else:
            dob1=old_data[2]
        if g!='':
            g1=g
        else:
            g1=old_data[3]
        #print(pp)
        if pp=="" or str(pp)=="b''" or str(pp)=='':
            pp1=old_data[4]
        else:
            pp1=pp
        if a!='':
            a1=a
        else:
            a1=old_data[5]
        if m!='':
            m1=m
        else:
            m1=old_data[6]
        if pd!='':
            pd1=pd
        else:
            pd1=old_data[7]
        if r!='':
            r1=r
        else:
            r1=old_data[8]
            
        #print(old_data[1:])
        #print(un,n,dob,g,pp)
        #print(un1,n1,dob1,g1,pp1)
        db.session.execute("update user set name=:n, dob=:dob, gender=:g, profile_picture=:pp,aadhar=:a,phone=:p,last_update=:l, profile_description=:pd, role=:r  where email=:mail",{"mail":email,"pd":pd1,"r":r1,"n":n1,"dob":dob1,"g":g1,"pp":pp1,"a":a1,"p":m1,"l":t})
        db.session.commit()
        return n1

    

    def check_username(self,email):
        a=db.session.execute("select name,password, user_id, email, gender from user where email=:mail",{"mail": email})
        a=list(a.fetchall())
        #print(a)
        if len(a)==0:
            return -1
        return list(a[0])

    def modify_account(self,email,name,dob,gender,pp):
        old=db.session.execute("select dob,profile_picture,user_id from user where email=:mail",{"mail":email})
        old=old.fetchall()[0]
        if dob=='-1':
            dob=old[0]
        if pp=="" or str(pp)=="b''":
            pp=old[1]
        db.session.execute("update user set name=:n, dob=:dob, gender=:g, profile_picture=:pp where user_id=:id",{"id":old[2],"n":name, "dob":dob,"g":gender, "pp":pp})
        db.session.commit()
        return old[2]


    def u_details(self,uid):
        d=db.session.execute("select u.email,u.name,u.dob,u.gender,u.profile_picture,u.aadhar,u.phone, u.profile_description,r.role_name from user u, roles r where u.role=r.role_id and user_id=:uid",{"uid":uid})    
        d=d.fetchall()[0]
        d=list(d)
        if d[4]=='' or d[4]=='None' or d[4]==None or d[4]=="b''" or str(d[4])=="b''":
            d[4]=-1
        else:
            d[4]=b64encode(d[4]).decode("utf-8")
        return d

    def u_details(self,uid):
        d=db.session.execute("select u.email,u.name,u.dob,u.gender,u.profile_picture,u.aadhar,u.phone, u.profile_description,r.role_name from user u, roles r where u.role=r.role_id and user_id=:uid",{"uid":uid})    
        d=d.fetchall()[0]
        d=list(d)
        if d[4]=='' or d[4]=='None' or d[4]==None or d[4]=="b''" or str(d[4])=="b''":
            d[4]=-1
        else:
            d[4]=b64encode(d[4]).decode("utf-8")
        return d

    def all_details(self,uid):
        d=db.session.execute("select u.email,u.name,u.dob,u.gender,u.profile_picture,u.aadhar,u.phone, u.profile_description,r.role_name from user u, roles r where u.role=r.role_id and user_id=:uid",{"uid":uid})    
        d=d.fetchall()[0]
        d=list(d)
        if d[4]=='' or d[4]=='None' or d[4]==None or d[4]=="b''" or str(d[4])=="b''":
            d[4]=-1
        else:
            d[4]=b64encode(d[4]).decode("utf-8")
        return d

    
    def get_username(self, uid):
        u=db.session.execute("select name from user where user_id=:uid",{"uid":uid})
        u=u.fetchall()
        u=u[0][0]
        #print(u)
        return u