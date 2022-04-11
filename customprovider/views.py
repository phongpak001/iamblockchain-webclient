from os import access
import profile
import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView)
from .provider import CustomProvider
from django.conf import settings

class CustomAdapter(OAuth2Adapter):
    provider_id = CustomProvider.id
    settings = app_settings.PROVIDERS.get(provider_id, {})
    if "CUSTOM_URL" in settings:
        web_url = settings.get("CUSTOM_URL").rstrip("/")
        api_url = "{0}/api/v3".format(web_url)
    else:
        web_url = "https://example.com"
        api_url = "https://api.example.com"
    # fetched programmatically, must be reachable from container
    access_token_url = "{0}/login/oauth/access_token".format(web_url)
    authorize_url = "{0}/login/oauth/authorize".format(web_url)
    profile_url = "{0}/user".format(api_url)
    emails_url = "{0}/user/emails".format(api_url)
    # Accessed by user browser, must be reachable by the host
    # authorize_url = '{}/o/authorize'.format('http://localhost:9977')
    
    # NOTE: trailing slashes in URLs are important, don't miss it
    
    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization' : 'token {}'.format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        if app_settings.QUERY_EMAIL and not extra_data.get("email"):
            extra_data["email"] = self.get_email(headers)
        return self.get_provider().sociallogin_from_response(request, extra_data)
    
oauth2_login = OAuth2LoginView.adapter_view(CustomAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(CustomAdapter)