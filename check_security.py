from math import log2
import string
import secrets

class Password:
    @staticmethod
    def check_for_words(password:str) -> bool:
        """
        Function for checking popular words used in passwords.
        Returns boolean to show another function that there is(are) hidden word(s) in password
        """

        most_used_words = [
            "password", "pass", "admin", "qwerty", "dragon",
            "monkey", "master", "login"
        ]
        replacement = {"@": "a", "$": "s",
                       "0": "o", "!": "i",
                       "3": "e", "1": "i"}

        password=password.lower() #lower password so it will be easier to check in the end

        for char, replace in replacement.items():
            # loop in order to replace all the symbols
            password=password.replace(char, replace)

        for word in most_used_words:
            # loop for checking word(s') existence in password
            if word in password:
                return True

        return False

    @staticmethod
    def analise(password:str):
        """
        Function gets string password and checks it for security
        according to Shannon formula (Entropy=H*log2(L))
        where H - length of password and L - length of used alphabet
        """

        if not password:
            return None # No password = None

        lower=any(c.islower() for c in password) # presence of lower-case letters
        upper=any(c.isupper() for c in password) # presence of upper-case letters
        digits=any(c.isdigit() for c in password) # presents of digits
        other=any(c in string.punctuation for c in password) # presents of other symbols
        word_found=Password.check_for_words(password) # hidden word finding

        symbol_used_size=0 # find L

        if lower:
            symbol_used_size+=26 # full english alphabet (lower-case)
        if upper:
            symbol_used_size+=26 # full english alphabet (upper-case)
        if digits:
            symbol_used_size+=10 # digits 0-9
        if other:
            symbol_used_size+=32 # other symbols

        entropy=len(password) * log2(symbol_used_size) # formula of Shannon

        if word_found: # if word(s) is(are) found decline entropy by 40%
            entropy*=0.4
        entropy = round(entropy, 1)

        # Checking of entropy bits
        if entropy<50:
            return "Weak password"
        elif entropy<75:
            return "Medium password"
        elif entropy>110:
            return "Strong password"

    @staticmethod # using this method so we can access function without creating class object
    def recommend_new_password():
        """
        Function for creation of approximately 111.4 entropy bits password
        """

        # log2(94) ~ 6.55
        # H * 6.44 > 110 -> H> 110/6.55 ~ 17 -> H>17

        everything=string.ascii_letters+string.digits+"!@#$%^&*" # every possible symbol for password

        password=[secrets.choice(string.ascii_lowercase)+secrets.choice(string.ascii_uppercase)
                  +secrets.choice(string.digits)+secrets.choice("!@#$%^&*")] # making sure every symbol is included

        #using secrets for higher security

        password+=[secrets.choice(everything) for _ in range(13)] # inputting next 13 random symbols

        secrets.SystemRandom().shuffle(password) # shuffle existing password, so guessing it became harder

        return "".join(password)