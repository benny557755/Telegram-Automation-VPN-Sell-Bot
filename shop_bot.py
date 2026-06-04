import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto

# --- Setup ---
TOKEN = "8844577576:AAEryF2SfwYtSqa0QyaoBmPBSaJw4zxNy4A" 
ADMIN_ID = 8547338616 

bot = Bot(token=TOKEN)
dp = Dispatcher()

class VPNOrder(StatesGroup):
    choosing_plan = State()
    waiting_for_payment = State()
    waiting_for_admin_key = State() 

# --- Keyboards ---

def main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="VPN ဝယ်ရန် 🛒", callback_data="buy_vpn"))
    builder.row(types.InlineKeyboardButton(text="အသုံးပြုနည်း လမ်းညွှန် 📖", callback_data="how_to_use"))
    builder.row(types.InlineKeyboardButton(text="Admin ဆက်သွယ်ရန် 📞", url="https://t.me/benny875"))
    return builder.as_markup()

def plans_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="၁ လ - ၄၀၀၀ ကျပ်", callback_data="plan_1month"))
    builder.row(types.InlineKeyboardButton(text="၂ လ - ၇၀၀၀ ကျပ်", callback_data="plan_2months"))
    builder.row(types.InlineKeyboardButton(text="နောက်သို့ 🔙", callback_data="back_home"))
    return builder.as_markup()

# --- Handlers ---

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"မင်္ဂလာပါ {message.from_user.first_name}!\nမြန်ဆန်စိတ်ချရတဲ့ VPN ဝန်ဆောင်မှုမှ ကြိုဆိုပါတယ်။",
        reply_markup=main_menu()
    )

@dp.callback_query(F.data == "back_home")
async def back_home(callback: types.CallbackQuery):
    await callback.message.edit_text("ပင်မစာမျက်နှာသို့ ပြန်ရောက်ပါပြီ။", reply_markup=main_menu())

@dp.callback_query(F.data == "buy_vpn")
async def buy_vpn_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("ဝယ်ယူလိုသည့် သက်တမ်းကို ရွေးချယ်ပေးပါ -", reply_markup=plans_menu())
    await callback.answer()

@dp.message(F.text == "/buy")
async def menu_buy(message: types.Message):
    await message.answer("ဝယ်ယူလိုသည့် သက်တမ်းကို ရွေးချယ်ပေးပါ -", reply_markup=plans_menu())

@dp.callback_query(F.data.startswith("plan_"))
async def show_payment(callback: types.CallbackQuery, state: FSMContext):
    plan = "၁ လ (၄၀၀၀ ကျပ်)" if callback.data == "plan_1month" else "၂ လ (၇၀၀၀ ကျပ်)"
    await state.update_data(selected_plan=plan)
    
    payment_text = (
        f"✅ သင်ရွေးချယ်ထားသော Plan: {plan}\n\n"
        "💰 **ငွေပေးချေရန် အချက်အလက်**\n"
        "KBZPay: 09682335618 (Name: Aung Lin Phyo)\n\n"
        "ငွေလွှဲပြီးပါက ငွေလွှဲပြေစာ (Screenshot) ကို ပို့ပေးပါ။"
    )
    await callback.message.answer(payment_text)
    await state.set_state(VPNOrder.waiting_for_payment)
    await callback.answer()

# ၂။ Screenshot လက်ခံခြင်း
@dp.message(VPNOrder.waiting_for_payment, F.photo)
async def handle_payment_ss(message: types.Message, state: FSMContext):
    data = await state.get_data()
    customer_id = message.from_user.id
    
    admin_kb = InlineKeyboardBuilder()
    admin_kb.add(types.InlineKeyboardButton(text="Key ပေးမည် 🔑", callback_data=f"givekey_{customer_id}"))

    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=f"🔔 **Order အသစ်!**\nPlan: {data.get('selected_plan')}\nUser: {message.from_user.full_name}\nID: `{customer_id}`",
        reply_markup=admin_kb.as_markup()
    )
    await message.answer("ငွေလွှဲပြေစာ ရရှိပါပြီ။ Admin မှ စစ်ဆေးပြီး VPN Key ကို ပို့ပေးပါလိမ့်မည်။")
    await state.clear()

