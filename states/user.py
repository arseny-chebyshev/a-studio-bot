from aiogram.dispatcher.filters.state import StatesGroup, State


class UserDialog(StatesGroup):
    start = State()

    s_select_service_group = State()
    s_select_service = State()
    s_service_details = State()
    s_select_date = State()
    s_select_master = State()

    m_select_master = State()
    m_select_service_group = State()
    m_select_service = State()
    m_select_service_details = State()
    m_select_date = State()

    select_datetime = State()


class RegisterUser(StatesGroup):
    send_contact = State()
