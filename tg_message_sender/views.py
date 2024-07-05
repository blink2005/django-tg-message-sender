import telebot

from django.shortcuts import render
from .models import History

ERROR_FILLED_FORM = 'Заполните все поля формы!'
MESSAGE_IS_SEND = 'Отправлено'

def main(request):
    if request.method == 'GET':
        return render_index_html(request)
    if request.method == 'POST':
        check_form = check_filled_form(request)
        if check_form:
            send_status = send_message(check_form['token'], check_form['chat_id'], check_form['message'])
            return render_index_html(request, status=send_status)
        else:
            return render_index_html(request, error=ERROR_FILLED_FORM)

def check_filled_form(request): # Вернёт заполненный словарь если поля формы заполнены
    token = request.POST.get('token')
    chat_id = request.POST.get('chat_id')
    message = request.POST.get('message')

    if token and chat_id and message:
        return {'chat_id': chat_id, 'token': token, 'message': message}
    else:
        return {}
    
def send_message(token, chat_id, message):
    try:
        bot = telebot.TeleBot(token)
        bot.send_message(chat_id=chat_id, text=message)
        add_in_history_db(token, chat_id, message)
        return MESSAGE_IS_SEND
    except Exception as ex:
        return str(ex)

def add_in_history_db(token, chat_id, message):
    History.objects.create(token=token, chat_id=chat_id, message=message)

def render_index_html(request, status='', error=''):
    return render(request, 'index.html', context={'error': error, 'status': status}) 