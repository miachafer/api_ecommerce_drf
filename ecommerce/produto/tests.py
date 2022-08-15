from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import ANY
import uuid
import json

from .models import Produto

class TestEndpointsProduto(APITestCase):
    def test_post_produto_request_invalida(self):
        request_produto = {
          "nome": 789123456,
          "descricao": 456782467,
          "preco": 8,
          "quantidade": -23
         }
        response = self.client.post('/produtos/', request_produto, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),{
            "nome": ["Nome do produto não pode conter só números. Forneça um novo nome."],
            "descricao": ["Descrição do produto não pode conter só números. Forneça uma nova descrição."]
            })

    def test_post_produto_request_valida(self):
        request_produto = {
          "nome": "Bola de Pilates",
          "descricao": "Bola de Pilates de 60 cm de diametro",
          "preco": 60.0,
          "quantidade": 50
         }
        response = self.client.post('/produtos/', request_produto, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(),{
          "id": ANY,
          "nome": "Bola de Pilates",
          "descricao": "Bola de Pilates de 60 cm de diametro",
          "preco": "60.00",
          "quantidade": 50,
          "criado_em": ANY,
          "atualizado_em": ANY
          })


    def test_get_lista_de_produtos(self):
        produto = Produto.objects.create(id=uuid.uuid4(), quantidade=10, preco=1.0)
        response = self.client.get('/produtos/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()),1)

    def test_get_produto_endpoint(self):
        produto = Produto.objects.create(quantidade=10, preco=1.0)
        response = self.client.get('/produtos/', args=produto.id, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),[{
          "id": ANY,
          "nome": ANY,
          "descricao": ANY,
          "preco": "1.00",
          "quantidade": 10,
          "criado_em": ANY,
          "atualizado_em": ANY
          }])




      


