# Доповніть програму-банкомат з попереднього завдання
# таким функціоналом, як використання банкнот.
# Отже, у банкоата повинен бути такий режим як "інкасація",
# за допомогою якого в нього можна "загрузити" деяку
# кількість банкнот (вибирається номінал і кількість).
# Зняття грошей з банкомату повинно відбуватись в межах
# наявних банкнот за наступним алгоритмом - видається
# мініальна кількість банкнот наявного номіналу. P.S.
# Будьте обережні з використанням "жадібного" алгоритму
# (коли вибирається спочатку найбільша банкнота, а потім
# - наступна за розміром і т.д.) - в деяких випадках він
# працює неправильно або не працює взагалі. Наприклад,
# якщо треба видати 160 грн., а в наявності є банкноти
# номіналом 20, 50, 100, 500, банкомат не зможе видати
# суму (бо спробує видати 100 + 50 + (невідомо), а
# потрібно було 100 + 20 + 20 + 20 ).
# 
# Особливості реалізаціі:
# - перелік купюр: 10, 20, 50, 100, 200, 500, 1000;
# - у одного користувача повинні бути права "інкасатора".
# Відповідно і у нього буде своє власне меню із пунктами:
# - переглянути наявні купюри;
# - змінити кільксть купюр;
# - видача грошей для користувачів відбувається в межах
# наявних купюр;
# - якщо гроші вносяться на рахунок - НЕ ТРЕБА їх
# розбивати і вносити в банкомат - не ускладнюйте собі
# життя, та й, наскільки я розумію, банкомати все, що в
# нього входить, відкладає в окрему касету.

import json

def users():
	user1 = {'login': 'Alex', 'password': '1111'}
	user2 = {'login': 'Anna', 'password': '2222'}
	user3 = {'login': 'Mark', 'password': '3333'}
	user4 = {'login': 'agent', 'password': 'agent'}
	users = [user1, user2, user3, user4]
	filename = 'users.data'
	with open(filename, 'w') as f:
		json.dump(users, f)

def balance():
	balance1 = 0
	filename = 'Alex_balance.data'
	with open(filename, 'w') as f:
		json.dump(balance1, f)
	balance2 = 100
	filename = 'Anna_balance.data'
	with open(filename, 'w') as f:
		json.dump(balance2, f)
	balance3 = 1000
	filename = 'Mark_balance.data'
	with open(filename, 'w') as f:
		json.dump(balance3, f)

def bank():
	filename = 'banknotes.data'
	with open(filename, 'r+') as f:
		banknotes = json.load(f)
		if not banknotes:
			banknotes = {'10': 0, '20': 5, '50': 5, '100': 3, '200': 10, '500': 1, '1000': 1}
			with open(filename, 'w') as f:
				banknotes = json.dump(f)
	return banknotes					
	
def get_load():
	load = {}
	while True:
		par = input('Enter par (empty enter - exit):')
		if par == '':
			break
		quantity = int(input('Enter quantity:'))
		load[par] = quantity
	return load
		
def login_check(login):
	filename = 'users.data'
	with open(filename) as f:
		users = json.load(f)
	for user in users:
		if login == user['login']:
			return user	

def password_check(login, password):
	if not login:
		return 
	if password == login['password']:
		return True
	
def check_balance(user):
	filename = str(user['login']) + '_balance.data'
	with open(filename) as f:
		balance = json.load(f)
	return balance

