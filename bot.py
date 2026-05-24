import os
import anthropic
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
 
# Ваши ключи (заменить на свои)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
 
SYSTEM_PROMPT = '''
Ты исламский учёный-ассистент. Отвечай на вопросы об исламе
на основе Корана, Сунны и мнений учёных. Определяй язык
вопроса автоматически и отвечай на том же языке.
Цитируй источники: аяты, хадисы, мнения улемов.
'''
 
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
 
async def handle_message(update: Update, context):
   user_text = update.message.text
   await update.message.reply_text('⏳ Ищу ответ...')
   
   response = client.messages.create(
       model='claude-sonnet-4-20250514',
       max_tokens=1000,
       system=SYSTEM_PROMPT,
       messages=[{'role': 'user', 'content': user_text}]
   )
   
   answer = response.content[0].text
   await update.message.reply_text(answer)
 
app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
