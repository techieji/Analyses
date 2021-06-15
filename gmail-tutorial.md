# How to use Google's Gmail API

In the interconnected world of today, informing people of things you are doing is vital to your
social status. The dominant way of doing so is email. Using email is great for one-on-one
conversations, but if you need to broadcast the same message or slightly different messages to
many people, typing each one into your mail client and clicking send can get tedious fast. How should
you solve this problem?

Chances are, you already know: using an API. I volunteer for [Valluvan Tamil Academy](https://www.valluvantamil.org/),
and we need to use Google's API for many things, including pulling from a database to customize a message to simply
sending a fixed message to a fixed group of people. Since the latter is simpler, that is what I'll cover in this article.

You'll first need to create a service account using [GCP](https://console.cloud.google.com/), enable the Gmail API, and save
the credentials file in your current working directory. I'm not going to go into this because minimal research can reveal the
answer to any questions you may have. This article is concerned with the email-sending part, not the configuration.

So once you have saved the credentials, which, for brevity's sake, I will call `creds.json`, you'll need to install some requirements,
namely the following, which is conveniently in python's `requirements` format:

```text
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
google-auth
```

Once these are installed, we can get started with the email sending part of this. Copy this file into `send.py`:

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


