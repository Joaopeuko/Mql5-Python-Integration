import smtplib
from email.mime.text import MIMEText
import email
import imaplib


# https://myaccount.google.com/u/0/security?hl=en:
class Email:
    def __init__(self,
                 email_from='trading.by.email@gmail.com',
                 smtp_ssl_host='smtp.gmail.com',  # connect with Google's servers
                 smtp_ssl_port=465
                 ):
        self.email_from = email_from
        self.password = input('Please, provide the password: ')
        self.smtp_ssl_host = smtp_ssl_host
        self.smtp_ssl_port = smtp_ssl_port

    def sending_email(self,
                      email_to
                      ):
        # https://docs.python.org/3/library/email.mime.html
        # the email lib has a lot of templates
        # for different message formats,
        # on our case we will use MIMEText
        # to send only text
        message = MIMEText('Hello World')

        message['from'] = self.email_from
        message['to'] = ', '.join(email_to)
        message['subject'] = 'Hello'

        # we'll connect using SSL
        server = smtplib.SMTP_SSL(self.smtp_ssl_host, self.smtp_ssl_port)
        # to interact with the server, first we log in
        # and then we send the message
        server.login(self.email_from, self.password)
        server.sendmail(self.email_from, email_to, message.as_string())
        print('Email has been sent.')
        server.quit()

    def receiving_email(self):

        # connect to the server and go to its inbox
        mail = imaplib.IMAP4_SSL(self.smtp_ssl_host)
        mail.login(self.email_from, self.password)

        # we choose the inbox but you can select others
        mail.select('inbox')

        # we'll search using the ALL criteria to retrieve
        # every message inside the inbox
        # it will return with its status and a list of ids
        _ , data = mail.search(None, 'ALL') # UNSEEN
        # the list returned is a list of bytes separated
        # by white spaces on this format: [b'1 2 3', b'4 5 6']
        # so, to separate it first we create an empty list
        mail_ids = []
        # then we go through the list splitting its blocks
        # of bytes and appending to the mail_ids list
        for block in data:
            # the split function called without parameter
            # transforms the text or bytes into a list using
            # as separator the white spaces:
            # b'1 2 3'.split() => [b'1', b'2', b'3']
            mail_ids += block.split()

        # now for every id we'll fetch the email
        # to extract its content
        for i in mail_ids:
            # the fetch function fetch the email given its id
            # and format that you want the message to be
            _ , data = mail.fetch(i, '(RFC822)')
            # the content data at the '(RFC822)' format comes on
            # a list with a tuple with header, content, and the closing
            # byte b')'
            for response_part in data:
                # so if its a tuple...
                if isinstance(response_part, tuple):
                    # we go for the content at its second element
                    # skipping the header at the first and the closing
                    # at the third
                    message = email.message_from_bytes(response_part[1])

                    # with the content we can extract the info about
                    # who sent the message and its subject
                    mail_from = message['from']
                    mail_subject = message['subject']

                    # then for the text we have a little more work to do
                    # because it can be in plain text or multipart
                    # if its not plain text we need to separate the message
                    # from its annexes to get the text
                    if message.is_multipart():
                        mail_content = ''

                        # on multipart we have the text message and
                        # another things like annex, and html version
                        # of the message, in that case we loop through
                        # the email payload
                        for part in message.get_payload():
                            # if the content type is text/plain
                            # we extract it
                            if part.get_content_type() == 'text/plain':
                                mail_content += part.get_payload()
                    else:
                        # if the message isn't multipart, just extract it
                        mail_content = message.get_payload()
                    mail.store(i, '+FLAGS', '(\\Seen)')
                    # and then let's show its result
                    email_print = mail_from[mail_from.find('<')+1: mail_from.find('>')]
                    print(f'From: {email_print}')
                    # print(f'Subject: {mail_subject}')
                    # print(f'Content: {mail_content}')


email_ = Email()

#email_.sending_email(['joaopeuko@gmail.com'])

email_.receiving_email()
