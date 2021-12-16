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
	filename1 = 'Alex_balance.data'
	with open(filename1, 'r') as f:
		balance1 = None
		try:
			json.load(f)
		except:
			pass
		if not balance1:
			balance1 = 0
			with open(filename1, 'w') as f:
				json.dump(balance1, f)		
	filename2 = 'Anna_balance.data'
	with open(filename2, 'r') as f:
		balance2 = None
		try:
			json.load(f)
		except:
			pass
		if not balance2:
			balance2 = 100
			with open(filename2, 'w') as f:
				json.dump(balance2, f)
	filename3 = 'Mark_balance.data'
	with open(filename3, 'r') as f:
		balance3 = None
		try:
			json.load(f)
		except:
			pass
		if not balance3:
			balance3 = 1000
			with open(filename3, 'w') as f:
				json.dump(balance3, f)

def bank():
	filename = 'banknotes.data'
	with open(filename) as f:
		banknotes = None
		try:
			banknotes = json.load(f)
		except:
			pass
		if not banknotes:	
			banknotes = {'10': 0, '20': 5, '50': 5, '100': 3, '200': 10, '500': 1, '1000': 1}
			with open(filename, 'w') as f:
				json.dump(banknotes, f)
	return banknotes					
	
def get_load():
	load = {}
	while True:
		par = input('Enter par (empty enter - exit): ')
		if par == '':
			break
		quantity = int(input('Enter quantity: '))
		load[par] = quantity
	return load
		
def login_check(login):
	filename = 'users.data'
	with open(filename) as f:
		users = json.load(f)
	for user in users:
		if login.lower() == user['login'].lower():
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
	filename = 'banknotes.data'
	with open(filename) as f:
		banknotes = json.load(f)
	summ_banknotes = 10 * banknotes['10'] + 20 * banknotes['20'] + 50 * banknotes['50'] + 100 * banknotes['100'] + 200 * banknotes['200'] + 500 * banknotes['500'] + 1000 * banknotes['1000']
	sort_summ = {}
	nom = [1000, 500, 200, 100, 50, 20, 10]
	for i in nom:
		if banknotes[str(i)] == 0:
			continue
		n = summ // i
		if banknotes[str(i)] < n:
			n = banknotes[str(i)]
		summ = summ - n * i
		if summ == 0:
			sort_summ.update({str(i): n})
			summ = 0
			cash = True
			break
		cash = False
		for j in nom:
			if j > i:
				if banknotes[str(j)] > 0:
					if summ % j == 0:
						cash = True
				if cash:				
					m = summ // j
					if banknotes[str(j)] < m and m > 0:
						m = banknotes[str(j)]
					sort_summ.update({str(j): m})
					summ = summ - m * j
				else:
					n = n - 1
	if summ > 0:
		print("Can't give a cash.")
	else:
		for k in sort_summ:
			banknotes.update({str(k): banknotes[str(k)] - sort_summ[str(k)]})
		with open(filename, 'w') as f:
			json.dump(banknotes, f)
	return cash		

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
		summ = input('\nAmount to be withdraw: ')
		trans = withdraw(user, summ)
		filename = str(user['login']) + '_transactions.data'
		with open(filename, 'w') as f:
			json.dump(summ, f)
			f.write('\n')
		print(trans)
	elif choice == 3:
		summ = input('\nEnter the replenishment sum: ')
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
		filename = 'banknotes.data'
		with open(filename) as f:
			banknotes = json.load(f)
		getload = get_load()	
		banknotes.update({'10': banknotes['10'] + getload['10'], '20': banknotes['20'] + getload['20'], '50': banknotes['50'] + getload['50'], '100': banknotes['100'] + getload['100'], '200': banknotes['200'] + getload['200'], '500': banknotes['500'] + getload['500'], '1000': banknotes['1000'] + getload['1000']})
		with open(filename, 'w') as f:
			json.dump(banknotes, f)
		print('\nYou have change the number of banknotes. \n\nThe set of banknotes: {banknotes}.')

def start():
	users()
	balance()
	bank()
	login_test = str(input('Enter login: '))
	user = login_check(login_test)
	password_test = str(input('Enter password: '))
	if password_check(user, password_test):
		if user['login'] == 'agent':
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
