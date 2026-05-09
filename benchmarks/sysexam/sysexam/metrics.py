from inspect_ai.scorer import Metric, SampleScore, metric


@metric
def points_accuracy() -> Metric:
    def metric_fn(scores: list[SampleScore]) -> float:
        total_earned = 0.0
        total_possible = 0.0

        for sample_score in scores:
            metadata = sample_score.score.metadata or {}
            total_earned += metadata.get("points_earned", 0)
            total_possible += metadata.get("points_possible", 0)

        if total_possible == 0:
            return 0.0

        return total_earned / total_possible

    return metric_fn


@metric
def total_points_earned() -> Metric:
    def metric_fn(scores: list[SampleScore]) -> float:
        total = 0.0

        for sample_score in scores:
            metadata = sample_score.score.metadata or {}
            total += metadata.get("points_earned", 0)

        return total

    return metric_fn


@metric
def total_points_possible() -> Metric:
    def metric_fn(scores: list[SampleScore]) -> float:
        total = 0.0

        for sample_score in scores:
            metadata = sample_score.score.metadata or {}
            total += metadata.get("points_possible", 0)

        return total

    return metric_fn


@metric
def points_stderr() -> Metric:
    def metric_fn(scores: list[SampleScore]) -> float:
        ratios = []
        for sample_score in scores:
            metadata = sample_score.score.metadata or {}
            earned = metadata.get("points_earned", 0)
            possible = metadata.get("points_possible", 0)
            if possible > 0:
                ratios.append(earned / possible)

        n = len(ratios)
        if n < 2:
            return 0.0

        mean_r = sum(ratios) / n
        sample_var = sum((r - mean_r) ** 2 for r in ratios) / (n - 1)
        return (sample_var / n) ** 0.5

    return metric_fn
