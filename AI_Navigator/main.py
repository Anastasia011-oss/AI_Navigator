from graph import (
    locations,
    dijkstra,
    get_route_information
)

from database import (
    create_database,
    save_route,
    get_history,
    update_actual_result
)

from statistics import show_statistics

from ai_analyzer import analyze_route


def show_locations():

    print("\n===== ЛОКАЦИИ =====")

    for code, name in locations.items():

        print(
            code,
            "-",
            name
        )


def find_route():

    show_locations()

    start = input(
        "\nНачальная точка: "
    ).upper()

    finish = input(
        "Конечная точка: "
    ).upper()

    if start not in locations:

        print(
            "Ошибка: такой начальной точки нет."
        )

        return

    if finish not in locations:

        print(
            "Ошибка: такой конечной точки нет."
        )

        return

    if start == finish:

        print(
            "Начальная и конечная точки "
            "совпадают."
        )

        return

    result = dijkstra(
        start,
        finish
    )

    if result is None:

        print(
            "Маршрут не найден."
        )

        return

    route, distance = result

    time, traffic, difficulty = (
        get_route_information(route)
    )

    print("\n===== РЕЗУЛЬТАТ =====")

    print(
        "Маршрут:",
        " → ".join(route)
    )

    print(
        "Расстояние:",
        distance,
        "км"
    )

    print(
        "Время:",
        time,
        "мин."
    )

    print(
        "Уровень заторов:",
        traffic
    )

    print(
        "Сложность дороги:",
        difficulty
    )

    print("\n===== СОХРАНЕНИЕ =====")

    user_name = input(
        "Имя пользователя: "
    )

    user_type = input(
        "Тип пользователя "
        "(student/worker/driver): "
    )

    save_route(
        user_name,
        user_type,
        start,
        finish,
        route,
        distance,
        time,
        traffic
    )

    print(
        "\nМаршрут сохранён в базу данных."
    )


def add_actual_result():

    history = get_history()

    if not history:

        print(
            "\nИстория маршрутов пустая."
        )

        return

    print("\n===== ИСТОРИЯ =====")

    for row in history:

        actual_time = row[9]

        if actual_time is None:
            actual_time_text = "нет"
        else:
            actual_time_text = str(actual_time)

        print(
            f"ID: {row[0]} | "
            f"Пользователь: {row[1]} | "
            f"Маршрут: "
            f"{row[5].replace(',', ' → ')} | "
            f"Прогноз: {row[7]} мин. | "
            f"Факт: {actual_time_text}"
        )

    try:

        route_id = int(
            input(
                "\nВведите ID поездки: "
            )
        )

        actual_time = float(
            input(
                "Фактическое время (мин.): "
            )
        )

        actual_distance = float(
            input(
                "Фактическое расстояние (км): "
            )
        )

    except ValueError:

        print(
            "Ошибка: необходимо вводить числа."
        )

        return

    update_actual_result(
        route_id,
        actual_time,
        actual_distance
    )

    print(
        "\nФактический результат сохранён."
    )


def show_history():

    history = get_history()

    print("\n===== ИСТОРИЯ МАРШРУТОВ =====")

    if not history:

        print(
            "История пока пустая."
        )

        return

    for row in history:

        actual_time = row[9]
        actual_distance = row[10]

        if actual_time is None:
            actual_time_text = "нет данных"
        else:
            actual_time_text = (
                str(actual_time) + " мин."
            )

        if actual_distance is None:
            actual_distance_text = "нет данных"
        else:
            actual_distance_text = (
                str(actual_distance) + " км"
            )

        print("\n----------------------------")

        print(
            "ID:",
            row[0]
        )

        print(
            "Пользователь:",
            row[1]
        )

        print(
            "Тип:",
            row[2]
        )

        print(
            "Маршрут:",
            row[5].replace(",", " → ")
        )

        print(
            "Расстояние:",
            row[6],
            "км"
        )

        print(
            "Прогнозируемое время:",
            row[7],
            "мин."
        )

        print(
            "Фактическое время:",
            actual_time_text
        )

        print(
            "Фактическое расстояние:",
            actual_distance_text
        )

        print(
            "Дата:",
            row[11]
        )


def ai_recommendation():

    show_locations()

    start = input(
        "\nНачальная точка: "
    ).upper()

    finish = input(
        "Конечная точка: "
    ).upper()

    if start not in locations:

        print(
            "Ошибка: такой точки нет."
        )

        return

    if finish not in locations:

        print(
            "Ошибка: такой точки нет."
        )

        return

    user_name = input(
        "Имя пользователя: "
    )

    result = dijkstra(
        start,
        finish
    )

    if result is None:

        print(
            "Маршрут не найден."
        )

        return

    route, distance = result

    time, traffic, difficulty = (
        get_route_information(route)
    )

    print("\n===== DIJKSTRA =====")

    print(
        "Маршрут:",
        " → ".join(route)
    )

    print(
        "Расстояние:",
        distance,
        "км"
    )

    print(
        "Расчётное время:",
        time,
        "мин."
    )

    analyze_route(
        user_name,
        start,
        finish,
        route,
        time
    )


def main():

    create_database()

    while True:

        print("\n")
        print("================================")
        print("         AI NAVIGATOR")
        print("================================")

        print(
            "1. Найти маршрут"
        )

        print(
            "2. Добавить результат прохождения"
        )

        print(
            "3. История маршрутов"
        )

        print(
            "4. Статистика"
        )

        print(
            "5. AI-рекомендация"
        )

        print(
            "0. Выход"
        )

        choice = input(
            "\nВыберите действие: "
        )

        if choice == "1":

            find_route()

        elif choice == "2":

            add_actual_result()

        elif choice == "3":

            show_history()

        elif choice == "4":

            show_statistics()

        elif choice == "5":

            ai_recommendation()

        elif choice == "0":

            print(
                "\nПрограмма завершена."
            )

            break

        else:

            print(
                "\nНеверный пункт меню."
            )


if __name__ == "__main__":
    main()