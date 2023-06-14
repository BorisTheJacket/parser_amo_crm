import time
import re
import logging
import json
from pupdb.core import PupDB
from pandas import DataFrame
from amo.api import Api
import database.database_worker as database


from aiogram import Bot, Dispatcher, executor, types

list_of_statuses = ['Рассрочка Тинькофф', 'МТС (от Тинькофф)', 'Ресурс Развития']


TOKEN = '6053579713:AAGhqGo2L-Mo0TPqSYVdxbypax0fL6ASfFM'
MSG = "Программировал ли ты сегодня, {}"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

list_of_dicts_bot = []
pd_list = []

DATA_DICT = {}

api = Api()


@dp.message_handler(content_types=['text'], regexp="^обратка$") #regexp='[^@]+@[^@]+\.[^@]+'
async def print_all_handler(message: types.Message):
    user_id = message.from_user.id
    state = database.get_state(user_id)
    emails = state.all_emails()
    messages = []
    for email, body in emails.items():
        print(email)
        email_valid = '🚀' if body['lead_id'] != '' else '🚫'
        messages.append(f'{email} {email_valid}')

    await message.answer('\n'.join(messages))


@dp.message_handler(content_types=['text']) #regexp='[^@]+@[^@]+\.[^@]+'
async def message_adder_handler(message: types.Message):
    user_id = message.from_user.id
    state = database.get_state(user_id)
    await message_adder(message, state)
    database.save_state(state)
    
    
    # regexp emails
    # buttons
    # change message


def get_emails(message: str):
    return re.findall(r'[\w\.-]+@[\w-]+\.[\w-]{2,4}', message)


async def message_adder(message: types.Message, state: database.State): # e-mail adders
    message_with_emails = message.text
    e_mails = get_emails(message_with_emails)
    no_lead_emails = []
    bad_emails = []
    for email in e_mails:
        contacts = api.get_contacts_by_email(email)
        if len(contacts) == 0:
            bad_emails.append(email)
            continue

        is_ok = False
        for contact in contacts:
            links = api.get_contact_links(contact.get_id())
            lead_id = links.get_first_lead_id()
            if lead_id is not None:
                state.add_email(email, contact.get_id(), lead_id)
                is_ok = True
                break

        if not is_ok:
            no_lead_emails.append(email)
    
    create_bad_emails_message(bad_emails, no_lead_emails)


def create_bad_emails_message(bad_emails, no_lead_emails):
    result = ''
    if len(bad_emails) > 0:
        bad_emails_message = '\n'.join(bad_emails)
        result += f'Не найдены:\n {bad_emails_message}'
    if len(no_lead_emails) > 0:
        no_lead_emails_message = '\n'.join(no_lead_emails)
        result += f'\n\nНе найдены сделки:\n {no_lead_emails_message}'
    return result

@dp.message_handler(content_types=['text'])
async def e_mail_taker(message: types.Message):
    if message.text != 'стоп':
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        user_full_name = message.from_user.full_name
        
        dict_of_values = {}

        global DATA_DICT

        DATA_DICT['Менеджер'] = ''
        DATA_DICT['Ссылка на сделку'] = ''
        DATA_DICT['Дата заявки'] = ''
        DATA_DICT['Дата оплаты'] = ''
        DATA_DICT['Стоимость курса'] = ''
        DATA_DICT['Приход ДС'] = ''
        DATA_DICT['Статус'] = ''
        DATA_DICT['К доплате'] = ''
        
        dict_of_values['Имя'] = user_full_name
        for index, searching_item in enumerate(message.text.split()):
            if "@" in searching_item:
                dict_of_values['E-mail'] = searching_item
            elif 'сумму' in searching_item:
                DATA_DICT['Приход ДС'] = message.text.split()[index+1]

        if len(list_of_dicts_bot) > 0:
            for item in list_of_dicts_bot:
                if item['Имя'] == dict_of_values['Имя']:
                    item['E-mail'] += " " + dict_of_values['E-mail']
                else:
                    list_of_dicts_bot.append(dict_of_values)
        else:
            list_of_dicts_bot.append(dict_of_values)
            
        logging.info(f'{user_id}{user_name} {time.asctime()}')
        print(list_of_dicts_bot)
        await message.reply('Забрал это сообщение')
    else:
        await message.reply('Отправил на данные на обработку. Скоро пришлю эксель файл.')
        # for item in list_of_dicts_bot:
        #     db.set(item['Имя'], item['E-mail'].split())
        for mail_list in list_of_dicts_bot:

            api = Api()

            for mail in mail_list['E-mail'].split():
                

                
                resp = api.get_contacts_by_email(mail)
                
                
                if len(resp) == 0:
                    print("Не нашёл e-mail: ", mail)
                    continue

                for contact in resp:
                    
                    lead_id = api.get_contact_links(contact.get_id())
                    
                    if lead_id.is_empty():
                        continue

                    lead = api.get_lead(lead_id.get_first_lead_id())

                    lead_custom_fields = lead.get_custom_fields()

                    DATA_DICT['Менеджер'] = lead.get_responsable()
                    DATA_DICT['Ссылка на сделку'] = lead.get_lead_url()
                    DATA_DICT['Дата заявки'] = lead.get_creation_date()
                    print(DATA_DICT['Ссылка на сделку'])
                    DATA_DICT['Дата оплаты'] = lead.get_closed_date()
                    if lead_custom_fields.is_exist('Осталось оплатить'):
                        DATA_DICT['Стоимость курса'] = lead.get_price() + lead.get_custom_fields().get_value('Осталось оплатить')
                    else:
                        DATA_DICT['Стоимость курса'] = lead.get_price()
                    
                    status = lead.get_custom_fields().get_value('Способ оплаты')
                    status_tip_oplaty = lead.get_custom_fields().get_value('Тип оплаты')
                    if status in list_of_statuses:
                        DATA_DICT['Статус'] = 'Брокер'
                    else:
                        DATA_DICT['Статус'] = status_tip_oplaty
                    if lead.get_custom_fields().is_exist('Осталось оплатить'):
                        DATA_DICT['К доплате'] = lead.get_custom_fields().get_value('Осталось оплатить')
                    else:
                        DATA_DICT['К доплате'] = 0

                    print(DATA_DICT)
                    pd_list.append(DATA_DICT)
                    DATA_DICT = {}
                    print(f'{mail} is Ok')

        df = DataFrame(pd_list)
        df.to_excel('Отчет.xlsx', sheet_name="sheet2", index=False)

        with open('Отчет.xlsx', 'rb') as misc:
            await bot.send_document(message.chat.id, misc)
        

if __name__ == '__main__':
    executor.start_polling(dp)
    
    
