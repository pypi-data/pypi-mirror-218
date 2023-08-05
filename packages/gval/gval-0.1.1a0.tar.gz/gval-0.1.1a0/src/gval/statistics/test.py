# Test.py

from gval.statistics.categorical_statistics import CategoricalStatistics as CatSt

# Import class and instantiate
cat_stats = CatSt()


@cat_stats.register_function(name="test")
def test(tp: float, fn: int) -> float:
    return tp + fn


@cat_stats.register_function_class(vectorize_func=True)
class Tester:
    @staticmethod
    def test5(tp: int, fn: int) -> float:
        return tp + fn

    @staticmethod
    def test6(tp: int, fn: int) -> float:
        return tp + fn


def register(stat_obj):
    @stat_obj.register_function(name="test")
    def test(tp: float, fn: int) -> float:
        return tp + fn

    @stat_obj.register_function_class(vectorize_func=True)
    class Tester:
        @staticmethod
        def test5(tp: int, fn: int) -> float:
            return tp + fn

        @staticmethod
        def test6(tp: int, fn: int) -> float:
            return tp + fn
