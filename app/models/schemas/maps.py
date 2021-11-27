import math
from itertools import permutations
from typing import List, Union

from pydantic import BaseModel

from app.models.schemas.points import Point, PointInDB


class Map(BaseModel):
    points: List[Union[Point, PointInDB]]

    def get_routes_amount(self):
        return math.factorial(len(self.points) - 1)

    def __get_distanced_route(self, route) -> list:
        """
        Возвращает попарный список возможных маршрутов с расстояниями вида:
        [(p1, p2, dist), (p2, pn, dist), (pn, pn+1, dist), ...]
        """
        route_pairs = []

        for i in range(0, len(route) - 1):
            route_pairs.append(
                (
                    str(route[i]),
                    str(route[i + 1]),
                    route[i].get_distance_to_another_point(route[i + 1]),
                )
            )

        return route_pairs

    def __get_routes(self) -> list:
        """Возвращает список возможных маршрутов вида: [(p1, p2, p3, pn), (p*, ...), ...]"""

        routes = []
        distanced_routes = []  # Маршруты с дистанциями попарно от точки до точки

        for points_combo in permutations(self.points[1:], r=len(self.points[1:])):
            route = [
                self.points[0],
            ]  # Путь с первой точкой в виде начальной
            for point in points_combo:
                route.append(point)
            route.append(self.points[0])  # Добавление первой точки в виде финальной
            routes.append(tuple(route))

        for route in routes:
            distanced_routes.append(self.__get_distanced_route(route))

        return distanced_routes

    def get_total_route_distance(self, route: list) -> float:
        """Возвращает общий путь маршрута"""
        distance = 0

        for point in route:
            distance += point[2]  # point: (from, to, -> distance <-)

        return distance

    def get_best_route(self) -> list:
        """Возвращает самый оптимальный путь, который есть в self.routes"""

        best_route = self.routes[0]
        for route in self.routes:
            if self.get_total_route_distance(route) <= self.get_total_route_distance(
                best_route
            ):
                best_route = route

        return best_route

    @property
    def routes(self) -> list:
        """Возвращает список возможных маршрутов"""
        return self.__get_routes()


class Route(BaseModel):
    from_: Union[Point, PointInDB]
    to: Union[Point, PointInDB]
    distance: float
