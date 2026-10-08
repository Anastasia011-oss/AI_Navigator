from database import get_history


def show_statistics():

    history = get_history()

    if not history:

        print("\nИстория маршрутов пока пустая.")

        return

    print("\n")
    print("===== СТАТИСТИКА =====")

    print(
        "Всего проходжень:",
        len(history)
    )

    total_distance = 0
    actual_times = []
    actual_distances = []

    route_counter = {}

    fastest_route = None
    slowest_route = None

    for row in history:

        route = row[5]
        distance = row[6]
        actual_time = row[9]
        actual_distance = row[10]

        total_distance += distance

        if actual_time is not None:

            actual_times.append(actual_time)

            if fastest_route is None:
                fastest_route = row

            elif actual_time < fastest_route[9]:
                fastest_route = row

            if slowest_route is None:
                slowest_route = row

            elif actual_time > slowest_route[9]:
                slowest_route = row

        if actual_distance is not None:
            actual_distances.append(actual_distance)

        if route not in route_counter:
            route_counter[route] = 0

        route_counter[route] += 1

    average_distance = (
        total_distance / len(history)
    )

    print(
        "Средняя расчётная дистанция:",
        round(average_distance, 2),
        "км"
    )

    if actual_times:

        average_actual_time = (
            sum(actual_times) /
            len(actual_times)
        )

        print(
            "Среднее фактическое время:",
            round(average_actual_time, 2),
            "мин."
        )

    else:

        print(
            "Среднее фактическое время: "
            "нет данных"
        )

    if actual_distances:

        average_actual_distance = (
            sum(actual_distances) /
            len(actual_distances)
        )

        print(
            "Средняя фактическая дистанция:",
            round(average_actual_distance, 2),
            "км"
        )

    else:

        print(
            "Средняя фактическая дистанция: "
            "нет данных"
        )

    print("\nСамые популярные маршруты:")

    sorted_routes = sorted(
        route_counter.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for route, count in sorted_routes:

        print(
            route.replace(",", " → "),
            "-",
            count,
            "раз"
        )

    if fastest_route:

        print("\nСамый быстрый маршрут:")

        print(
            fastest_route[5].replace(",", " → "),
            "-",
            fastest_route[9],
            "мин."
        )

    if slowest_route:

        print("\nСамый медленный маршрут:")

        print(
            slowest_route[5].replace(",", " → "),
            "-",
            slowest_route[9],
            "мин."
        )

    print("\nРазница между прогнозом и фактическим временем:")

    for row in history:

        if row[9] is not None:

            difference = row[9] - row[7]

            print(
                row[5].replace(",", " → "),
                ":",
                round(difference, 2),
                "мин."
            )