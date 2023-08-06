from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import IO, Tuple

SUCCESS_EXIT_CODE = 0
FAILURE_EXIT_CODE = 255


class AbstractCoverageService(ABC):
    @abstractmethod
    def get_actual_coverage(self) -> int:
        pass


class AbstractOutputService(ABC):
    @abstractmethod
    def print(self, content: str):
        pass


class CliOutputService(AbstractOutputService):

    def print(self, content: str):
        print(str)


@dataclass
class CheckCoverage:
    expected_coverage: int
    coverage_service: AbstractCoverageService

    def is_enough(self) -> Tuple[bool, float]:
        actual_coverage = self.coverage_service.get_actual_coverage()

        return actual_coverage >= self.expected_coverage, actual_coverage


@dataclass
class JsonCoverageService(AbstractCoverageService):
    coverage_json: dict

    def get_actual_coverage(self) -> int:
        if 'totals' not in self.coverage_json:
            return 0

        if 'percent_covered' not in self.coverage_json['totals']:
            return 0

        if not isinstance(self.coverage_json['totals']['percent_covered'], int):
            return 0

        return self.coverage_json['totals']['percent_covered']
