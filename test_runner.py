import os
import subprocess

root_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))


def run(command):
    """
    To run all the test cases
    :return:
    """
    subprocess.run(command, shell=True)


if __name__ == "__main__":

    test_command = "python -m pytest -s " + os.path.join(root_path, "cases", "test_cases.py::TestCases::test_weather") + \
    " --html=" + os.path.join(root_path, "report_output", "open_weather_map_testing_report.html")

    run(test_command)