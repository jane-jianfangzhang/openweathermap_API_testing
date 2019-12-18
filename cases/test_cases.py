import requests
from logger import log
from config import DataConstant as dc
from validation import comvalidation, specialvalidation
import pytest


class TestCases:
    logging = log()

    def test_weather(self):

        # Step1: Send request and get response
        try:
            self.logging.info("-----------Get weather and forecasts------------------")
            self.logging.info("test")
            response = requests.get(dc.base_url)
            # self.logging.debug("The response is %s" % (response.text))

            # Step2: Get response to do common validation

            comvalidation.common_validation(response.status_code, requests.codes.ok)

            # Step3: Special validation base on caseType

            specialvalidation.special_validation(response, self.logging)

            self.logging.info("Cases Pass !")

        except Exception as e:

            self.logging.info("Cases Fail failed,  some error hit in test scripts!" )

            self.logging.error(e, exc_info=True)

            pytest.fail()
