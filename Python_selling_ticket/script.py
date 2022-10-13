ticket = int(input("Введите количество билетов, которое хотите приобрести "))
price = 0
price_ticket = 0
for i in range(1, ticket + 1):
    age = int(input(f"Введите возраст {i}-го посетителя "))
    if age < 18:
        price_ticket = 0
    elif 18 <= age < 25:
        price_ticket = 990
    else:
        price_ticket = 1390
    if ticket > 3:
        price = price_ticket - 10 * price_ticket // 100 + price
    else:
        price = price_ticket + price

print("Сумма к оплате", price)
