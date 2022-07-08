import requests

class ResyLogin(): 
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.headers = {
            'origin': 'https://resy.com',
            'accept-encoding': 'gzip, deflate, br',
            'x-origin': 'https://resy.com',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'application/json, text/plain, */*',
            'referer': 'https://resy.com/',
            'authority': 'api.resy.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                }

    def login(self):
        data = {
        'email': self.username,
        'password': self.password
            }
        response = requests.post('https://api.resy.com/3/auth/password', headers=self.headers, data=data)
        res_data = response.json()
        try:
            auth_token = res_data['token']
        except KeyError:
            print("Incorrect username/password combination")
        payment_method_string = '{"id":' + str(res_data['payment_method_id']) + '}'
        print(f"Logged in as {self.username}")
        return auth_token, payment_method_string
