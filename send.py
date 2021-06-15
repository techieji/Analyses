from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart()
msg['to'] = 'person@example.com'
msg['from'] = 'me@example2.com'
msg['subject'] = 'Test Subject'

msg.attach(MIMEText("This is the content!"))

print(msg)