# ၃။ Admin အပိုင်း
@dp.callback_query(F.data.startswith("givekey_"))
async def admin_ask_key(callback: types.CallbackQuery, state: FSMContext):
    cust_id = callback.data.split("_")[1]
    await state.update_data(target_user=cust_id)
    await callback.message.answer(f"User `{cust_id}` အတွက် VPN Key ကို ရိုက်ထည့်ပါ။")
    await state.set_state(VPNOrder.waiting_for_admin_key)
    await callback.answer()

@dp.message(VPNOrder.waiting_for_admin_key)
async def admin_send_key_to_user(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return 
    
    data = await state.get_data()
    user_id = data.get('target_user')
    vpn_key = message.text

    try:
        await bot.send_message(
            chat_id=user_id,
            text=f"✅ **သင့်ရဲ့ VPN Key ရရှိပါပြီ!**\n\nKey: `{vpn_key}`\n\nအသုံးပြုနည်းလမ်းညွှန်အတိုင်း ချိတ်ဆက်အသုံးပြုနိုင်ပါပြီ။"
        )
        await message.answer(f"User `{user_id}` ထံသို့ Key ပို့ပြီးပါပြီ။")
        await state.clear()
    except Exception as e:
        await message.answer(f"Error: {e}")

# --- Guide  ---
@dp.callback_query(F.data == "how_to_use")
async def vpn_guide_callback(callback: types.CallbackQuery):
    await send_guide(callback.message)
    await callback.answer()

@dp.message(F.text == "/help")
async def menu_help(message: types.Message):
    await send_guide(message)

async def send_guide(message: types.Message):
    await message.answer("VPN ချိတ်ဆက်နည်း လမ်းညွှန်ပုံများကို ပို့ပေးနေပါသည်။ ခေတ္တစောင့်ပါ။")
    
    # 
    media = [
        InputMediaPhoto(media="AgACAgUAAxkBAAM2agV7dAF5GuWjUiCgL--ifcXB1lsAAjwPaxsL5yhUpOwU5_8E6gMBAAMCAAN5AAM7BA", caption="အဆင့် ၁ - App ကိုဖွင့်ပါ"),
        InputMediaPhoto(media="AgACAgUAAxkBAAM4agV7kSCbUzQ4wikKggOj_7iRQUoAArAOaxviWihUnTOErnxTcHwBAAMCAAN5AAM7BA", caption="အဆင့် ၂ - + လေးကိုနှိပ်လိုက်ပါ"),
        InputMediaPhoto(media="AgACAgUAAxkBAAM6agV7qfe0Fhm-o9mf_Jr8Vo8Cs_wAAj0PaxsL5yhUTCP2t1seJwQBAAMCAAN4AAM7BA" , caption ="အဆင့် ၃ - Copy Config from clipboard ဆိုတာကိုနှိပ်လိုက်ပါ"),
        InputMediaPhoto(media="AgACAgUAAxkBAAM8agV7tuVZuf0yUMbn13Qne3BWIUsAArIOaxviWihUzFxzxCijJAoBAAMCAAN5AAM7BA", caption="အဆင့် ၄ - Connect ကိုနှိပ်ပြီး သုံးနိုင်ပါပြီ")
    ]
    try:
        await bot.send_media_group(chat_id=message.chat.id, media=media)
    except Exception as e:
        await message.answer(f"ပုံပို့ရာတွင် အမှားအယွင်းရှိနေပါသည်: {e}")

# --- Start Up ---
async def main():
    logging.basicConfig(level=logging.INFO)
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Bot ကို ပြန်စတင်ရန်"),
        types.BotCommand(command="buy", description="VPN ဝယ်ယူရန်"),
        types.BotCommand(command="help", description="အသုံးပြုနည်း လမ်းညွှန်")
    ])
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())