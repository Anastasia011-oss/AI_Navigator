locations = {
    "A": "Центр",
    "B": "Университет",
    "C": "Лікарня",
    "D": "Парк",
    "E": "Вокзал",
    "F": "Торговий центр",
    "G": "Аеропорт"
}


graph = {
    "A": {
        "B": {
            "distance": 5,
            "time": 8,
            "traffic": 2,
            "difficulty": 1
        },
        "D": {
            "distance": 7,
            "time": 10,
            "traffic": 1,
            "difficulty": 1
        }
    },

    "B": {
        "A": {
            "distance": 5,
            "time": 8,
            "traffic": 2,
            "difficulty": 1
        },
        "C": {
            "distance": 4,
            "time": 7,
            "traffic": 3,
            "difficulty": 2
        },
        "E": {
            "distance": 6,
            "time": 9,
            "traffic": 2,
            "difficulty": 1
        }
    },

    "C": {
        "B": {
            "distance": 4,
            "time": 7,
            "traffic": 3,
            "difficulty": 2
        },
        "G": {
            "distance": 8,
            "time": 15,
            "traffic": 2,
            "difficulty": 1
        }
    },

    "D": {
        "A": {
            "distance": 7,
            "time": 10,
            "traffic": 1,
            "difficulty": 1
        },
        "F": {
            "distance": 6,
            "time": 9,
            "traffic": 1,
            "difficulty": 1
        }
    },

    "E": {
        "B": {
            "distance": 6,
            "time": 9,
            "traffic": 2,
            "difficulty": 1
        },
        "G": {
            "distance": 7,
            "time": 10,
            "traffic": 2,
            "difficulty": 1
        }
    },

    "F": {
        "D": {
            "distance": 6,
            "time": 9,
            "traffic": 1,
            "difficulty": 1
        },
        "G": {
            "distance": 7,
            "time": 11,
            "traffic": 1,
            "difficulty": 1
        }
    },

    "G": {
        "C": {
            "distance": 8,
            "time": 15,
            "traffic": 2,
            "difficulty": 1
        },
        "E": {
            "distance": 7,
            "time": 10,
            "traffic": 2,
            "difficulty": 1
        },
        "F": {
            "distance": 7,
            "time": 11,
            "traffic": 1,
            "difficulty": 1
        }
    }
}


def dijkstra(start, finish):
    distances = {}

    for point in graph:
        distances[point] = float("inf")

    distances[start] = 0

    previous = {}
    visited = set()

    while len(visited) < len(graph):

        current = None
        current_distance = float("inf")

        for point in graph:
            if point not in visited:
                if distances[point] < current_distance:
                    current = point
                    current_distance = distances[point]

        if current is None:
            break

        visited.add(current)

        for neighbor in graph[current]:

            road = graph[current][neighbor]

            new_distance = (
                distances[current] +
                road["distance"]
            )

            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance
                previous[neighbor] = current

    if distances[finish] == float("inf"):
        return None

    route = []

    current = finish

    while current != start:

        route.append(current)

        current = previous[current]

    route.append(start)

    route.reverse()

    return route, distances[finish]


def get_route_information(route):
    total_time = 0
    total_traffic = 0
    total_difficulty = 0

    for i in range(len(route) - 1):

        current = route[i]
        next_point = route[i + 1]

        road = graph[current][next_point]

        total_time += road["time"]
        total_traffic += road["traffic"]
        total_difficulty += road["difficulty"]

    return total_time, total_traffic, total_difficulty