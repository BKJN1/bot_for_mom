import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from aiogram.types import FSInputFile

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# -------------------------------
# Товары
# -------------------------------
products = {
    "Халаты": [
        {"name": "Туркменский махровый халат (48, молочный)", "price": "10 000 ₸", "photo": "images/zen-renkler-1-scaled.jpg"},
        {"name": "Туркменский махровый халат (48, бирюза)", "price": "10 000 ₸", "photo": "images/zen-renkler-1-scaled.jpg"},
        {"name": "Туркменский махровый халат (54, молочный)", "price": "10 000 ₸", "photo": "images/zen-renkler-1-scaled.jpg"},
    ],
    "Полотенце": {
        "name": "Полотенце для рук (40x70, цвета разные)",
        "price": "550 ₸",
        "photo": "images/zen-renkler-1-scaled.jpg",
        "colors": ["Белый", "Серый", "Синий", "Розовый"]
    },
    "Носки": {
        "name": "Носки детские (2–4 года)",
        "price": "220 ₸",
        "photo": "images/zen-renkler-1-scaled.jpg",
        "colors": ["Синие", "Белые", "Красные"]
    }
}

# -------------------------------
# Клавиатуры
# -------------------------------
def main_menu():
    kb = [
        [KeyboardButton(text="🛍 Посмотреть товары")],
        [KeyboardButton(text="📞 Связаться с продавцом")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def products_menu():
    kb = [
        [KeyboardButton(text="Халаты")],
        [KeyboardButton(text="Полотенце для рук")],
        [KeyboardButton(text="Носки детские")],
        [KeyboardButton(text="⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def back_menu():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️ Назад")]], resize_keyboard=True)

def menu_button():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🏠 В меню")]], resize_keyboard=True)

# -------------------------------
# /start
# -------------------------------
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Здравствуйте! 👋\nЯ помогу вам оформить заказ.\nВыберите действие:",
        reply_markup=main_menu()
    )

# -------------------------------
# Связаться с продавцом
# -------------------------------
@dp.message(F.text == "📞 Связаться с продавцом")
async def contact_seller(message: types.Message):
    await message.answer(
        f"📞 Связаться с продавцом:\n\n"
        f"👤 Админ: @{(await bot.get_chat(ADMIN_ID)).username}\n"
        f"📱 Телефон: +7 777 777 77 77",
        reply_markup=back_menu()
    )

# -------------------------------
# Посмотреть товары
# -------------------------------
@dp.message(F.text == "🛍 Посмотреть товары")
async def show_categories(message: types.Message):
    await message.answer("Выберите категорию товаров:", reply_markup=products_menu())

# -------------------------------
# Халаты
# -------------------------------
# -------------------------------
# Халаты
# -------------------------------
@dp.message(F.text == "Халаты")
async def show_halats(message: types.Message):
    text = "🧥 Наши халаты:\n\n"
    for p in products["Халаты"]:
        text += f"• {p['name']} — {p['price']}\n"
    await message.answer(
        text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📸 Посмотреть фото халатов")],
                [KeyboardButton(text="🛒 Заказать халат")],
                [KeyboardButton(text="⬅️ Назад")]
            ],
            resize_keyboard=True
        )
    )

@dp.message(F.text == "📸 Посмотреть фото халатов")
async def show_halats_photos(message: types.Message):
    for p in products["Халаты"]:
        photo_file = FSInputFile(p["photo"])
        await message.answer_photo(photo_file, caption=f"{p['name']} — {p['price']}")
    await message.answer("Выберите другой раздел:", reply_markup=products_menu())

