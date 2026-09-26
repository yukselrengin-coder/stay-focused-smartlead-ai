"""Flask ve veritabanından bağımsız yapay zekâ servisi."""
import re
import requests
from config import Config

class AIServiceError(Exception):
    pass

class AIService:
    def __init__(self, settings=Config):
        self.settings = settings

    def _sistem_talimati(self):
        return self.settings.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis):
        greeting = ' '.join(re.findall(r'\w+', mesaj.casefold()))
        reply = getattr(self.settings, 'FIXED_REPLIES', {}).get(greeting)
        if reply is not None:
            return reply
        if not self.settings.GROQ_API_KEY:
            return self.settings.DEMO_REPLY
        if self.settings.AI_PROVIDER != 'groq':
            raise AIServiceError('Sağlayıcı desteklenmiyor.')
        messages = [{'role': 'system', 'content': self._sistem_talimati()}]
        messages.extend(gecmis[-10:])
        messages.append({'role': 'user', 'content': mesaj})
        return self._groq_istegi(messages)

    def _groq_istegi(self, messages):
        try:
            result = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers={'Authorization': f'Bearer {self.settings.GROQ_API_KEY}'},
                json={'model': self.settings.AI_MODEL, 'messages': messages, 'max_tokens': 400},
                timeout=25,
            )
            result.raise_for_status()
            answer = result.json()['choices'][0]['message']['content']
            if not isinstance(answer, str) or not answer.strip():
                raise ValueError('Boş yanıt')
            return answer
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError) as exc:
            raise AIServiceError('Asistan şu anda yanıt veremiyor. Lütfen tekrar deneyin.') from exc

ai_service = AIService()