def sort(summ):
	summ_banknotes = 10 * banknotes['10'] + 20 * banknotes['20'] + 50 * banknotes['50'] + 100 * banknotes['100'] + 200 * banknotes['200'] + 500 * banknotes['500'] + 1000 * banknotes['1000']
	sorted = {'10': 0, '20': 0, '50': 0, '100': 0, '200': 0, '500': 0, '1000': 0}
	if summ_banknotes - summ >= 0:
		if banknotes['1000'] > 0:
			n1000 = summ // 1000
			if n1000 <= banknotes['1000']:
				sorted.update('1000', n1000)
			else:
				n1000 = banknotes['1000']
				sorted.update('1000', n1000)
			summ = summ - 1000 * n1000
			if summ % 500 != 0 and summ % 200 != 0 and summ % 100 != 0 and summ % 50 != 0 and summ % 20 != 0 and summ % 10 != 0:
				n1000 = 0
				summ = summ - 1000 * n1000
				sorted.update('1000', n1000)
			banknotes.update('1000', -n1000)
		if banknotes['500'] >= 0:
			n500 = summ // 500
			if n500 <= banknotes['500']:
				sorted.update('500', n500)
			else:
				n500 = banknotes['500']
				sorted.update('500', n500)
			summ = summ - 500 * n500
			if summ % 200 != 0 and summ % 100 != 0 and summ % 50 != 0 and summ % 20 != 0 and summ % 10 != 0:
				n500 = 0
				summ = summ - 500 * n500
				sorted.update('500', n500)	
			banknotes.update('500', -n500)
		if banknotes['200'] >= 0:
			n200 = summ // 200
			if n200 <= banknotes['200']:
				sorted.update('200', n200)
			else:
				n200 = banknotes['200']
				sorted.update('200', n200)
			summ = summ - 200 * n200
			if summ % 100 != 0 and summ % 50 != 0 and summ % 20 != 0 and summ % 10 != 0:
				n200 = 0
				summ = summ - 200 * n200
				sorted.update('200', n200)
			banknotes.update('200', -n200)
		if banknotes['100'] >= 0:
			n100 = summ // 100
			if n100 <= banknotes['100']:
				sorted.update('100', n100)
			else:
				n100 = banknotes['100']
				sorted.update('100', n100)
			summ = summ - 100 * n100
			if summ % 50 != 0 and summ % 20 != 0 and summ % 10 != 0:
				n100 = 0
				summ = summ - 100 * n100
				sorted.update('100', n100)
			banknotes.update('100', -n100)
		if banknotes['50'] >= 0:
			n50 = summ // 50
			if n50 <= banknotes['50']:
				sorted.update('50', n50)
			else:
				n50 = banknotes['50']
				sorted.update('50', n50)
			summ = summ - 50 * n50
			if summ % 20 != 0 and summ % 10 != 0:
				n50 = 0
				summ = summ - 50 * n50
				sorted.update('50', n50)
			banknotes.update('50', -n50)
		if banknotes['20'] >= 0:
			n20 = summ // 20
			if n20 <= banknotes['20']:
				sorted.update('20', n20)
			else:
				n20 = banknotes['20']
				sorted.update('20', n20)
			summ = summ - 20 * n20
			if summ % 10 != 0:
				n20 = 0
				summ = summ - 20 * n20
				sorted.update('20', n20)
			banknotes.update('20', -n20)	
		if banknotes['10'] >= 0:
			n10 = summ // 10
			if n10 <= banknotes['10']:
				sorted.update('10', n10)
			else:
				n10 = banknotes['10']
				sorted.update('10', n10)
			summ = summ - 10 * n10
			banknotes.update('10', -n10)
		print(f"You got 10: {sorted['10']}, 20: {sorted['20']}, 50: {sorted['50']}, 100: {sorted['100']}, 200: {sorted['200']}, 500: {sorted['500']}, 1000: {sorted['1000']}.")	
	else:
		print('The ATM does not have this amount of funds.')			

def withdraw(user, summ):
	filename = str(user['login']) + '_balance.data'
	with open(filename) as f:
		balance = json.load(f)	
	digit = summ.isdigit()
	if digit:
		summ = int(summ)
		if summ > 0:
			if balance - summ >= 0:
				if sort(summ):
					balance = balance - summ
					with open(filename, 'w') as f:
						json.dump(balance, f)
					return '\nYou withdrew ' + str(summ) + '.'
			else:
				return '\nNot enough money!'
		else:
			print('\nEnter a positive number!')    

def replenishment(user, summ):
	filename = str(user['login']) + '_balance.data'
	with open(filename) as f:
		balance = json.load(f)
	digit = summ.isdigit()
	if digit:
		summ = int(summ)
		if summ	> 0:
			balance = balance + summ
			with open(filename, 'w') as f:
				json.dump(balance, f)
			return '\nYou have deposited the amount ' + str(summ) + '.'
		else:
			return '\nEnter a positive number!'

def user_choice(choice, user):
	if choice == 1:
		print(f'\nYour balance: {check_balance(user)}.')
	elif choice == 2:
		summ = input('\nAmount to be withdraw:')
		trans = withdraw(user, summ)
		filename = str(user['login']) + '_transactions.data'
		with open(filename, 'w') as f:
			json.dump(summ, f)
			f.write('\n')
		print(trans)
	elif choice == 3:
		summ = input('\nEnter the replenishment sum:')
		trans = replenishment(user, summ)
		filename = str(user['login']) + '_transactions.data'
		with open(filename, 'w') as f:
			json.dump(summ, f)
			f.write('\n')
		print(trans)     

def agent_choice(choice):
	if choice == 1:
		print(f'\nThe set of banknotes: {bank()}.')
	elif choice == 2:
		banknotes.update(get_load())
		filename = 'banknotes.data'
		with open(filename, 'w') as f:
				json.dump(banknotes, f)
		print('\nYou have change the number of banknotes. \nThe set of banknotes: {banknotes}.')

def start():
	users()
	balance()
	bank()
	login_test = str(input('Enter login: '))
	user = login_check(login_test)
	password_test = str(input('Enter password: '))
	if password_check(user, password_test):
		if user['login'] == agent:
			while True:
				choice = int(input('\nSelect item:\n1. Check set of banknotes.\n2. Change the number of banknotes.\n3. Exit.\n\nYour choice: '))
				if choice == 3:
					break
				agent_choice(choice)
		else:
			while True:
				choice = int(input('\nSelect item:\n1. Check balance.\n2. Withdraw money.\n3. Deposit cash.\n4. Exit.\n\nYour choice: '))
				if choice == 4:
					break
				user_choice(choice, user)
	else:
		print(f'User not found!')

start()
