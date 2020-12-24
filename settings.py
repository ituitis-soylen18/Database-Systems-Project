DEBUG = True
PORT = 8080
SECRET_KEY = "secret"
WTF_CSRF_ENABLED = True

PASSWORDS = {
    "zümra": "$pbkdf2-sha256$29000$itF6r1WKMeYcI.Qcg3AOQQ$2FfE1FhS4dOLKmtKEckNtwg0kTFux6R8sc.p1Mrra7k",
    "normaluser": "$pbkdf2-sha256$29000$itF6r1WKMeYcI.Qcg3AOQQ$2FfE1FhS4dOLKmtKEckNtwg0kTFux6R8sc.p1Mrra7k",
}

ADMIN_USERS = ["zümra"]