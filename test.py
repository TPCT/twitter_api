from requests import Session
from datetime import datetime

username = "islam"
email = "islam@stackdeans.com"
password = "Th3@Professional"
birthday = datetime.strptime("14/8/1998", "%d/%m/%Y")

session = Session()
session.headers.update({
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'x-twitter-client-language': 'en'
})
session.proxies.update({
            "http": "socks5://suejqebo-rotate:tsitm3zlm1hh@p.webshare.io:80/",
            "https": "socks5://suejqebo-rotate:tsitm3zlm1hh@p.webshare.io:80/"
        })
# guest token
guest_token_response = session.post('https://api.twitter.com/1.1/guest/activate.json')
guest_token = guest_token_response.json()['guest_token'].strip()
print(guest_token)

session.headers.update({'x-guest-token': guest_token})
task_flow_response = session.post('https://twitter.com/i/api/1.1/onboarding/task.json?flow_name=signup', json={
    "input_flow_data": {
        "flow_context": {
            "debug_overrides": {},
            "start_location": {
                "location": "manual_link"
            }
        }
    },
    "subtask_versions": {
        "contacts_live_sync_permission_prompt": 0,
        "email_verification": 1,
        "topics_selector": 1,
        "wait_spinner": 1,
        "cta": 4
    }
})
flow_token = task_flow_response.json()['flow_token']
print(flow_token)

# email available task
email_available_response = session.get(
    'https://twitter.com/i/api/i/users/email_available.json?email=islam@stackedans.com')
is_available = not email_available_response.json()['taken']
print(is_available)
# begin verification response

begin_verification_response = session.post('https://twitter.com/i/api/1.1/onboarding/begin_verification.json', json={
    'email': "islam@stackdeans.com",
    'display_name': "islam",
    'flow_token': flow_token
})
print(begin_verification_response, begin_verification_response.text)

code = input("code: ")

# register an email

register_email_response = session.post("https://twitter.com/i/api/1.1/onboarding/task.json", json={
    "flow_token": flow_token, "subtask_inputs": [
        {"subtask_id": "Signup",
         "sign_up": {"link": "email_next_link", "name": "islam", "email": email,
                     "birthday": {"day": birthday.day, "month": birthday.month, "year": birthday.year},
                     "personalization_settings": {"allow_cookie_use": True, "allow_device_personalization": True,
                                                  "allow_partnerships": True, "allow_ads_personalization": True}}},
        {"subtask_id": "SignupSettingsListEmailNonEU", "settings_list": {
            "setting_responses": [{"key": "twitter_for_web", "response_data": {"boolean_data": {"result": True}}}],
            "link": "next_link"}},
        {"subtask_id": "SignupReview", "sign_up_review": {"link": "signup_with_email_next_link"}},
        {"subtask_id": "EmailVerification",
         "email_verification": {"code": code, "email": email, "link": "next_link"}}
    ]})

print(register_email_response, register_email_response.text)
