from django.test import TestCase


class TestePaginas(TestCase):
    def teste_pagina(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Lista de Candidatos')
