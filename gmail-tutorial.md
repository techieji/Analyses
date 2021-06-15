# How to use Google's Gmail API

In the interconnected world of today, informing people of things you are doing is vital to your
social status. The dominant way of doing so is email. Using email is great for one-on-one
conversations, but if you need to broadcast the same message or slightly different messages to
many people, typing each one into your mail client and clicking send can get tedious fast. How should
you solve this problem?

Chances are, you already know: using an API. I volunteer for [Valluvan Tamil Academy](https://www.valluvantamil.org/),
and we need to use Google's API for many things, including pulling from a database to customize a message to simply
sending a fixed message to a fixed group of people. Since the latter is simpler, that is what I'll cover in this article.

## Acquiring Credentials

You'll first need to create a service account using [GCP](https://console.cloud.google.com/), enable the Gmail API, add permissions
to send emails, and save the credentials file in your current working directory. I'm not going to go into this because minimal research
can reveal the answer to any questions you may have. This article is concerned with the email-sending part, not the configuration.

So once you have saved the credentials, which, for brevity's sake, I will call `creds.json`, you'll need to install some requirements,
namely the following, which is conveniently in python's `requirements` format:

```text
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
google-auth
```

Once these are installed, we can get started. 

## Building a Message

Python has a builtin email module for creating emails. Google accepts these objects and can send them. So, logically, we should first
learn how to construct a message. Copy the following text to a file somewhere:

```python
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart()
msg['to'] = 'person@example.com'
msg['from'] = 'me@example2.com'
msg['subject'] = 'Test Subject'

msg.attach(MIMEText("This is the content!"))

print(msg)
```

The above code does not actually send anything; all it does is print out the constructed message.

When this code is run, you should see something like this:

```text
Content-Type: multipart/mixed; boundary="===============2209331409816672794=="
MIME-Version: 1.0
to: person@example.com
from: me@example2.com
subject: Test Subject

--===============2209331409816672794==
Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

This is the content!
--===============2209331409816672794==--
```

You can also add images to the `MIMEMultipart` object by using the attach method. There are a few changes you have
to make, however. First, you have to add the line `from email.mime.image import MIMEImage` to the top, and second, you
have to add a line `msg.attach(MIMEImage('filename.here'))`.

But enough about creating messages. How do we send them? We first have to authenticate.

## Authenticating

Remember `creds.json`, your credentials file? In order to successfully authenticate, you need to create an environment variable
`GOOGLE_APPLICATION_CREDENTIALS` which is set to the path of your credentials file. After this is done, you need some basic boilerplate
code:

```python
import google.auth
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
credentials, project = google.auth.default(scopes=SCOPES)
delegated_credentials = credentials.with_subject('me@example2.com')
service = build('gmail', 'v1', credentials=delegated_credentials)
```

Basically, all this code does is declare what permissions it wants, what service account it wants it for, and finally builds a service with which emails
can be sent.

Finally, we can get to the fun part: actually sending the message.

## Sending Emails

This part is the most complex:

```python
import base64

service.users().message().send(
    userId='me',
    body={
        'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()
    }
).execute()
```

There's not a lot to explain. It just works.

## Putting the Pieces Together

Here is everything shown above put together into one giant code blob:

```python
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

import base64

import google.auth
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
credentials, project = google.auth.default(scopes=SCOPES)
delegated_credentials = credentials.with_subject('me@example2.com')
service = build('gmail', 'v1', credentials=delegated_credentials)

#### The actual email starts here

msg = MIMEMultipart()
msg['to'] = 'person@example.com'
msg['from'] = 'me@example2.com'
msg['subject'] = 'Test Subject'

msg.attach(MIMEText("This is the content!"))
msg.attach(MIMEImage("thing.jpg"))            # Attaching an image

#### The actual email ends here

service.users().message().send(
    userId='me',
    body={
        'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()
    }
).execute()
```

To review the steps this program takes:

1. Authenticate using the credential file
2. Build a service using the credentials
3. Create the actual email
4. Send it using some magic

And that is how you use Gmail's API to send emails.
