Title: Enabling SMTP authentication PLAIN mechanism for web2py
Date: 2015-10-08 16:47:21
Category: web2py
Tags: python, web2py
Slug: web2py_smtp
Authors: Abhishek Bajpai
Summary: SMTP authentication PLAIN mechanism for web2py


Some SMTP servers needs clients to configuration for authentication mechanism. Their is no way to configure this mechanism in web2py.


In order to enable this mechanism changes are required in /usr/lib64/python2.7/smtplib.py

```python
    AUTH_PLAIN = "PLAIN"
    AUTH_CRAM_MD5 = "CRAM-MD5"
    AUTH_LOGIN = "LOGIN"

    self.ehlo_or_helo_if_needed()

    if not self.has_extn("auth"):
        raise SMTPException("SMTP AUTH extension not supported by server.")

    # Authentication methods the server supports:
    authlist = self.esmtp_features["auth"].split()

    # List of authentication methods we support: from preferred to
    # less preferred methods. Except for the purpose of testing the weaker
    # ones, we prefer stronger methods like CRAM-MD5:
    preferred_auths = [AUTH_CRAM_MD5, AUTH_PLAIN, AUTH_LOGIN]

    # Determine the authentication method we'll use
    authmethod = None
```

just modify the preferred_auths list according to your preferred settings.


In my case

```python
    preferred_auths = [AUTH_PLAIN, AUTH_CRAM_MD5, AUTH_PLAIN, AUTH_LOGIN]
```


