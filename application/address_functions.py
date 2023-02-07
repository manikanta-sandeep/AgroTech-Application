from .database import db 
from .local_time import *




class addressfunctions:
    def delete_countries(self):
        db.session.execute("delete from city")
        db.session.commit()
        return

    def add_roles(self):
        l=['gram(g)', 'kilogram(kg)', 'tonne(t)', 'unit(u)','pound(lb)', 'ounce(oz)', 'kilometer(km)', 'hectometer(hm)', 'decameter(dam)', 'meter(m)', 'decimeter(dm)', 'centimeter(cm)','millimeter(mm)']
        for i in l:
            db.session.execute('insert into units(unit_name) values (:i)',{"i":i})
            db.session.commit()
        return

    def add_country(self):
        a=['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
        for i in a:
            t=time_calc().time()
            db.session.execute("insert into country(country, last_update) values (:n,:t)",{"n":i,"t":t})
            db.session.commit()
        return

    def add_states(self):
        a=['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Daman and Diu', 'Delhi', 'Dadra and Nagar Haveli', 'Goa', 'Gujarat', 'Himachal Pradesh', 'Haryana', 'Jharkhand', 'Jammu and Kashmir', 'Karnataka', 'Kerala', 'Lakshadweep', 'Maharashtra', 'Meghalaya', 'Manipur', 'Madhya Pradesh', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Puducherry', 'Rajasthan', 'Sikkim', 'Telangana', 'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
        for i in a:
            t=time_calc().time()
            db.session.execute("insert into state(state,country_id,last_update) values(:s,103,:t)",{"s":i,"t":t})
            db.session.commit()
        return

    def all(self):
        co=db.session.execute('select country_id,country from country')
        c=db.session.execute('select city_id,city from city')
        s=db.session.execute('select state_id,state from state')
        r=db.session.execute('select role_id,role_name from roles')
        co,c,s,r=co.fetchall(),c.fetchall(),s.fetchall(),r.fetchall()
        #print(co,c,s,r)
        return [co,c,s,r]

    def add_address(self,a,uid,k,iid):
        t=time_calc().time()
        if k==0:
            db.session.execute('insert into address(address, address2, district, city_id, postal_code, phone, last_update) values(:a,:a2,:d,:cid,:p,:phn,:l)',{"a":a[0],"a2":a[1],"d":a[2],"cid":a[3],"p":a[4],"phn":a[5],"l":t})
            db.session.commit()
            a=db.session.execute('select address_id from address where last_update=:t',{"t":t})
            a=a.fetchall()
            aid=a[0][0]
            db.session.execute('update user set address_id=:aid where user_id=:uid',{"uid":uid,"aid":aid})
            db.session.commit()
        else:
            r=db.session.execute('select address from inventory where inventory_id=:iid',{"iid":iid})
            r=r.fetchall()
            aid=r[0][0]
            o=db.session.execute('select address, address2, district, city_id, postal_code, phone, last_update from address where address_id=:aid',{"aid":aid})
            old_data=o.fetchall()[0]
            if a[1]!='':
                a[1]=a[1]
            else:
                a[1]=old_data[1]
            if a[2]!='':
                a[2]=a[2]
            else:
                a[2]=old_data[2]

            if a[3]!='':
                a[3]=a[3]
            else:
                a[3]=old_data[3]
            if a[4]!='':
                a[4]=a[4]
            else:
                a[4]=old_data[4]

            if a[0]!='':
                a[0]=a[0]
            else:
                a[0]=old_data[0]

            if a[5]!='':
                a[5]=a[5]
            else:
                a[5]=old_data[5]
            print(aid)
            db.session.execute('update address set address=:a, address2=:a2, district=:d, city_id=:cid, postal_code=:p, phone=:phn, last_update=:l where address_id=:aid',{"a":a[0],"a2":a[1],"d":a[2],"cid":a[3],"p":a[4],"phn":a[5],"l":t,"aid":aid})
            db.session.commit()
        
        return aid

    def update_address(self,a1,a2,d,city,z,am,uid):
        a=db.session.execute('select a.address, a.address2, a.district, a.city_id, a.postal_code, a.phone, a.last_update,a.address_id from user u, address a where a.address_id=u.address_id and u.user_id=:id',{"id":uid})
        old_data=a.fetchall()[0]
        t=time_calc().time()
        if a1!='':
            a11=a1
        else:
            a11=old_data[0]
        if a2!='':
            a21=a2
        else:
            a21=old_data[1]
        if d!='':
            d1=d
        else:
            d1=old_data[2]
        if city!='':
            city1=city
        else:
            city1=old_data[3]
        if z!='':
            z1=z
        else:
            z1=old_data[4]
        if am!='':
            am1=am
        else:
            am1=old_data[5]
        
        db.session.execute("update address set address=:a1, address2=:a2, district=:d, city_id=:c, postal_code=:p, phone=:ph, last_update=:t where address_id=:aid",{"a1":a11,"a2":a21,"p":z1,"ph":am1,"c":city1,"d":d1,"t":t,"aid":old_data[7]})
        db.session.commit()
        return

    def all2(self):
        i=db.session.execute("select item_id, item_name from item")
        u=db.session.execute("select unit_id, unit_name from units")
        i,u=i.fetchall(),u.fetchall()
        return [i,u]

    def t_address(self, address_id):
        d=db.session.execute("select a.address,a.address2,a.district,a.city_id,c.city,c.state_id,s.state,s.country_id,co.country,a.postal_code,a.phone,a.last_update from address a, city c, country co, state s where a.city_id=c.city_id and c.state_id=s.state_id and s.country_id=co.country_id and a.address_id=:aid",{"aid":address_id})
        d=d.fetchall()
        d=list(d[0])
        #print(address_id,d)
        return d