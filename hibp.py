from errbot import BotPlugin, botcmd, arg_botcmd, webhook
import re
import requests
import json
import logging

baseAPI = "https://haveibeenpwned.com/api/v2/"
userAgent = "Errbot-HIBPplugin/0.1"
limit = 20 # Quit after this many hits

class hibp(BotPlugin):
    """
    Query the HaveIBeenPwned database. Currently this will only perform lookups in breaches of a provided email address.
    """

    def get_account(self, emailaccount):
        userAgent = "Errbot-HIBPplugin/1.0"
        headers = {'user-agent': userAgent}
        url = baseAPI + "breachedaccount/" + emailaccount
        self.log.debug("URL: " + url)
        r = requests.get(url, headers=headers)
        return r

    @botcmd
    def hibp(self, message, emailaccount):
        """
        Lookup all breaches for an email account in the HaveIBeenPwned database
        """
        
        if emailaccount is '':
            self.log.debug("No email address found. Exiting.")
            yield "`Error:` I can't look up an email address if you don't tell me what it is..."
        else:
            self.log.debug("Email: {}".format(emailaccount))
            response = self.get_account(emailaccount)
            if response.status_code in (200,):
                #self.log.debug("Retrieved data: {}".format(response.text))
                data = response.json()
                #self.log.debug("JSON data: {}".format(data))
                pwnage = 0
                yield "```{}``` was found in the following breaches:".format(emailaccount)
                for line in data:
                    pwnage += 1
                    yield "_{}_".format(line['Domain'])
                    if pwnage >= limit:
                        yield "... and more - too many to show here. Visit haveibeenpwned.com"

            elif response.status_code in (400,):
                self.send(message.frm, "`Error: Bad Request`")
            elif response.status_code in (401,):
                self.send(message.frm, "`Error: Access Denied`")
            elif response.status_code in (403,):
                self.send(message.frm, "`Error: Forbidden`")
            elif response.status_code in (404,):
                #self.send(message.frm, "```{}``` was not found in the HIBP breach database.".format(emailaccount))
                self.log.debug("Email {} was not found in the HIBP database".format(emailaccount))
                yield "```{}``` was not found in the HIBP breach database.".format(emailaccount)
            elif response.status_code in (429,):
                self.send(message.frm, "`Error: Too Many Requests - the rate limit has been exceeded`") 
            else:
                yield "Unhandled error"