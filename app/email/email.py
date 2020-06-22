import uuid
import base64
import smtplib

class Email:
    client = None
    sender = []
    receiver = []
    subject = "Mensagem enviada pelo MWooAPI"
    message = ""
    attachments = []

    def __init__(self, host, port, user, password):
        self.initiateClient(host, port, user, password)

    def initiateClient(self, host, port, user, password):
        self.client = smtplib.SMTP_SSL(
            host=host,
            port=port
        )
        self.client.login(user, password)
        self.client.ehlo_or_helo_if_needed()

    def setSender(self, sender):
        self.sender = sender
        return self.sender

    def setReceiver(self, receiver):
        if isinstance(receiver, list):
            self.receiver = receiver
        else:
            self.receiver.append(receiver)
        return self.receiver

    def setSubject(self, subject):
        self.subject = subject
        return self.subject

    def setMessage(self, message):
        self.message = message
        return self.message

    def setAttachments(self, attachment):
        attachmentOpened = open(attachment, "rb")
        filecontent = attachmentOpened.read()
        attachmentEncoded = base64.b64encode(filecontent)

        self.attachments.append([
            attachment,
            attachmentEncoded
        ])

        return self.attachments

    def makeEmail(self):
        uniqueKey = uuid.uuid4()
        receivers = ["{} <{}>".format(r[0], r[1]) for r in self.receiver]

        email = "From: {} <{}>\n".format(self.sender[0],self. sender[1])
        email += "To: {}\n".format(";".join(receivers))
        email += "Subject: {}\n".format(self.subject)

        email += "MIME-Version: 1.0\n"
        email += "Content-Type: multipart/mixed; boundary={}\n".format(uniqueKey)
        email += "--{}\n".format(uniqueKey)

        email += "Content-Type: text/plain\n"
        email += "Content-Transfer-Encoding:8bit\n"
        email += "\n"
        email += "{}\n".format(self.message)
        email += "--{}\n".format(uniqueKey)

        if len(self.attachments) > 0:
            for attachment in self.attachments:
                email += """
                Content-Type: application/json; name="{filename}"
                Content-Transfer-Encoding:base64
                Content-Disposition: attachment; filename={filename}"

                {content}
                --{key}
                """.format(
                    filename=attachment[0].split('/')[1],
                    content=attachment[1],
                    key=uniqueKey
                )
        return email

    def send(self):
        try:
            message = self.makeEmail()

            self.client.sendmail(
                self.sender[1],
                [r[1] for r in self.receiver],
                message.encode("ascii", errors="ignore")
            )

            print("Successfully sent email")
        except Exception as e:
            print("Error: unable to send email", e)
