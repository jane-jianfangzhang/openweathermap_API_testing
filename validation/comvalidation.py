
def common_validation(response, expectedstatuscd):

    if response != expectedstatuscd:
        raise AssertionError("Common validation is fail! The expected response code is %s, but the actual "
                             "response status code result is %s"
                             % (expectedstatuscd, response))
    else:
        print("Common validation of status code is PASS!")

