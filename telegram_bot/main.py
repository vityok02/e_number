import telebot
import json
from telebot import types

bot = telebot.TeleBot("6876807033:AAGQ2Pl5zfwVC6w1VKnRNAChFNoOnz1Mnu0", parse_mode=None)

checked_numbers_file = open("checked_numbers.json", encoding="utf8")
checked_numbers = json.load(checked_numbers_file)
numbers_with_name_file = open("numbers_with_names.json", encoding="utf8")
numbers_with_names = json.load(numbers_with_name_file)
with open('unchecked_numbers.json', 'r') as f:
    unchecked_numbers = json.load(f)

@bot.message_handler(commands=['start'])
def send_welcome_message(message):
	bot.send_message(message.chat.id, "Привіт! Приступімо до роботи:😉")
	select_action(message)

def select_action(message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	check = types.KeyboardButton(text='Перевірити чи додати спам номер📞')
	html = types.KeyboardButton(text='Посилання на сайт "Є номер"💻')
	keyboard.add(check)
	keyboard.add(html)
	bot.send_message(message.chat.id, "Оберіть дію:🤔", reply_markup=keyboard)



@bot.message_handler(regexp="Перевірити чи додати спам номер📞")
def handle_message(message):
	msg = bot.send_message(message.chat.id, "Введіть номер для перевірки:✍")
	bot.register_next_step_handler(msg, check_number)

def find_number_index(checked_numbers, number_to_find, message):
	for item in checked_numbers['checked_numbers']:
		if number_to_find in item:
			n = item[number_to_find]
			if n == 5:
				danger_level = "Кримінальний"
			elif n == 4:
				danger_level = "Небезпечний"
			elif n == 3:
				danger_level = "Критичний"
			elif n == 2:
				danger_level = "Середній"
			elif n == 1:
				danger_level = "Безпечний"

	bot.send_message(message.chat.id, f"Цей номер є у нашій базі✅. Його рівень небезпеки: {danger_level}")

def check_number(message):
	number = str(message.text)
	if number in numbers_with_names:
		numbers = numbers_with_names[number]
		find_number_index(checked_numbers, number, message)
		bot.send_message(message.chat.id, f"Цей номер був також підписаний у користувачів як:\n ")
		bot.send_message(message.chat.id, '\n'.join(numbers))
		select_action(message)
	else:
		bot.send_message(message.chat.id, "Ми нічого не знаємо про цей номер🤷.\nМи його відправили на перевірку.")
		unchecked_numbers["numbers"].append(number)
		with open('unchecked_numbers.json', 'w') as f:
			json.dump(unchecked_numbers, f, indent='\n')
		select_action(message)


@bot.message_handler(regexp='Посилання на сайт "Є номер"💻')
def handle_message(message):
	menu1 = telebot.types.InlineKeyboardMarkup()
	menu1.add(telebot.types.InlineKeyboardButton(text='Сайт "Є номер"', url="https://enomer.netlify.app/"))
	bot.send_message(message.chat.id, text='Клацніть на посилання нижче:', reply_markup=menu1)
	select_action(message)

bot.polling(none_stop=True)