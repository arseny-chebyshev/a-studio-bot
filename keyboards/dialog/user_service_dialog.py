import operator
from datetime import date, timedelta
from filters.base import is_button_selected
from aiogram.types import CallbackQuery, Message
from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Radio, Button, Group, Back, Next, ManagedRadioAdapter
from aiogram_dialog.widgets.text import Format, Const
from loader import session
from models.serializers import Service, Date, Master
from states.user import UserDialog
from keyboards.dialog.base_dialog_buttons import cancel_button, continue_button, back_to_start_button, default_nav
from .actions import switch_date, apply_order


async def get_service_group(**kwargs):
    params = {"lang": "RU", "company": 17280}
    json = session.get("https://dikidi.app/mobile/ajax/newrecord/company_services",
                        params=params).json()
    services_raw = json['data']['list']
    service_groups = [(service_group['name'], int(service_group['id']))
                      for service_group in services_raw.values()]
    return {'service_groups': service_groups}


async def get_service(**kwargs):
    params = {"lang": "RU", "company": 17280}
    json = session.get("https://dikidi.app/mobile/ajax/newrecord/company_services",
                       params=params).json()
    services_raw = json['data']['list']
    services = {service_group['id']: [Service(service) for service in service_group['services']]
                for service_group in services_raw.values()}
    service_list = [(item, item.id)
                    for item in services[kwargs['aiogd_context'].widget_data['r_service_group']]]
    return {'services': service_list}


async def get_service_details(**kwargs):
    params = {"lang": "RU", "company": 17280}
    json = session.get("https://dikidi.app/mobile/ajax/newrecord/company_services",
                       params=params).json()
    services_raw = json['data']['list']
    services = {service_group['id']: [Service(service) for service in service_group['services']]
                for service_group in services_raw.values()}
    item = [item for item in services[kwargs['aiogd_context'].widget_data['r_service_group']]
            if item.id == int(kwargs['aiogd_context'].widget_data['r_service'])][0]
    return {"item": item}


async def get_date_range(**kwargs):
    service_id = kwargs['aiogd_context'].widget_data['r_service']
    params = {"lang": "RU", "company_id": 17280,
              "service_id[]": service_id}
    if not 'start_date' in kwargs['aiogd_context'].widget_data.keys():
        json = session.get("https://dikidi.app/ru/mobile/ajax/newrecord/get_datetimes",
                       params=params).json()
        start_date = date.fromisoformat(json['data']['date_near'])
        kwargs['aiogd_context'].widget_data['start_date'] = str(start_date)
        kwargs['aiogd_context'].widget_data['earliest_date'] = str(start_date)
        return await get_date_range(**kwargs)
    start_date = date.fromisoformat(kwargs['aiogd_context'].widget_data['start_date'])
    params['date'] = str(start_date)
    json = session.get("https://dikidi.app/ru/mobile/ajax/newrecord/get_datetimes",
                       params=params).json()
    date_objs = [Date.fromisoformat(item) for item in json['data']['dates_true']]
    dates = [(f"{item.day} {item.month_dict[item.month]} ({item.week_dict[item.weekday()]})",
              str(item)) for item in date_objs]
    return {"dates": dates}


async def get_master(**kwargs):
    service_id = kwargs['aiogd_context'].widget_data['r_service']
    date_id = kwargs['aiogd_context'].widget_data['r_date']
    params = {"lang": "RU", "company_id": 17280,
              "date": date_id, "service_id[]": service_id}
    master_list = [Master(item) for item in
                   session.get("https://dikidi.app/ru/mobile/ajax/newrecord/get_datetimes/",
                               params=params).json()['data']['masters'].values()]
    masters = [(f"{item.name}, {item.price}, {item.time}", item.id) for item in master_list]
    return {"masters": masters}


async def select_service_group(c: CallbackQuery, b: Button, d: DialogManager):
    await d.switch_to(UserDialog.s_select_service_group)


@is_button_selected(key='r_service_group')
async def select_service(c: CallbackQuery, b: Button, d: DialogManager):
    await d.switch_to(UserDialog.s_select_service)


@is_button_selected(key='r_service')
async def select_details(c: CallbackQuery, b: Button, d: DialogManager):
    await d.switch_to(UserDialog.s_service_details)


async def select_date(c: CallbackQuery, b: Button, d: DialogManager):
    await d.switch_to(UserDialog.s_select_date)


@is_button_selected(key='r_date')
async def select_master(c: CallbackQuery, b: Button, d: DialogManager):
    await d.switch_to(UserDialog.s_select_master)


@is_button_selected(key='r_master')
async def select_datetime(c: CallbackQuery, b: Button, d: DialogManager):
    await d.switch_to(UserDialog.select_datetime)


async def add_item(c: CallbackQuery, r: ManagedRadioAdapter, d: DialogManager, button_id: str):
    print(r.widget.widget_id)
    for group in c.values['message'].reply_markup['inline_keyboard']:
        for button in group:
            text = button['text']
            if text.startswith('✅'):
                print(text)


service_group_keyboard = Window(Const("Выбери категорию услуг:"),
                                Group(Radio(Format("✅ {item[0]}"),
                                      Format("🔘 {item[0]}"),
                                      id="r_service_group", items='service_groups',
                                      item_id_getter=operator.itemgetter(1)),
                                width=2),
                                Button(continue_button,
                                       on_click=select_service,
                                       id='continue'),
                                Group(back_to_start_button,
                                      cancel_button, width=2),
                                getter=get_service_group,
                                state=UserDialog.s_select_service_group)

service_keyboard = Window(Const("Выбери услугу:"),
                          Group(Radio(Format("✅ {item[0].name}"),
                                      Format("🔘 {item[0].name}"),
                                      id="r_service", items='services',
                                      item_id_getter=operator.itemgetter(1)),
                                width=1),
                          Button(continue_button,
                                 on_click=select_details,
                                 id='continue'),
                          default_nav,
                          getter=get_service,
                          state=UserDialog.s_select_service)

service_detail_keyboard = Window(Format("{item.name}: от {item.price}, {item.time} (окончательная цена и время будут известны при выборе свободного мастера)"),
                                 Button(Const("🔎 Выбрать время"),
                                        on_click=select_date,
                                        id='continue'),
                                 default_nav,
                                 getter=get_service_details,
                                 state=UserDialog.s_service_details)

date_keyboard = Window(Const("Выбери дату:"),
                       Group(Radio(Format("✅ {item[0]}"),
                                   Format("🗓 {item[0]}"),
                                   id="r_date", items='dates',
                                      item_id_getter=operator.itemgetter(1)),
                       width=2),
                       Group(Button(Const("Раньше"),
                                    id='back_range',
                                    on_click=switch_date),
                             Button(Const("Позже"),
                                    id='next_range',
                                    on_click=switch_date),
                             width=2),
                       Button(continue_button,
                              on_click=select_master,
                              id='continue'),
                       default_nav,
                       getter=get_date_range,
                       state=UserDialog.s_select_date)

master_keyboard = Window(Const("Выбери мастера:"),
                         Group(Radio(Format("✅ {item[0]}"),
                                     Format("🔘 {item[0]}"),
                                     id="r_master", items='masters',
                                     item_id_getter=operator.itemgetter(1)),
                               width=1),
                         Button(continue_button,
                                on_click=select_datetime,
                                id='continue'),
                         default_nav,
                         getter=get_master,
                         state=UserDialog.s_select_master)

service_keyboards = (service_group_keyboard,
                     service_keyboard, service_detail_keyboard,
                     date_keyboard, master_keyboard)
