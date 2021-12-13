import unittest
from src import app
from mockupdb import *
from src.mongo_utility import mongo_utility
from src.getAbnormalContact import calculate_abnoramlacy
from src.getMatchContactInvoice import check_confidence_contact


class InvoiceTestCases(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.server = MockupDB(auto_ismaster=True)
        self.server.run()
        app.testing = True
        app.config['MONGO_URI'] = self.server.uri
        self.app = app

    @classmethod
    def tearDown(self):
        self.server.stop()

    def test_add_new_invoice(self):
        """Testing for insert the data in mongo"""
        insert_data = {
            "_id": "unique-invoice-id-6",
            "organization": "organization-id",
            "createdAt": "2021-10-11T09:53:31.339Z",
            "updatedAt": "2021-11-29T13:15:19.500Z",
            "amount": {
                "currencyCode": "EUR",
                "value": 26.3
            },
            "contact": {
                "_id": "unique-contact-id",
                "iban": "DE88100500001310032358",
                "name": "Anirudh Sharma",
                "organization": "organization-id"
            },
            "invoiceDate": "2021-10-11T00:00:00.000Z",
            "invoiceId": "VR210230898"
        }
        mongo = mongo_utility(self.app)
        future = go(mongo.insert_document, insert_data)

        request = self.server.receives(
            OpMsg({"insert": "invoice", "ordered": True, "$db": "invoiceDB", "$readPreference": {"mode": "primary"},
                   "documents": [{"_id": "unique-invoice-id-6", "organization": "organization-id",
                                  "createdAt": "2021-10-11T09:53:31.339Z", "updatedAt": "2021-11-29T13:15:19.500Z",
                                  "amount": {"currencyCode": "EUR", "value": 26.3},
                                  "contact": {"_id": "unique-contact-id", "iban": "DE88100500001310032358",
                                              "name": "Anirudh Sharma", "organization": "organization-id"},
                                  "invoiceDate": "2021-10-11T00:00:00.000Z", "invoiceId": "VR210230898"}]}))
        request.ok(cursor={'inserted_id': "unique-invoice-id-6"})

        # act
        http_response = future()

        # assert
        data = http_response
        self.assertIn("unique-invoice-id-6", data.inserted_id)

    def test_get_abnormal(self):
        """Testing the business logic to see if abnormal amount is there"""
        message = calculate_abnoramlacy(23, list([{'amount': {'value': 23}}, {'amount': {'value': 23}}]))
        self.assertEqual(False, message[0]["abnormal"])

    def test_get_suggest_invoice(self):
        """Testing the business logic for finding the confidence"""
        message = check_confidence_contact(list([{'contact': {'name': 'Anirudh Sharma'}}, {'contact': {'name': 'Anir'}},
                                                 {'contact': {'name': 'Anirudh Sharma'}}]), 3)

        self.assertEqual(0.67, message[0]["confidence"])
