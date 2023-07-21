from Helpers.HttpClient import ResponseWrapper, requestWrapper
import unittest
from email.message import Message
from unittest.mock import patch, Mock
import json

class HttpClientTestCase(unittest.TestCase):

    @patch("Helpers.tests.testHttpClient.requestWrapper")
    def test_ResponseWrapperJsonOk(self, mock_requestWrapper: Mock):
        mock_requestWrapper.return_value = ResponseWrapper(
                headers=None,
                status=200,
                body='{"data":{"someAttr":"something"}}',
            )
        response = requestWrapper("https://dummyUrl")
        mock_requestWrapper.assert_called_once()
        self.assertIsInstance(response, ResponseWrapper)
        self.assertIsInstance(response.json(), dict)


    @patch("Helpers.tests.testHttpClient.requestWrapper")
    def test_ResponseWrapperTextOk(self, mock_requestWrapper: Mock):
        headersMock = Message()
        headersMock.add_header("Content-Type","text/html")
        mock_requestWrapper.return_value = ResponseWrapper(
                headers=headersMock,
                status=404,
                body=b'Not Found',
            )
        response = requestWrapper("https://dummyUrl")
        mock_requestWrapper.assert_called_once()
        self.assertIsInstance(response.text(),str)

    @patch("Helpers.tests.testHttpClient.requestWrapper")
    def test_ResponseWrapperJsonKO(self, mock_requestWrapper: Mock):
        headersMock = Message()
        headersMock.add_header("Content-Type","text/json")
        mock_requestWrapper.return_value = ResponseWrapper(
                headers=headersMock,
                status=200,
                body=b'qd"svf"dcc[d{svdwf{"{"}}]',
            )
        response = requestWrapper("https://dummyUrl")
        self.assertIsInstance(response, ResponseWrapper)
        with self.assertRaises(json.JSONDecodeError) as jsonError:
            response.json()

    @patch("Helpers.tests.testHttpClient.requestWrapper")
    def test_ResponseWrapperBinaryOk(self, mock_requestWrapper: Mock):
        mock_requestWrapper.return_value = ResponseWrapper(
                headers=None,
                status=200,
                body=b'qdsvfdcc[d{svdwf{{}}]',
            )
        response = requestWrapper("https://dummyUrl")
        self.assertIsInstance(response, ResponseWrapper)
        self.assertIsInstance(response.raw(),bytes)
        