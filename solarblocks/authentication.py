
from rest_framework.authentication import TokenAuthentication as DRFTokenAuthentication
from rest_framework.authentication import SessionAuthentication as DRFSessionAuthentication
from accounts.models import Token




class TokenAuthentication(DRFTokenAuthentication):
    model = Token



class SessionAuthentication(DRFSessionAuthentication):
    pass