import re
from pathlib import Path
import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram_dialog import DialogManager
from aiogram.types import Message, ReplyKeyboardRemove
from settings import post_channel
from states.user import UserDialog, RegisterUser
from loader import dp


@dp.message_handler(state=RegisterUser.send_contact, content_types=aiogram.types.ContentType.CONTACT)
async def process_contact(msg: Message, state: FSMContext):
    data = await state.get_data()
    item = data['item']
    master = data['master']
    date_obj = data['date_obj']
    datetime_id = data['datetime']
    await dp.bot.send_message(chat_id=post_channel,
                              text=f"""<strong>Услуга:</strong> {item.name}
<strong>Стоимость:</strong> {master.price}
<strong>Время:</strong> {date_obj.day} {date_obj.month_dict[date_obj.month]} ({date_obj.week_dict[date_obj.weekday()]}) {str(datetime_id[11:16])}
<strong>Продолжительность:</strong> {master.time}
<strong>Мастер:</strong> {master.name}""")
    await msg.forward(chat_id=post_channel)
    await msg.answer("Спасибо! Запись была оформлена. За день до встречи придёт СМС-напоминание на указанный номер.",
                     reply_markup=ReplyKeyboardRemove())
    await state.reset_state(with_data=True)


@dp.message_handler(Text(equals=["❌ Отмена"]), state=RegisterUser.send_contact)
async def cancel_record(msg: Message, state: FSMContext):
    await msg.answer("Запись отменена.", reply_markup=ReplyKeyboardRemove())
    await state.reset_state(with_data=True)


@dp.message_handler(state=RegisterUser.send_contact)
async def require_push(msg: Message, state: FSMContext):
    await msg.answer("Пожалуйста, нажми на одну из кнопок. Я не смогу продолжать диалог дальше, пока они тут 😓")


@dp.message_handler(commands=["start"], state=None)
async def start(msg: Message):
    await msg.answer("""👋Привет! Я - бот для записи в салон красоты "A-Studio". Воспользуйся командами ниже, чтобы узнать, что я умею.
/service - записаться на услугу или к определённому мастеру
/help - узнать ответы на часто задаваемые вопросы""")


@dp.message_handler(commands=['service'], state=None)
async def select_service(msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserDialog.start)


@dp.message_handler(commands=['help'], state=None)
async def show_help(msg: Message):
    h = Path(__file__).with_name('help.txt')
    with h.open('r', encoding='utf-8') as response:
        await msg.answer(response.read(), reply_markup=ReplyKeyboardRemove())
        response.close()


@dp.message_handler(Text(equals=["привет!", "привет", "здравствуйте", "добрый день", "👋", "🙋‍♂️", "🙋‍♀️"], ignore_case=True), state=None)
async def hello(msg: Message):
    await msg.answer("""👋Привет! Я - бот для записи в салон красоты "A-Studio". Воспользуйся командами ниже, чтобы узнать, что я умею.
/service - записаться на услугу или к определённому мастеру
/help - узнать ответы на часто задаваемые вопросы""")


@dp.message_handler(regexp=re.compile('как.*дела.*', re.IGNORECASE), state=None)
async def answer_how_are_you(msg: Message):
    await msg.answer("Да ничего, понемногу развиваюсь. Скоро мне добавят крутых функций, и я буду самым крутым помощником на свете! Спасибо, что интересуешься!")


@dp.message_handler(regexp=re.compile('(.*записаться.*|.*ногти.*|.*маникюр.*|.*сколько.*)', re.IGNORECASE), state=None)
async def info_service(msg: Message):
    await msg.answer("Чтобы записаться к нам, а также узнать информацию о ценах, окошках и свободных мастерах, используй команду /service.")
