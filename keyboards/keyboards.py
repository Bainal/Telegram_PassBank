import aiogram
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_reply_keyboard() -> aiogram.types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Показать пароли")
    builder.button(text="Добавить пароль")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_entering_data_inline_keyboard(
    service_name: str, login: str, password: str
) -> aiogram.types.InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=("Площадка" if service_name == None else service_name),
                callback_data="entering_service_name",
            )
        ],
        [
            InlineKeyboardButton(
                text=("Логин" if login == None else login),
                callback_data="entering_login",
            )
        ],
        [
            InlineKeyboardButton(
                text=("Пароль" if password == None else password),
                callback_data="entering_password",
            )
        ],
        [
            InlineKeyboardButton(text="Выход", callback_data="exit_cb"),
            InlineKeyboardButton(text="Сохранить", callback_data="save_cb"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_show_password_inline_keyboard(
    buttons_texts: list, buttons_callbacks: list, current_page: int, total_pages: int
) -> aiogram.types.InlineKeyboardMarkup:
    buttons = []
    # for i in range(0, len(buttons_texts)):
    #     if i % 2 == 0:
    #         buttons.append([InlineKeyboardButton(text=f"{buttons_texts[i]}", callback_data=f"{buttons_callbacks[i]}")])
    #     else:
    #         buttons[len(buttons) - 1].append(InlineKeyboardButton(text=f"{buttons_texts[i]}", callback_data=f"{buttons_callbacks[i]}"))

    # if len(buttons_texts) % 2 != 0:
    #     buttons[len(buttons) - 1].append(InlineKeyboardButton(text=" ", callback_data="non_clickable_cb"))

    for i in range(0, len(buttons_texts)):
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{buttons_texts[i]}", callback_data=f"{buttons_callbacks[i]}"
                )
            ]
        )

    temp = []
    if current_page != total_pages:
        if current_page != 1:
            temp.append(InlineKeyboardButton(text="Назад", callback_data="move_back_cb"))
        temp.append(
            InlineKeyboardButton(
                text=f"{current_page} / {total_pages}", callback_data="non_clickable_cb"
            )
        )
        if current_page != total_pages:
            temp.append(InlineKeyboardButton(text="Вперед", callback_data="move_next_cb"))
    buttons += [temp]
    buttons += [[InlineKeyboardButton(text="Выход", callback_data="exit_cb")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_password_inline_keyboard() -> aiogram.types.InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Назад", callback_data="back_cb"),
            InlineKeyboardButton(text="Удалить", callback_data="delete_cb"),
            InlineKeyboardButton(text="Изменить", callback_data="change_cb"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_confirmation_inline_keyboard() -> aiogram.types.InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Нет", callback_data="answer_no_cb"),
            InlineKeyboardButton(text="Да", callback_data="answer_yes_cb"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
