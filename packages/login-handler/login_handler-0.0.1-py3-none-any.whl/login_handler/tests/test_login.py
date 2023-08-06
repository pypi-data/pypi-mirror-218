
class TestLogin(object):

    def test_basic(self, app, client):
        response = client.get("/")

        assert "HI" == response.data.decode("utf-8")

    def test_database(self, app, client, database):
        data = {
            "username": "Raheel",
            "email": "raheel@real.com",
            "age": 23
        }
        response = client.post("/create-user", data=data, follow_redirects=True)

        assert "HI" == response.data.decode("utf-8")

        data = {
            "username": "Raheel",
            "email": "new-raheel@real.com",
            "age": 25
        }
        response = client.post("/create-user", data=data, follow_redirects=True)

        assert "User already exists" == response.data.decode()

    def test_login(self, client):
        data = {
            "username": "Raheel",
            "email": "raheel@real.com"
        }

        response = client.post("/login-user", data=data, follow_redirects=True)

        assert 200 == response.status_code