# 👉 Новое: выбор конкретного халата для заказа
@dp.message(F.text == "🛒 Заказать халат")
async def choose_halats_to_order(message: types.Message):
    kb = [[KeyboardButton(text=f"🛒 Заказать {p['name']}")] for p in products["Халаты"]]
    kb.append([KeyboardButton(text="⬅️ Назад")])
    await message.answer("Выберите нужный халат:", reply_markup=ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

# -------------------------------
# Полотенце
# -------------------------------
@dp.message(F.text == "Полотенце для рук")
async def show_towel(message: types.Message):
    p = products["Полотенце"]
    photo_file = FSInputFile(p["photo"])
    await message.answer_photo(
        photo_file,
        caption=f"{p['name']}\nЦена: {p['price']}",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🎨 Выбрать цвет полотенца")],
                [KeyboardButton(text=f"🛒 Заказать {p['name']}")],
                [KeyboardButton(text="⬅️ Назад")]
            ],
            resize_keyboard=True
        )
    )

@dp.message(F.text == "🎨 Выбрать цвет полотенца")
async def choose_towel_color(message: types.Message):
    colors = products["Полотенце"]["colors"]
    kb = [[KeyboardButton(text=f"🛒 Заказать Полотенце ({c})")] for c in colors]
    kb.append([KeyboardButton(text="⬅️ Назад")])
    await message.answer("Выберите цвет:", reply_markup=ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

# -------------------------------
# Носки
# -------------------------------
@dp.message(F.text == "Носки детские")
async def show_socks(message: types.Message):
    p = products["Носки"]
    photo_file = FSInputFile(p["photo"])
    await message.answer_photo(
        photo_file,
        caption=f"{p['name']}\nЦена: {p['price']}",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🎨 Выбрать цвет носков")],
                [KeyboardButton(text=f"🛒 Заказать {p['name']}")],
                [KeyboardButton(text="⬅️ Назад")]
            ],
            resize_keyboard=True
        )
    )

@dp.message(F.text == "🎨 Выбрать цвет носков")
async def choose_socks_color(message: types.Message):
    colors = products["Носки"]["colors"]
    kb = [[KeyboardButton(text=f"🛒 Заказать Носки ({c})")] for c in colors]
    kb.append([KeyboardButton(text="⬅️ Назад")])
    await message.answer("Выберите цвет:", reply_markup=ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

# -------------------------------
# Заказ товара
# -------------------------------
user_orders = {}  # временно хранит заказы (user_id: товар)

@dp.message(F.text.startswith("🛒 Заказать"))
async def order_item(message: types.Message):
    item = message.text.replace("🛒 Заказать ", "")
    user_orders[message.from_user.id] = item
    await message.answer("Пожалуйста, введите ваше имя:", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text.regexp(r"^[А-Яа-яA-Za-zёЁ\- ]+$"))
async def get_name(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_orders and not isinstance(user_orders[user_id], dict):
        user_orders[user_id] = {"item": user_orders[user_id], "name": message.text}
        await message.answer("Теперь отправьте ваш номер телефона (в формате +7...)")
    else:
        await message.answer("Введите корректное имя, пожалуйста.")

@dp.message(F.text.regexp(r"^\+?\d{10,13}$"))
async def get_phone(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_orders and isinstance(user_orders[user_id], dict):
        user_orders[user_id]["phone"] = message.text
        order = user_orders[user_id]

        # Сообщение админу
        order_text = (
            f"🆕 Новый заказ!\n\n"
            f"👤 Имя: {order['name']}\n"
            f"📱 Телефон: {order['phone']}\n"
            f"📦 Товар: {order['item']}\n"
            f"От пользователя: @{message.from_user.username or 'без юзернейма'}"
        )
        await bot.send_message(ADMIN_ID, order_text)

        # Сообщение пользователю
        await message.answer("✅ Спасибо! Ваш заказ принят. Мы скоро свяжемся с вами 🙌", reply_markup=menu_button())
        del user_orders[user_id]

# -------------------------------
# Назад и меню
# -------------------------------
@dp.message(F.text == "⬅️ Назад")
async def go_back(message: types.Message):
    await message.answer("Главное меню:", reply_markup=main_menu())

@dp.message(F.text == "🏠 В меню")
async def go_menu(message: types.Message):
    await message.answer("Вы в главном меню:", reply_markup=main_menu())

# -------------------------------
# Запуск
# -------------------------------
if __name__ == "__main__":
    dp.run_polling(bot)
