# https://pytest-flask.readthedocs.io/en/latest/features.html
from app import app
from flask.ext.testing import TestCase


class TestCaseApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'sekrit!'
        return app

    def test_get_access_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_without_username_and_password(self):
        response = self.client.post("/", data=dict(username="", password=""))
        self.assertEqual(response.status_code, 200)
        self.assert_context('error', 'Usuário e Senha são obrigatórios')

    def test_template_index(self):
        self.client.get("/")
        self.assert_template_used('index.html')

    def test_post_access_index(self):
        data = {"username": "user",
                "password": "pass"}
        response = self.client.post("/", data=data, follow_redirects=True)
        assert response.status_code == 200

    def test_template_post_access_index(self):
        data = {"username": "user",
                "password": "pass"}
        self.client.post("/", data=data, follow_redirects=True)
        self.assert_template_used('bdmeptoxls.html')

    def test_template_logout(self):
        self.client.get("/logout", follow_redirects=True)
        self.assert_template_used('index.html')

    def test_dashboard_without_login(self):
        response = self.client.get("/bdmeptoxls")
        assert response.status_code == 302

    def test_dashboard_without_login_redirect_to_login(self):
        self.client.get("/bdmeptoxls", follow_redirects=True)
        self.assert_template_used('index.html')

    def test_recomendacao(self):
        response = self.client.get("/recomendacao")
        assert response.status_code == 200
        self.assert_template_used('recomendacao.html')

    def test_download_mensal(self):
        data = {"username": "user",
                "password": "pass"}
        self.client.post("/", data=data, follow_redirects=True)
        data = {"estacao": "83695",
                "data_inicio": "01/01/2016",
                "data_fim": "01/02/2016"}
        response = self.client.post("/download/mensal", data=data, follow_redirects=True)
        assert response.content_type == 'application/vnd.ms-excel'
        assert response.headers['Content-Disposition'] == 'attachment; filename=ITAPERUNA_01012016_01022016_MENSAIS.xls'

    def test_download_mensal_without_login(self):
        data = {"estacao": "83695",
                "data_inicio": "01/01/2016",
                "data_fim": "01/02/2016"}
        response = self.client.post("/download/mensal", data=data)
        assert response.status_code == 302
        self.client.post("/download/mensal", data=data, follow_redirects=True)
        self.assert_template_used('index.html')

    def test_download_diarios(self):
        data = {"username": "user",
                "password": "pass"}
        self.client.post("/", data=data, follow_redirects=True)
        data = {"estacao": "83695",
                "data_inicio": "01/01/2016",
                "data_fim": "01/02/2016"}
        response = self.client.post("/download/diarios", data=data, follow_redirects=True)
        assert response.content_type == 'application/vnd.ms-excel'
        assert response.headers['Content-Disposition'] == 'attachment; filename=ITAPERUNA_01012016_01022016_DIARIOS.xls'

    def test_download_diarios_without_login(self):
        data = {"estacao": "83695",
                "data_inicio": "01/01/2016",
                "data_fim": "01/02/2016"}
        response = self.client.post("/download/diarios", data=data)
        assert response.status_code == 302
        self.client.post("/download/diarios", data=data, follow_redirects=True)
        self.assert_template_used('index.html')

    def test_download_horarios(self):
        data = {"username": "user",
                "password": "pass"}
        self.client.post("/", data=data, follow_redirects=True)
        data = {"estacao": "83695",
                "data_inicio": "01/01/2016",
                "data_fim": "01/02/2016"}
        response = self.client.post("/download/horarios", data=data, follow_redirects=True)
        assert response.content_type == 'application/vnd.ms-excel'
        assert response.headers['Content-Disposition'] == 'attachment; filename=ITAPERUNA_01012016_01022016_HORARIOS.xls'

    def test_download_horarios_without_login(self):
        data = {"estacao": "83695",
                "data_inicio": "01/01/2016",
                "data_fim": "01/02/2016"}
        response = self.client.post("/download/horarios", data=data)
        assert response.status_code == 302
        self.client.post("/download/diarios", data=data, follow_redirects=True)
        self.assert_template_used('index.html')

    def test_error_404(self):
        self.client.get("/asfdasd")
        self.assert_template_used("status_code/404.html")
