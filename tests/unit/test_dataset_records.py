from functools import partial
import json
from unittest import TestCase

from pandas import DataFrame
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


class TestDatasetRecords(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.tamr = Client(auth)

    @responses.activate
    def test_get(self):
        records_url = f"{self._dataset_url}/records"
        responses.add(responses.GET, self._dataset_url, json={})
        responses.add(
            responses.GET,
            records_url,
            body="\n".join([json.dumps(x) for x in self._records_json]),
        )

        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)
        records = list(dataset.records())
        self.assertListEqual(records, self._records_json)

    @responses.activate
    def test_update(self):
        def create_callback(request, snoop):
            snoop["payload"] = list(request.body)
            return 200, {}, json.dumps(self._response_json)

        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        records_url = f"{self._dataset_url}:updateRecords"
        updates = TestDatasetRecords.records_to_updates(self._records_json)
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, partial(create_callback, snoop=snoop)
        )

        response = dataset._update_records(updates)
        self.assertEqual(response, self._response_json)
        self.assertEqual(snoop["payload"], TestDatasetRecords.stringify(updates))

    @responses.activate
    def test_nan_update(self):
        def create_callback(request, snoop, status):
            snoop["payload"] = list(request.body)
            return status, {}, json.dumps(self._response_json)

        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        records_url = f"{self._dataset_url}:updateRecords"
        updates = TestDatasetRecords.records_to_updates(self._nan_records_json)

        snoop = {}
        responses.add_callback(
            responses.POST,
            records_url,
            partial(create_callback, snoop=snoop, status=200),
        )

        self.assertRaises(ValueError, lambda: dataset._update_records(updates))

    @responses.activate
    def test_upsert(self):
        def create_callback(request, snoop):
            snoop["payload"] = list(request.body)
            return 200, {}, json.dumps(self._response_json)

        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        records_url = f"{self._dataset_url}:updateRecords"
        updates = TestDatasetRecords.records_to_updates(self._records_json)
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, partial(create_callback, snoop=snoop)
        )

        response = dataset.upsert_records(self._records_json, "attribute1")
        self.assertEqual(response, self._response_json)
        self.assertEqual(snoop["payload"], TestDatasetRecords.stringify(updates))

    @responses.activate
    def test_upsert_from_dataframe(self):
        def create_callback(request, snoop):
            snoop["payload"] = list(request.body)
            return 200, {}, json.dumps(self._response_json)

        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        records_url = f"{self._dataset_url}:updateRecords"
        updates = TestDatasetRecords.records_to_updates(self._records_json)
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, partial(create_callback, snoop=snoop)
        )

        response = dataset.upsert_from_dataframe(
            self._dataframe, primary_key_name="attribute1"
        )
        self.assertEqual(response, self._response_json)
        self.assertEqual(snoop["payload"], TestDatasetRecords.stringify(updates))

    @responses.activate
    def test_upsert_from_dataframe_nan(self):
        def create_callback(request, snoop):
            snoop["payload"] = list(request.body)
            return 200, {}, json.dumps(self._response_json)

        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        records_url = f"{self._dataset_url}:updateRecords"
        updates = TestDatasetRecords.records_to_updates(self._null_records_json)
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, partial(create_callback, snoop=snoop)
        )

        response = dataset.upsert_from_dataframe(
            self._dataframe_nan, primary_key_name="pk"
        )
        self.assertEqual(response, self._response_json)
        self.assertEqual(snoop["payload"], TestDatasetRecords.stringify(updates))

    @responses.activate
    def test_delete(self):
        def create_callback(request, snoop):
            snoop["payload"] = list(request.body)
            return 200, {}, json.dumps(self._response_json)

        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        records_url = f"{self._dataset_url}:updateRecords"
        deletes = TestDatasetRecords.records_to_deletes(self._records_json)
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, partial(create_callback, snoop=snoop)
        )

        response = dataset.delete_records(self._records_json, "attribute1")
        self.assertEqual(response, self._response_json)
        self.assertEqual(snoop["payload"], TestDatasetRecords.stringify(deletes))

    @responses.activate
    def test_delete_ids(self):
        def create_callback(request, snoop):
            snoop["payload"] = list(request.body)
            return 200, {}, json.dumps(self._response_json)

        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        records_url = f"{self._dataset_url}:updateRecords"
        deletes = TestDatasetRecords.records_to_deletes(self._records_json)
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, partial(create_callback, snoop=snoop)
        )

        ids = [r["attribute1"] for r in self._records_json]
        response = dataset.delete_records_by_id(ids)
        self.assertEqual(response, self._response_json)
        self.assertEqual(snoop["payload"], TestDatasetRecords.stringify(deletes))

    @responses.activate
    def test_delete_all(self):
        responses.add(responses.GET, self._dataset_url, json={})
        dataset = self.tamr.datasets.by_resource_id(self._dataset_id)

        responses.add(responses.DELETE, self._dataset_url + "/records", status=204)
        response = dataset.delete_all_records()
        self.assertEqual(response.status_code, 204)

    @staticmethod
    def records_to_deletes(records):
        return [
            {"action": "DELETE", "recordId": i}
            for i, record in enumerate(records, start=1)
        ]

    @staticmethod
    def records_to_updates(records):
        return [
            {"action": "CREATE", "recordId": i, "record": record}
            for i, record in enumerate(records, start=1)
        ]

    @staticmethod
    def stringify(updates):
        return [json.dumps(u).encode("utf-8") for u in updates]

    _dataset_id = "1"
    _dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/{_dataset_id}"

    _records_json = [{"attribute1": 1}, {"attribute1": 2}]
    _dataframe = DataFrame(_records_json, columns=["attribute1"], dtype=object)
    _nan_records_json = [
        {"pk": 1, "attribute1": float("nan")},
        {"pk": 2, "attribute1": float("nan")},
    ]
    _dataframe_nan = DataFrame(
        _nan_records_json, columns=["pk", "attribute1"], dtype=object
    )
    _null_records_json = [{"pk": 1, "attribute1": None}, {"pk": 2, "attribute1": None}]
    _response_json = {
        "numCommandsProcessed": 2,
        "allCommandsSucceeded": True,
        "validationErrors": [],
    }
