from django.test import TestCase
from rest_framework.reverse import reverse_lazy
from empresas.models import Empresa


class EmpresaViewSetTestCase(TestCase):

    def setUp(self):
        self.url_listagem = reverse_lazy('listagem_empresa')
        self.url_detalhes = reverse_lazy('detalhes_empresa')

        Empresa.objects.create(
            cnpj='14.375.882/0001-84',
            nome='ACME',
            capital_social=1000000
        )

    def test_get_empresa(self):
        response = self.client.get(self.url_listagem)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_post_empresa(self):
        payload = {
            'cnpj': '25.768.090/0001-96',
            'nome': 'Wayne Corp',
            'capital_social': 500000
        }
        response = self.client.post(self.url_listagem, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.json().get('cnpj'))
        self.assertIsNotNone(response.json().get('nome'))
        self.assertIsNotNone(response.json().get('capital_social'))
        self.assertIsNotNone(response.json().get('id'))

    def test_retrieve_empresa(self):
        response = self.client.get(reverse_lazy('detalhes_empresa', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), dict))

    def test_delete_empresa(self): ...

    def test_put_empresa(self): ...

    def test_patch_empresa(self): ...
