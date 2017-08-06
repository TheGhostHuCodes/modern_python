from collections import defaultdict
from functools import partial
from math import fsum, sqrt
from pprint import pprint
from random import sample
from typing import DefaultDict, Dict, Iterable, List, Tuple, Sequence  # NOQA

Point = Tuple[int, ...]
Centroid = Point


def transpose(data):
    """Swap the rows and columns in a 2D array of data"""
    return list(zip(*data))


def mean(data: Iterable[float]) -> float:
    """Accurate arithmetic mean"""
    data = list(data)
    return fsum(data) / len(data)


def dist(p: Point, q: Point, fsum=fsum, sqrt=sqrt, zip=zip) -> float:
    """Euclidean distance function for multi-dimensional data"""
    return sqrt(fsum([(x - y)**2 for x, y in zip(p, q)]))


def assign_data(centroids: Sequence[Centroid],
                data: Iterable[Point]) -> Dict[Centroid, List[Point]]:
    """Group data points to the closest centroid"""
    d: DefaultDict[Centroid, List[Point]] = defaultdict(list)
    for point in data:
        closest_centroid = min(  # type: ignore
            centroids, key=partial(dist, point))
        d[closest_centroid].append(point)
    return dict(d)


def compute_centroids(groups: Iterable[Sequence[Point]]) -> List[Centroid]:
    """Compute the centroid of each group"""
    return [
        tuple(map(mean, transpose(group)))  #type: ignore
        for group in groups
    ]


def k_means(data: Iterable[Point], k: int=2,
            iterations: int=50) -> List[Centroid]:
    data = list(data)
    centroids = sample(data, k)
    for i in range(iterations):
        labeled = assign_data(centroids, data)
        centroids = compute_centroids(labeled.values())
    return centroids


if __name__ == '__main__':

    points = [
        (10, 41, 23),
        (22, 30, 29),
        (11, 42, 5),
        (20, 32, 4),
        (12, 40, 12),
        (21, 36, 23),
    ]

    centroids = k_means(points, k=3)
    d = assign_data(centroids, points)
    pprint(d)
