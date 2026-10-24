from rest_framework_simplejwt.tokens import RefreshToken

class MyToken(RefreshToken): 
    @classmethod 
    def for_user(cls, user): 
        token = super().for_user(user) 
        # Custom payload 
        token['username'] = user.username 
        token['email'] = user.email 
        token['first_name'] = user.first_name 
        token['last_name'] = user.last_name

        return token