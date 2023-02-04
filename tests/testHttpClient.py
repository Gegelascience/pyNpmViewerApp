from Helpers.HttpClient import ResponseWrapper, requestWrapper
import unittest


class HttpClientTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.urlJson = "https://registry.npmjs.org/ngx-view360"
        self.urlBinary = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/The_Earth_seen_from_Apollo_17.jpg/1024px-The_Earth_seen_from_Apollo_17.jpg"

    def test_ResponseWrapperJsonOk(self):
        response = requestWrapper(self.urlJson)
        self.assertIsInstance(response, ResponseWrapper)
        if response.status == 200:
            data = response.json()
            self.assertIsInstance(data, dict)

        else:
            self.assertIsInstance(response.text(),str)


    def test_ResponseWrapperJsonKO(self):
        response = requestWrapper(self.urlBinary)
        self.assertIsInstance(response, ResponseWrapper)
        if response.status == 200:
            with self.assertRaises(UnicodeDecodeError) as UnicodeErr:
                data = response.json()

        else:
            self.assertIsInstance(response.text(),str)


        