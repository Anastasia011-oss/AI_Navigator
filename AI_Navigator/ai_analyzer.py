from database import (
    get_route_statistics,
    get_user_statistics
)

def analyze_route(
        user_name,
        start_point,
        finish_point,
        dijkstra_route,
        dijkstra_time
):

    statistics = get_route_statistics(
        start_point,
        finish_point
    )

    user_statistics = get_user_statistics(
        user_name,
        start_point,
        finish_point
    )

    print("\n")
    print("===== AI-АНАЛИЗ =====")

    print(
        "Пользователь:",
        user_name
    )

    if statistics:

        print("\n===== ОБЩАЯ СТАТИСТИКА =====")

        best_route = None
        best_actual_time = None

        for row in statistics:

            route = row[0]
            count = row[1]
            expected_time = row[2]
            actual_time = row[3]

            print(
                "\nМаршрут:",
                route.replace(",", " → ")
            )

            print(
                "Количество поездок:",
                count
            )

            if expected_time is not None:

                print(
                    "Среднее прогнозируемое время:",
                    round(expected_time, 2),
                    "мин."
                )

            if actual_time is not None:

                print(
                    "Среднее фактическое время:",
                    round(actual_time, 2),
                    "мин."
                )

                if (
                    best_actual_time is None
                    or actual_time < best_actual_time
                ):

                    best_actual_time = actual_time
                    best_route = route

    else:

        print(
            "\nВ базе пока нет общей истории "
            "для этого маршрута."
        )

        best_route = None

    print("\n===== ЛИЧНАЯ СТАТИСТИКА =====")

    if user_statistics:

        user_best_route = None
        user_best_time = None

        for row in user_statistics:

            route = row[0]
            count = row[1]
            expected_time = row[2]
            actual_time = row[3]

            print(
                "\nПользователь:",
                user_name
            )

            print(
                "Маршрут:",
                route.replace(",", " → ")
            )

            print(
                "Количество поездок:",
                count
            )

            if expected_time is not None:

                print(
                    "Среднее прогнозируемое время:",
                    round(expected_time, 2),
                    "мин."
                )

            if actual_time is not None:

                print(
                    "Среднее фактическое время:",
                    round(actual_time, 2),
                    "мин."
                )

                if (
                    user_best_time is None
                    or actual_time < user_best_time
                ):

                    user_best_time = actual_time
                    user_best_route = route

    else:

        print(
            "У пользователя пока нет "
            "истории этого маршрута."
        )

        user_best_route = None
        user_best_time = None

    print("\n===== AI-РЕКОМЕНДАЦИЯ =====")

    dijkstra_route_text = ",".join(
        dijkstra_route
    )

    print(
        "Маршрут Dijkstra:"
    )

    print(
        " → ".join(dijkstra_route)
    )

    print(
        "Расчётное время:",
        dijkstra_time,
        "мин."
    )

    if user_best_route is not None:

        print(
            "\nAI учитывает личную историю пользователя."
        )

        if user_best_route == dijkstra_route_text:

            print(
                "Ваш личный опыт подтверждает "
                "маршрут Dijkstra."
            )

            if user_best_time is not None:

                difference = (
                    user_best_time - dijkstra_time
                )

                print(
                    "Ваше среднее фактическое время:",
                    round(user_best_time, 2),
                    "мин."
                )

                if difference < 0:

                    print(
                        "Для вас этот маршрут обычно "
                        "быстрее расчётного времени на",
                        round(abs(difference), 2),
                        "мин."
                    )

                elif difference > 0:

                    print(
                        "Для вас этот маршрут обычно "
                        "дольше расчётного времени на",
                        round(difference, 2),
                        "мин."
                    )

                else:

                    print(
                        "Ваше фактическое время примерно "
                        "совпадает с расчётным."
                    )

        else:

            print(
                "AI рекомендует ваш наиболее "
                "быстрый исторический маршрут:"
            )

            print(
                user_best_route.replace(
                    ",",
                    " → "
                )
            )

            print(
                "Среднее фактическое время:",
                round(user_best_time, 2),
                "мин."
            )
    else:

        if best_route is not None:

            print(
                "Личной истории пока нет."
            )

            print(
                "AI использует общую статистику "
                "других пользователей."
            )

            print(
                "Наиболее быстрый исторический маршрут:"
            )

            print(
                best_route.replace(
                    ",",
                    " → "
                )
            )

            if best_actual_time is not None:

                print(
                    "Среднее фактическое время:",
                    round(best_actual_time, 2),
                    "мин."
                )

        else:

            print(
                "Недостаточно данных для AI-рекомендации."
            )

            print(
                "Рекомендуется использовать "
                "маршрут Dijkstra."
            )