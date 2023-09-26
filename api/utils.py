import re

class UserValidator:
    def __init__(self, email, password, full_name, phone, pincode):
        self.email = email
        self.password = password
        self.full_name = full_name
        self.phone = phone
        self.pincode = pincode

    def validate_email(self):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            return "Invalid email address"
        return None

    def validate_password(self):
        if len(self.password) < 8:
            return "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', self.password) or not re.search(r'[a-z]', self.password):
            return "Password must contain both uppercase and lowercase letters"
        return None

    def validate_full_name(self):
        if not re.match(r'^[A-Za-z]+\s[A-Za-z]+$', self.full_name):
            return "Invalid full name. Please provide both First Name and Last Name"
        return None

    def validate_phone(self):
        if not re.match(r'^\d{10}$', self.phone):
            return "Phone number must be 10 digits"
        return None

    def validate_pincode(self):
        if not re.match(r'^\d{6}$', self.pincode):
            return "Pincode must be 6 digits"
        return None
    
    def validate_all(self):
        errors = filter(None, [
            self.validate_email(),
            self.validate_password(),
            self.validate_full_name(),
            self.validate_phone(),
            self.validate_pincode()
        ])
        return list(errors)

class ContentValidator:
    def __init__(self, title, body, summary):
        self.title = title
        self.body = body
        self.summary = summary

    def validate_title(self):
        if len(self.title) > 30:
            return "Invalid content title, it must be less then 30 characters."
        return None

    def validate_body(self):
        if len(self.body) > 300:
            return "Invalid content body, it must be less then 30 characters."
        return None

    def validate_summary(self):
        if len(self.summary) > 60:
            return "Invalid content summary, it must be less then 30 characters."
        return None
    
    def validate_all(self):
        errors = filter(None, [
            self.validate_title(),
            self.validate_body(),
            self.validate_summary()
        ])
        return list(errors)