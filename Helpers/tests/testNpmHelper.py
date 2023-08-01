from Helpers.NpmHelper import NpmHelper
from Helpers.HttpClient import ResponseWrapper
import unittest
from datetime import datetime
from unittest.mock import patch, Mock

class NpmHelperTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.myNpmWrapper = NpmHelper()

    def test_getListIntervalOneYearNpm_Ok(self):
        startDate = datetime.strptime("01/01/1995", "%d/%m/%Y")
        endDate = datetime.strptime("01/01/1996", "%d/%m/%Y")
        nbYear = NpmHelper.getListIntervalOneYearNpm(startDate,endDate)
        self.assertEqual(len(nbYear),2)

    @patch("Helpers.NpmHelper.requestWrapper")
    def test_checkIntegrity(self, requestMock:Mock):
        fakeNpmData = {
            "dist-tags": {
                 "latest":"1.4.3"
            },
            "versions": {
                 "1.4.3": {
                      "dist":{
                           "tarball":"someUrl",
                           "integrity":"sha512-sFcuivsDZ99fY0TbvuRC6CDXB8r/ylafjJAMnbSF0y4EMM1/1DtQo40G2WKz1rBbyiz4SLAc3Wa6yZyC4XSGOQ=="
                      }
                 }
            }
        }

        with open("Helpers/tests/assets/light-cycle-1.4.3.tgz","rb") as checkFile:
            refData = checkFile.read()
        requestMock.return_value = ResponseWrapper(
                headers=None,
                status=200,
                body=refData,
            )
        integrityOk = self.myNpmWrapper.checkPackageIntegrity(fakeNpmData)
        self.assertEqual(integrityOk,True,"Invalid integrity check")

    