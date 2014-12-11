from authomatic.providers import oauth2

CONFIG = {
        
    'fb': {
           
        'class_': oauth2.Facebook,
        
        # Facebook is an AuthorizationProvider too.
        'consumer_key': '1487223801519357',
        'consumer_secret': '0705561d967c0702c19d6b5554a84865',
        
        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_likes',],
    },
    
}