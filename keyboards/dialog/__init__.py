from loader import dp
from aiogram_dialog import DialogRegistry
from keyboards.dialog.user_base_dialog import user_dialog

registry = DialogRegistry(dp)
registry.register(user_dialog)
