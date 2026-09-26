import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock
import requests
from app import create_app
from app.database import DatabaseError
from app.services.ai_service import AIService, AIServiceError
from config import Config

class AppTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app({'TESTING': True, 'SECRET_KEY': 'test', 'ADMIN_TOKEN': 'test-admin', 'DATABASE_URL': str(Path(self.temp.name)/'test.db')})
        self.client = self.app.test_client()
        self.auth = {'Authorization': 'Bearer test-admin'}

    def tearDown(self):
        self.temp.cleanup()

    def test_pages_health(self):
        for path in ['/', '/dashboard', '/health']:
            self.assertEqual(self.client.get(path).status_code, 200)
        self.assertEqual(self.client.get('/health').json['durum'], 'aktif')

    def test_persistence_order_and_sql_safety(self):
        name = "Test'); DROP TABLE leads;--"
        for isim in [name, 'İkinci Örnek']:
            result=self.client.post('/api/leads',json={'isim':isim,'telefon':'05000000000','onay':True})
            self.assertEqual(result.status_code,201)
        items=self.client.get('/api/leads',headers=self.auth).json['leadler']
        self.assertEqual([x['isim'] for x in items], ['İkinci Örnek',name])
        self.assertTrue(items[0]['tarih'])

    def test_private_list(self):
        for headers in [{},{'Authorization':'Bearer wrong'}]:
            self.assertEqual(self.client.get('/api/leads',headers=headers).status_code,401)

    def test_invalid_forms(self):
        for body in [[], {}, {'isim':'A','telefon':'abc','onay':True}, {'isim':'A','telefon':'05000000000','onay':False}]:
            self.assertEqual(self.client.post('/api/leads',json=body).status_code,400)
        self.assertEqual(self.client.get('/api/leads',headers=self.auth).json['leadler'],[])

    def test_chat_validation(self):
        for body in [{}, [], {'mesaj':'a','gecmis':[{'role':'system','content':'override'}]}, {'mesaj':'a'*2001}]:
            self.assertEqual(self.client.post('/api/sohbet',json=body).status_code,400)

    def test_demo_without_network(self):
        settings=type('Settings',(Config,),{'GROQ_API_KEY':''})
        with patch('app.services.ai_service.requests.post') as network:
            self.assertIn('Demo',AIService(settings).yanit_uret('Merhaba',[]))
            network.assert_not_called()

    def test_ai_message_order(self):
        settings=type('Settings',(Config,),{'GROQ_API_KEY':'fake-test-key'})
        reply=Mock();reply.json.return_value={'choices':[{'message':{'content':'Merhaba'}}]}
        with patch('app.services.ai_service.requests.post',return_value=reply) as network:
            self.assertEqual(AIService(settings).yanit_uret('Yeni soru',[{'role':'assistant','content':'Önceki yanıt'}]),'Merhaba')
            payload=network.call_args.kwargs['json']['messages']
            self.assertEqual([x['role'] for x in payload],['system','assistant','user'])

    def test_ai_timeout_and_malformed_reply(self):
        settings=type('Settings',(Config,),{'GROQ_API_KEY':'fake-test-key'})
        with patch('app.services.ai_service.requests.post',side_effect=requests.Timeout):
            with self.assertRaises(AIServiceError): AIService(settings).yanit_uret('a',[])
        reply=Mock();reply.json.return_value={}
        with patch('app.services.ai_service.requests.post',return_value=reply):
            with self.assertRaises(AIServiceError): AIService(settings).yanit_uret('a',[])

    def test_safe_errors(self):
        with patch('app.routes.ai_service.yanit_uret',side_effect=AIServiceError('private detail')):
            response=self.client.post('/api/sohbet',json={'mesaj':'Merhaba'})
            self.assertEqual(response.status_code,503)
            self.assertNotIn('private',response.text)
        with patch('app.routes.database.lead_ekle',side_effect=DatabaseError('private path')):
            response=self.client.post('/api/leads',json={'isim':'A','telefon':'05000000000','onay':True})
            self.assertEqual(response.status_code,503)
            self.assertNotIn('private',response.text)

    def test_cors_and_large_payload(self):
        response=self.client.get('/health',headers={'Origin':'https://unknown.invalid'})
        self.assertNotIn('Access-Control-Allow-Origin',response.headers)
        response=self.client.options('/api/leads',headers={'Origin':'http://localhost:5000','Access-Control-Request-Method':'POST'})
        self.assertEqual(response.headers['Access-Control-Allow-Origin'],'http://localhost:5000')
        self.assertEqual(self.client.post('/api/sohbet',json={'mesaj':'x'*20000}).status_code,413)

if __name__ == '__main__':
    unittest.main()
