
# import the mysql and sys modules
import mysql.connector
import sys
import smtplib #used for smtp mail
import getpass #used for getpass method 

# open a database connection
# be sure to change the host IP address, username, password and database name to match your own.Database provided in SIMAS898 github repository.
con = mysql.connector.connect (host = "localhost", user = "root", password = "", db = "fltechnics")

# prepare a cursor object using cursor() method
cursor =  con.cursor ()

# execute the SQL query using execute() method.Join is used in order to return values AIL_NUMBER || MODEL_NUMBER || MODEL_DESCRIPTION || OWNER_COMPANY_NAME || COMPANY_COUNTRY_CODE || COMPANY_COUNTRY_NAME
cursor.execute ("SELECT aircraft.TAIL_NUMBER,model.MODEL_NUMBER,model.DESCRIPTION,companies.COMPANY_NAME,country_codes.CODE,country_codes.COUNTRY_NAME FROM aircraft LEFT JOIN model ON aircraft.MDL_AUTO_KEY = model.MDL_AUTO_KEY left JOIN companies  on aircraft.CMP_OWNER = companies.CMP_AUTO_KEY LEFT JOIN country_codes on country_codes.COC_AUTO_KEY = companies.COC_AUTO_KEY")
       
       
# fetch all of the rows from the query
data = cursor.fetchall ()


# print the rows
for row in data :
 print (row[0],row[1],row[2],row[3],row[4],row[5],'\n','_____________________________________________________________________')


 # this cursor is the same select is above except it has a where statement that returns rows which are not null in companies.COC_AUTO_KEY because without this it is not possible to link the company to any country and this may crash the querry.Companies.SDF_COC_003 set to T in order to return airplanes that are owned by EU companies
cursor.execute (" SELECT aircraft.TAIL_NUMBER,model.MODEL_NUMBER,model.DESCRIPTION,companies.COMPANY_NAME,country_codes.CODE,country_codes.COUNTRY_NAME FROM aircraft LEFT JOIN model ON aircraft.MDL_AUTO_KEY = model.MDL_AUTO_KEY left JOIN companies  on aircraft.CMP_OWNER = companies.CMP_AUTO_KEY LEFT JOIN country_codes on country_codes.COC_AUTO_KEY = companies.COC_AUTO_KEY WHERE companies.COC_AUTO_KEY IS NOT NULL AND country_codes.SDF_COC_003='T'")
print ("Generuojama HTML ataskaita. Prasome palaukti.Ja rasite sio .py failo direktorijoje")
data = cursor.fetchall ()
#html string creates html tags
html = """
<table border=1 bgcolor="#5882FA">
     <tr>
       <th>TAIL_NUMBER</th>
       <th>AIRCRAFT_MODEL</th>
	   <th>MODEL_DESCRIPTION</th>
	   <th>OWNER_COMPANY</th>
	   <th>OWNER_COUNTRY_CODE</th>
	   <th>OWNER_COUNTRY_NAME</th>
     </tr>"""
	 #loop for row in data populates rows within html
for row in data:
    html = html + "<tr>"
	#for col in row populates columns with data
    for col in row:
        html = html + "<td>" + col.replace(" ", "") + "</td>"
    html = html + "</tr>"
html = html + "</table>"
#same sql querry as above but returns nonEU base companies
cursor.execute (" SELECT aircraft.TAIL_NUMBER,model.MODEL_NUMBER,model.DESCRIPTION,companies.COMPANY_NAME,country_codes.CODE,country_codes.COUNTRY_NAME FROM aircraft LEFT JOIN model ON aircraft.MDL_AUTO_KEY = model.MDL_AUTO_KEY left JOIN companies  on aircraft.CMP_OWNER = companies.CMP_AUTO_KEY LEFT JOIN country_codes on country_codes.COC_AUTO_KEY = companies.COC_AUTO_KEY WHERE companies.COC_AUTO_KEY IS NOT NULL AND country_codes.SDF_COC_003='F'")
data = cursor.fetchall ()
#html is generated the same principle as EU companies table
html = html + """
<table border=1 bgcolor="#FE2E2E">
     <tr>
       <th>TAIL_NUMBER</th>
       <th>AIRCRAFT_MODEL</th>
	   <th>MODEL_DESCRIPTION</th>
	   <th>OWNER_COMPANY</th>
	   <th>OWNER_COUNTRY_CODE</th>
	   <th>OWNER_COUNTRY_NAME</th>
     </tr>"""
for row in data:
    html = html + "<tr>"
    for col in row:
        html = html + "<td>" + col.replace(" ", "") + "</td>"
    html = html + "</tr>"
html = html + "</table>"

 #new file is created and it is populated with string from html variable.
with open("AircraftReport.html", "w") as file:
    file.write(html)
	
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
login=input("Kad issiusti kolegai pranesima iveskite savo gmail vartotojo varda iki @ zenklo.\n Taip pat nueikite i https://myaccount.google.com/lesssecureapps ir nustatykite allow less seucre apps i on \n:")
passwordas=getpass.getpass("Suveskite savo gmail slaptazodi.") 
# Authentication 
s.login(login, passwordas) 
rec=input("suveskite gavejo el.pasto adresa:") 

# message to be sent 
message = "Sveiki,\n norime informuoti,kad sugeneruota Lektuvu ataskaita. Del jos galite kreiptis i sio laisko siunteja."

# sending the mail 
s.sendmail(login, rec, message) 
print ("Atlikta")  
# terminating the session 
s.quit() 

con.close()