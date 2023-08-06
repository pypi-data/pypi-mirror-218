import unittest

import mock
import pytest
from azureml.featurestore._utils.utils import (
    _download_file,
    _ensure_azureml_full_path,
    _parse_path_format,
    _process_path,
    _resolve_hdfs_path_from_storage_info,
)


@pytest.mark.unittest
class UtilsTest(unittest.TestCase):
    def test_parse_path_format(self):
        from azureml.featurestore._utils.utils import PathType

        test_cases = [
            ("https://account.blob.core.windows.net/container/data.csv", PathType.cloud),
            ("adl://account.azuredatalakestore.net/data.csv", PathType.storage),
            ("abfs://container@account.dfs.core.windows.net/data.csv", PathType.storage),
            ("abfss://container@account.dfs.core.windows.net/data.csv", PathType.storage),
            ("wasbs://container@account.blob.core.windows.net", PathType.storage),
            ("wasb://container@account.blob.core.windows.net", PathType.storage),
            ("azureml://datastores/datastore/paths/data.parquet", PathType.azureml),
            (
                "azureml://subscriptions/sub_id/resourcegroups/rg/workspaces/ws/datastores/datastore/paths/data.parquet",
                PathType.azureml,
            ),
            ("./test/data.csv", PathType.local),
            ("/Users/test/data.csv", PathType.local),
        ]

        for test_case in test_cases:
            path_type, path = _parse_path_format(path=test_case[0])
            self.assertEqual(path_type, test_case[1])
            self.assertEqual(path, test_case[0])

    @mock.patch("azureml.featurestore._utils.utils._download_file")
    def test_process_path(self, mock_download_file):
        local_path = __file__

        path = _process_path(local_path)
        self.assertEqual(path, local_path)

        with self.assertRaises(ValueError) as ve:
            _process_path("../dummy/data.csv")
        self.assertTrue("does not exist." in str(ve.exception))

        mock_download_file.return_value = "./download/data.csv"
        path = _process_path("abfss://container@account.dfs.core.windows.net/data.csv")
        self.assertEqual(path, "./download/data.csv")

        # download failure
        mock_download_file.side_effect = Exception("Download failure")
        with self.assertRaises(Exception) as ex:
            _process_path("abfss://container@account.dfs.core.windows.net/data.csv")
        self.assertTrue("Download failure" in str(ex.exception))

    @mock.patch("azureml.featurestore._utils.utils.Copier")
    @mock.patch("azureml.featurestore._utils.utils.download_artifact_from_aml_uri")
    @mock.patch("azureml.featurestore._utils.utils.download_artifact_from_storage_url")
    def test_download_file(self, mock_download_from_storage_uri, mock_download_from_aml_uri, mock_copier):
        import os

        from azureml.featurestore._utils.utils import PathType

        from azure.ai.ml.operations import DatastoreOperations

        cur_path = os.getcwd()
        local_mock_spec_path = os.path.join(cur_path, "spec")
        local_path = _download_file(
            path="azureml://subscriptions/sub/resourcegroups/rg/workspaces/ws/datastores/st/paths/feature_retrieval_spec/",
            path_type=PathType.azureml,
            target_path=cur_path,
        )
        self.assertEqual(local_path, os.path.join(cur_path, "feature_retrieval_spec"))

        mock_download_from_storage_uri.return_value = local_mock_spec_path
        local_path = _download_file(
            path="cloud_path",
            path_type=PathType.cloud,
            target_path=cur_path,
            datastore_operations=mock.MagicMock(DatastoreOperations),
        )
        mock_download_from_storage_uri.assert_called_once()
        self.assertEqual(local_path, local_mock_spec_path)

        mock_download_from_aml_uri.return_value = local_mock_spec_path
        local_path = _download_file(
            path="aml_path",
            path_type=PathType.azureml,
            target_path="\\temp\\test",
            datastore_operations=mock.MagicMock(DatastoreOperations),
        )
        mock_download_from_aml_uri.assert_called_once()
        self.assertEqual(local_path, local_mock_spec_path)

        local_path = _download_file(
            path=local_mock_spec_path,
            path_type=PathType.local,
            target_path=os.path.join(cur_path, "local"),
            datastore_operations=mock.MagicMock(DatastoreOperations),
        )
        self.assertEqual(local_path, local_mock_spec_path)

        with self.assertRaises(Exception) as ex:
            local_path = _download_file(
                path="storage_path",
                path_type=PathType.storage,
                target_path=local_mock_spec_path,
                datastore_operations=mock.MagicMock(DatastoreOperations),
            )
        self.assertIn("Can't download from path: storage_path, path type: storage is not supported", str(ex.exception))

    def test_ensure_azureml_full_path(self):
        path = _ensure_azureml_full_path(
            path="azureml://datastores/datastore/paths/data.parquet",
            subscription_id="sub_id",
            resource_group="rg",
            workspace_name="ws",
        )
        self.assertEqual(
            path,
            "azureml://subscriptions/sub_id/resourcegroups/rg/workspaces/ws/datastores/datastore/paths/data.parquet",
        )

    def test_resolve_hdfs_path_from_storage_info(self):
        from azure.ai.ml.entities._assets._artifacts.artifact import ArtifactStorageInfo

        asset_artifact = ArtifactStorageInfo(
            name=None,
            version=None,
            datastore_arm_id="datastores/dummy_datastore",
            relative_path="data/path",
            storage_account_url="storage_account.dfs.core.windows.net",
            container_name="container",
        )

        path = _resolve_hdfs_path_from_storage_info(asset_artifact=asset_artifact)
        self.assertEqual(path, "abfss://container@storage_account.dfs.core.windows.net/data/path")

        asset_artifact.storage_account_url = "storage_account.blob.core.windows.net"
        path = _resolve_hdfs_path_from_storage_info(asset_artifact=asset_artifact)
        self.assertEqual(path, "wasbs://container@storage_account.blob.core.windows.net/data/path")

        from azure.ai.ml.exceptions import ValidationException

        asset_artifact.storage_account_url = "storage_account.datalake"
        with self.assertRaises(ValidationException) as ve:
            _resolve_hdfs_path_from_storage_info(asset_artifact=asset_artifact)
        self.assertTrue("Unsupported Storage account type. Storage url:" in str(ve.exception))
