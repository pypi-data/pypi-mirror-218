import json
import os
import sys

from .classes import CheckCoverage, CliOutputService, JsonCoverageService, SUCCESS_EXIT_CODE, FAILURE_EXIT_CODE

if __name__ == '__main__':
    is_enough, actual_coverage = CheckCoverage(
        expected_coverage=int(os.getenv('EXPECTED_COVERAGE')),
        coverage_service=JsonCoverageService(
            coverage_json=json.load(
                open(
                    os.getenv('COVERAGE_FILE', 'coverage.json'),
                    'r'
                )
            )
        )
    ).is_enough()

    output_service = CliOutputService()

    output_service.print(f"Actual coverage: {actual_coverage}")

    if is_enough:
        output_service.print("Oh yeah")
        sys.exit(SUCCESS_EXIT_CODE)

    output_service.print("Oh no")
    sys.exit(FAILURE_EXIT_CODE)


