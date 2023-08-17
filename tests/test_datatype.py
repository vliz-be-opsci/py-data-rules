from unittest import TestCase

from py_data_rules.data_type import (
    XSDAnyURI,
    XSDBoolean,
    XSDDate,
    XSDDateTime,
    XSDFloat,
    XSDInteger,
    XSDString,
)


class TestDataType(TestCase):
    def test_xsdstring(self):
        self.assertEqual(XSDString().match("ATextField"), True)
        self.assertEqual(XSDString(r"\d{2}.+").match("ATextField"), False)
        self.assertEqual(XSDString(r"\d{2}.+").match("01ATextField"), True)

    def test_xsdinteger(self):
        self.assertEqual(XSDInteger.match("1"), True)
        self.assertEqual(XSDInteger.match("1.1"), False)
        self.assertEqual(XSDInteger.repair("1.1"), "1")
        self.assertEqual(XSDInteger.repair("ATextField"), None)

    def test_xsdfloat(self):
        self.assertEqual(XSDFloat.repair("ATextField"), None)
        self.assertEqual(XSDFloat.repair("8603700"), "8603700")
        self.assertEqual(XSDFloat.repair("8,603,700"), "8603700")
        self.assertEqual(XSDFloat.repair("8.603.700"), "8603700")
        self.assertEqual(XSDFloat.repair("8603700.80"), "8603700.80")
        self.assertEqual(XSDFloat.repair("8603700,80"), "8603700.80")
        self.assertEqual(XSDFloat.repair("8 603 700.80"), "8603700.80")
        self.assertEqual(XSDFloat.repair("8 603 700,80"), "8603700.80")
        self.assertEqual(XSDFloat.repair("8'603'700.80"), "8603700.80")
        self.assertEqual(XSDFloat.repair("8'603'700,80"), "8603700.80")
        self.assertEqual(XSDFloat.repair("8_603_700.80"), "8603700.80")
        self.assertEqual(XSDFloat.repair("8_603_700,80"), "8603700.80")
        self.assertEqual(XSDFloat.repair("8,603,700.80"), "8603700.80")
        self.assertEqual(XSDFloat.repair("8.603.700,80"), "8603700.80")

    def test_xsddate(self):
        self.assertEqual(XSDDate().match("ATextField"), False)
        self.assertEqual(XSDDate().match("2023-13-01"), False)
        self.assertEqual(XSDDate().match("20230113"), False)
        self.assertEqual(XSDDate().match("2023-01-13"), True)
        self.assertEqual(XSDDate("%Y%m%d").match("20230113"), True)
        self.assertEqual(XSDDate(["%Y%m%d"]).match("20230113"), True)

    def test_xsddatetime(self):
        self.assertEqual(XSDDateTime().match("ATextField"), False)
        self.assertEqual(XSDDateTime().match("2023-01-13T09:10:11Z"), True)

    def text_xsdboolean(self):
        self.assertEqual(XSDBoolean.match("ATextField"), False)
        self.assertEqual(XSDBoolean.match("true"), True)
        self.assertEqual(XSDBoolean.repair("Y"), "true")
        self.assertEqual(XSDBoolean.repair("N"), "false")
        self.assertEqual(XSDBoolean.repair("ATextField"), None)

    def test_xsdanyuri(self):
        self.assertEqual(XSDAnyURI.match("0000-0002-5934-8998"), False)
        self.assertEqual(
            XSDAnyURI.match("https://orcid.org/0000-0002-5934-8998"), True
        )
        self.assertEqual(
            XSDAnyURI("https://orcid.org/").repair("0000-0002-5934-8998"),
            "https://orcid.org/0000-0002-5934-8998",
        )
        self.assertEqual(
            XSDAnyURI("orcid.org/").repair("0000-0002-5934-8998"), None
        )
