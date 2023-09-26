import imaplib,email,getpass,os,sys

# CHANGE USERNAME AND PASSWORD HERE
user = "blabla@bla.com"
pwd = "WriteYourPasswordHere"
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)

# CHANGE DIRECTORY AS PER YOUR PREFERENCE 
detach_dir = r"E:\ASSIGNMENTS Beams and Cables"

m.select('INBOX')

#typ, items = m.search(None, 'FROM','"%s"' % user)
typ, items = m.search(None, 'ALL')
items = items[0].split()

#YOU CAN CHANGE THESE KEYWORDS 
#THE SCRIPT WILL DOWNLOAD ONLY THOSE ATTACHMENTS WHOSE FILENAME STARTS WITH THESE KEYWORDS
#SO YOU CAN TELL THE OTHERS BEFOREHAND TO ADD YOUR CHOSEN KEYWORD IN THE BEGINNING OF THE FILENAME
swith = ['BEAMS','CABLES']

try:
    os.mkdir(detach_dir)
except FileExistsError:
    pass

#CURRENTLY IT DOWNLOADS ALL FILES STARTING WITH THE KEYWORD  

count = 1
for emailid in reversed(items):
    if count < 3:
        typ,data = m.fetch(emailid, "(RFC822)")
        email_body = data[0][1].decode('utf-8')
        mail = email.message_from_string(email_body)
        print(emailid)
        print("[" + mail["From"] + "] :" + mail["Subject"])
        
       
        for part in mail.walk():
                if part.get_content_maintype() == 'multipart':
                      #print("maintype is multipart")
                      continue
                if part.get('Content-Disposition') is None:
                      #print("content disposition is None")
                      continue
                
                filename = part.get_filename()
                #print('x ',filename)
                
                    
                if not filename:
                    continue;
                    
                s = ""
                x = False
                for i in swith:
                    if filename.upper().startswith(i):
                        s = i
                        x = True
                    
                if not x:
                    #print('y')
                    continue;
                
		#HERE IT CREATES DIRECTORIES ACCORDING TO THE COLLEGE AND BRANCH 
		#I CAN CHANGE THIS TO JUST DOWNLOAD THE FILE AND NOT CREATE THE SUBFOLDERS TOO 
                if filename[len(s)+1 : len(s)+3 ].upper() == "UI":
                    college = "IIIT"
                    y = int(filename[len(s)+3 : len(s) + 5])
                    y = (20 - y)
                    year = "Year-%d" % y
                    branch = filename[len(s) + 5 : len(s) + 7].upper()
                    roll = filename[len(s)+1 : len(s)+9 ].upper()
                else:
                    college = "SVNIT"
                    y = int(filename[len(s)+2 : len(s) + 4])
                    y = (20 - y)
                    year = "Year-%d" % y
                    branch = filename[len(s)+4 : len(s) + 6].upper()
                    roll = filename[len(s)+1 : len(s)+8 ].upper()
                
                att_path = os.path.join(detach_dir,college)
                att_path = os.path.join(att_path,year)
                att_path = os.path.join(att_path,branch)
                att_path = os.path.join(att_path,roll)
                
                try:
                    os.makedirs(att_path)
                except FileExistsError:
                    pass
                
                att_path = os.path.join(att_path,filename)
                with open(att_path,'wb') as fp:
                    fp.write(part.get_payload(decode = True))
                
       # count += 1
