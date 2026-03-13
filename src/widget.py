def mask_account_card(input_string: str) -> str:
    """
    Маскирует номер банковской карты или счёта в зависимости от типа.
    """
    # Извлекаем номер — все последовательности цифр из строки
    import re
    digits = ''.join(re.findall(r'\d', input_string))

    # Определяем тип по ключевым словам в строке (без учёта регистра)
    input_lower = input_string.lower()

    is_card = any(
        keyword in input_lower
        for keyword in ['visa', 'mastercard', 'maestro', 'mir', 'amex']
    )
    is_account = 'счёт' in input_lower or 'account' in input_lower

    # Проверяем, что распознан ровно один тип
    if not (is_card or is_account):
        raise ValueError("Не удалось определить тип: карта или счёт")
    if is_card and is_account:
        raise ValueError("Строка содержит признаки и карты, и счёта — повторите ввод")

    # Выделяем часть строки до номера (тип продукта)
    # Ищем начало последовательности цифр
    number_start = re.search(r'\d', input_string)
    if number_start is None:
        raise ValueError("В строке не найден номер (цифры)")

    product_type = input_string[:number_start.start()].rstrip()

    # Применяем соответствующую функцию маскировки
    if is_card:
        # Для карт ожидаем 16 цифр
        if len(digits) != 16:
            raise ValueError("Номер карты должен содержать 16 цифр")
        masked_number = get_mask_card_number(digits)
    else:  # is_account
        # Для счетов ожидаем 20 цифр
        if len(digits) != 20:
            raise ValueError("Номер счёта должен содержать 20 цифр")
        masked_number = get_mask_account(digits)

    # Возвращаем строку с типом и замаскированным номером
    return f"{product_type} {masked_number}"