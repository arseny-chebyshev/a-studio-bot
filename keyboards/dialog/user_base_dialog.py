import operator
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Radio, Button, Group
from aiogram_dialog.widgets.text import Format, Const
from keyboards.dialog.base_dialog_buttons import cancel_button, continue_button, default_nav
from keyboards.dialog.user_service_dialog import service_keyboards, select_service_group
from keyboards.dialog.user_master_dialog import master_keyboards, select_master
from keyboards.dialog.actions import apply_order, get_datetime
from states.user import UserDialog

start_keyboard = Window(Const("""Пожалуйста, выбери способ записи с помощью кнопок ниже:"""),
                        Group(Button(Const("💅Найти услугу"),
                                     id="find_service", on_click=select_service_group),
                              Button(Const("👱‍♀️Найти мастера"),
                                     id="find_master", on_click=select_master),
                              cancel_button,
                              width=2),
                        state=UserDialog.start)

datetime_keyboard = Window(Const("Выбери подходящее время:"),
                           Group(Radio(Format("✅ {item[0]}"),
                                       Format("🕘 {item[0]}"),
                                       id="r_datetime", items='datetimes',
                                       item_id_getter=operator.itemgetter(1)),
                                 width=2),
                           Button(continue_button,
                                  on_click=apply_order,
                                  id='continue'),
                           default_nav,
                           getter=get_datetime,
                           state=UserDialog.select_datetime)


user_dialog = Dialog(start_keyboard, *service_keyboards, *master_keyboards, datetime_keyboard)
