from datetime import date, timedelta
from loader import session
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from models.serializers import Service, Master, Date
from states.user import UserDialog, RegisterUser
from filters.base import is_button_selected
from keyboards.menu.kbds import request_phone_button_kbd


async def cancel(c: CallbackQuery, b: Button, d: DialogManager):
    await c.message.delete()
    await c.message.answer(text=f"Действие отменено.")
    await d.mark_closed()
    await d.data['state'].reset_state(with_data=True)


async def erase_widget_data(c: CallbackQuery, b: Button, d: DialogManager):
    d.data['aiogd_context'].widget_data = {}
    await d.switch_to(UserDialog.start)


async def switch_date(c: CallbackQuery, b: Button, d: DialogManager):
    prev_start = date.fromisoformat(d.data['aiogd_context'].widget_data['start_date'])
    if b.widget_id == "next_range":
        d.data['aiogd_context'].widget_data['start_date'] = str(prev_start + timedelta(days=8))
    elif b.widget_id == 'back_range':
        if prev_start <= date.fromisoformat(d.data['aiogd_context'].widget_data['earliest_date']):
            await c.answer("Не получится записаться раньше 😕")
        else:
            d.data['aiogd_context'].widget_data['start_date'] = str(prev_start - timedelta(days=8))
    await d.switch_to(d.data['aiogd_context'].state)


@is_button_selected(key='r_datetime')
async def apply_order(c: CallbackQuery, b: Button, d: DialogManager):
    widget_data = d.data['aiogd_context'].widget_data
    service_group_id = widget_data['r_service_group']
    service_id = int(widget_data['r_service'])
    date_id = widget_data['r_date']
    datetime_id = widget_data['r_datetime']
    master_id = widget_data['r_master']
    date_obj = Date.fromisoformat(date_id)
    service_json = session.get("https://dikidi.app/mobile/ajax/newrecord/company_services/",
                               params={"lang": "RU", "company": 17280,
                                       "master": master_id}).json()['data']['list']
    master_json = session.get("https://dikidi.app/ru/mobile/ajax/newrecord/get_datetimes",
                              params={"lang": "RU", "company_id": 17280, "service_id[]": service_id,
                                      "date": date_id, "master_id": master_id}).json()['data']
    services = {service_group['id']: [Service(service) for service in service_group['services']]
                for service_group in service_json.values()}
    item = [item for item in services[service_group_id]
            if item.id == service_id][0]
    master = Master(master_json['masters'][widget_data['r_master']])

    await d.data['state'].update_data({"item": item, "master": master,
                                       "date_obj": date_obj, "datetime": datetime_id})
    await c.message.delete()
    await c.message.answer(f"""Отлично! Вот детали заказа:
<strong>Услуга:</strong> {item.name}
<strong>Стоимость:</strong> {master.price}
<strong>Время:</strong> {date_obj.day} {date_obj.month_dict[date_obj.month]} ({date_obj.week_dict[date_obj.weekday()]}) {str(datetime_id[11:16])}
<strong>Продолжительность:</strong> {master.time}
<strong>Мастер:</strong> {master.name}""")
    await c.message.answer(f"""Если всё хорошо, то пожалуйста, нажми кнопку внизу, и я перешлю все детали администратору салона, он создаст заявку по номеру телефона и имени в Telegram. Если что-то не так - нажми на кнопку отмены, и всё отменится.""",
                           reply_markup=request_phone_button_kbd)
    await d.mark_closed()
    await RegisterUser.send_contact.set()


async def get_datetime(**kwargs):
    service_id = kwargs['aiogd_context'].widget_data['r_service']
    date_id = kwargs['aiogd_context'].widget_data['r_date']
    master_id = kwargs['aiogd_context'].widget_data['r_master']
    params = {"lang": "RU", "company_id": 17280,
              "date": date_id, "service_id[]": service_id}
    json = session.get("https://dikidi.app/ru/mobile/ajax/newrecord/get_datetimes/",
                       params=params).json()['data']['times'][master_id]
    datetimes = [(item[11:16], item) for item in json]
    return {"datetimes": datetimes}
