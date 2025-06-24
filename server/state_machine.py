import json

class CallStateMachine:
    def __init__(self, user_data):
        self.user = user_data
        self.step = 'GREETING'

    def next(self, incoming_text):
        if self.step == 'GREETING':
            self.step = 'PII_NAME'
            return f"Hello, I’m Iris calling on behalf of {self.user['name']}."

        if self.step.startswith('PII'):
            field = {
                'PII_NAME': 'name',
                'PII_DOB': 'dob',
                'PII_CC': 'creditCard',
                'PII_ZIP': 'zip'
            }[self.step]
            reply = self.user[field]
            if self.step == 'PII_NAME': self.step = 'PII_DOB'
            elif self.step == 'PII_DOB': self.step = 'PII_CC'
            elif self.step == 'PII_CC': self.step = 'PII_ZIP'
            else: self.step = 'TRANSACTION'
            return reply

        if self.step == 'TRANSACTION':
            self.step = 'SUMMARY'
            return "I’d like to review my recent transactions. I see a $50 charge at Starbucks I didn’t make."  

        return None

    def summary_bullets(self):
        return [
            "Verified user identity.",
            "User disputed $50 Starbucks charge.",
            "Agency will credit within 3–5 business days."
        ]