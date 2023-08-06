import os
import unittest
from unittest.mock import MagicMock

import mock
import pytest
from azureml.featurestore import FeatureSetSpec
from azureml.featurestore._utils.error_constants import EMPTY_FEATURE_MESSAGE
from azureml.featurestore.contracts import Column, ColumnType, DateTimeOffset, SourceType

from azure.ai.ml.exceptions import ValidationException

spec_path = os.path.join(os.path.dirname(__file__), "data", "feature_set_spec")
spec_path_local_source = os.path.join(os.path.dirname(__file__), "data", "feature_set_spec_local_source")


@pytest.mark.unittest
class FeatureSetSpecTest(unittest.TestCase):
    @mock.patch("azureml.featurestore._utils.utils._download_file")
    @mock.patch("azureml.featurestore.contracts.transformation_code.copy_rename_and_zip")
    def test_load_feature_set_spec(self, mock_copy_rename_and_zip, mock_download_file):
        mock_copy_rename_and_zip.return_value = "./code/test.zip"
        fset_spec = FeatureSetSpec.from_config(spec_path=spec_path)

        assert fset_spec.source.type == SourceType.MLTABLE
        assert "data_sources/customer_transactions/mltable" in fset_spec.source.path
        assert fset_spec.source.timestamp_column.name == "timestamp"
        assert fset_spec.source.timestamp_column.format == "%Y-%m-%d %H:%M:%S"
        assert fset_spec.source.source_delay == DateTimeOffset(days=1, hours=0, minutes=0)
        assert len(fset_spec.index_columns) == 1
        assert fset_spec.index_columns[0].name == "customer_id"
        assert fset_spec.index_columns[0].type == ColumnType.STRING
        assert fset_spec.feature_transformation_code.path == "./code"
        assert fset_spec.feature_transformation_code.transformer_class == "foo.CustomerTransactionsTransformer"
        assert fset_spec.source_lookback == DateTimeOffset(days=30, hours=0, minutes=0)
        assert fset_spec.temporal_join_lookback == DateTimeOffset(days=2, hours=0, minutes=0)
        assert fset_spec._feature_transformation_code_local_path == "./code/test.zip"

        # local feature source
        with self.assertRaises(Exception) as ex:
            FeatureSetSpec.from_config(spec_path=spec_path_local_source)
        assert "must be cloud path" in str(ex.exception)

        # copy and rename fail
        mock_copy_rename_and_zip.side_effect = Exception("Fail to copy and rename file")
        with self.assertRaises(Exception) as ex:
            FeatureSetSpec.from_config(spec_path=spec_path)
        assert "Fail to copy and rename file" in str(ex.exception)

        # download fail
        cloud_yaml_path = "wasbs://test@storage.blob.core.windows.net/spec_path"
        mock_download_file.side_effect = Exception("Fail to download file")
        with self.assertRaises(Exception) as ex:
            FeatureSetSpec.from_config(spec_path=cloud_yaml_path)
        assert "Fail to download file" in str(ex.exception)

    @mock.patch("azureml.featurestore.contracts.transformation_code.copy_rename_and_zip")
    def test_feature_set_spec_repr(self, mock_copy_rename_and_zip):
        mock_copy_rename_and_zip.return_value = "./code/test.zip"
        fset_spec = FeatureSetSpec.from_config(spec_path=spec_path)

        expected = """FeatureSetSpec
{
  "source": "FeatureSource(type: mltable, path: abfss://container@storage.dfs.core.windows.net/data_sources/customer_transactions/mltable, timestamp_column: TimestampColumn(Name=timestamp,Format=%Y-%m-%d %H:%M:%S), source_delay: DateTimeOffset(Days=1,Hours=0,Minutes=0))",
  "features": [
    "Feature(Name=transactions_6hr_sum,Type=integer)",
    "Feature(Name=transactions_1day_sum,Type=integer)",
    "Feature(Name=spend_6hr_sum,Type=float)",
    "Feature(Name=spend_1day_sum,Type=float)",
    "Feature(Name=is_sunny,Type=boolean)"
  ],
  "index_columns": [
    "Column(Name=customer_id,Type=string)"
  ],
  "feature_transformation_code": "TransformationCode(Path=./code,TransformerClass=foo.CustomerTransactionsTransformer)",
  "source_lookback": "DateTimeOffset(Days=30,Hours=0,Minutes=0)",
  "temporal_join_lookback": "DateTimeOffset(Days=2,Hours=0,Minutes=0)"
}"""
        assert fset_spec.__repr__() == expected
        assert fset_spec.__str__() == expected

    @mock.patch("azureml.featurestore.contracts.transformation_code.copy_rename_and_zip")
    def test_feature_set_spec(self, mock_copy_rename_and_zip):
        mock_copy_rename_and_zip.return_value = "./code/test.zip"
        fset_spec = FeatureSetSpec.from_config(spec_path=spec_path)

        timestamp_column, timestamp_column_format = fset_spec.get_timestamp_column()

        assert timestamp_column == "timestamp"
        assert timestamp_column_format == "%Y-%m-%d %H:%M:%S"

        index_columns = fset_spec.get_index_columns()

        assert len(index_columns) == 1
        assert index_columns[0].name == "customer_id"
        assert index_columns[0].type == ColumnType.STRING

        assert fset_spec.get_feature(name="transactions_6hr_sum").type == ColumnType.INTEGER
        assert fset_spec.get_feature(name="transactions_1day_sum").type == ColumnType.INTEGER
        assert fset_spec.get_feature(name="spend_6hr_sum").type == ColumnType.FLOAT
        assert fset_spec.get_feature(name="spend_1day_sum").type == ColumnType.FLOAT

        # no features
        with self.assertRaises(ValidationException) as ve:
            fset_spec.get_feature(name="dummy_feature")
        assert "Feature 'dummy_feature' not found in this feature set spec." in ve.exception.message

        # only str feature name
        with self.assertRaises(ValidationException) as ve:
            fset_spec.get_feature(name=1)
        assert "Name must be the string name of a feature in this feature set spec." in ve.exception.message

        # init failure
        with self.assertRaises(ValidationException) as ve:
            fset_spec = FeatureSetSpec(source=None, index_columns=[Column("id", ColumnType.INTEGER)])
        assert "Feature source is required for a feature set, please provide a feature source" in ve.exception.message

        with self.assertRaises(ValidationException) as ve:
            from azureml.featurestore.contracts.feature_source import FeatureSource
            from azureml.featurestore.contracts.timestamp_column import TimestampColumn

            fset_spec = FeatureSetSpec(
                source=FeatureSource(type=SourceType.CSV, path="test", timestamp_column=TimestampColumn("timestamp")),
                index_columns=None,
            )
        assert (
            "Index columns is required for a feature set, please provide non empty index columns"
            in ve.exception.message
        )

    @mock.patch("azureml.featurestore.contracts.transformation_code.copy_rename_and_zip")
    @mock.patch("azureml.featurestore.feature_set_spec.FeatureSetSpec.to_spark_dataframe")
    def test_create_feature_set_spec(self, mock_to_spark_dataframe, mock_copy_rename_and_zip):
        from azureml.featurestore import create_feature_set_spec
        from pyspark.sql import DataFrame
        from pyspark.sql.types import FloatType, IntegerType, StringType, StructField, StructType

        spec_path = os.path.join(os.path.dirname(__file__), "data", "feature_set_spec_no_features")
        mock_copy_rename_and_zip.return_value = "./code/test.zip"

        # not infer
        with self.assertRaises(Exception) as e:
            fset_spec = create_feature_set_spec(infer_schema=False, spec_path=spec_path)
        self.assertIn(EMPTY_FEATURE_MESSAGE, str(e.exception))

        # infer
        mock_df = MagicMock(DataFrame)
        mock_to_spark_dataframe.return_value = mock_df
        mock_df.columns = [
            "transactions_6hr_sum",
            "transactions_1day_sum",
            "spend_6hr_sum",
            "spend_1day_sum",
            "customer_id",
            "driver_id",
            "timestamp",
        ]
        mock_df.schema = StructType(
            [
                StructField(name="transactions_6hr_sum", dataType=IntegerType()),
                StructField(name="transactions_1day_sum", dataType=IntegerType()),
                StructField(name="spend_6hr_sum", dataType=FloatType()),
                StructField(name="spend_1day_sum", dataType=FloatType()),
                StructField(name="customer_id", dataType=IntegerType()),
                StructField(name="driver_id", dataType=IntegerType()),
                StructField(name="timestamp", dataType=StringType()),
            ]
        )
        fset_spec = create_feature_set_spec(infer_schema=True, spec_path=spec_path)

        assert fset_spec.source.type == SourceType.MLTABLE
        assert "data_sources/customer_transactions/mltable" in fset_spec.source.path
        assert fset_spec.source.timestamp_column.name == "timestamp"
        assert fset_spec.source.timestamp_column.format == "%Y-%m-%d %H:%M:%S"
        assert fset_spec.source.source_delay == DateTimeOffset(days=1, hours=0, minutes=0)

        assert len(fset_spec.index_columns) == 2
        assert len(fset_spec.features) == 4
        assert fset_spec.get_feature(name="transactions_6hr_sum").type == ColumnType.INTEGER
        assert fset_spec.get_feature(name="transactions_1day_sum").type == ColumnType.INTEGER
        assert fset_spec.get_feature(name="spend_6hr_sum").type == ColumnType.FLOAT
        assert fset_spec.get_feature(name="spend_1day_sum").type == ColumnType.FLOAT

        assert fset_spec.feature_transformation_code.path == "./code"
        assert fset_spec.feature_transformation_code.transformer_class == "foo.CustomerTransactionsTransformer"
        assert fset_spec.source_lookback == DateTimeOffset(days=30, hours=0, minutes=0)
        assert fset_spec.temporal_join_lookback == DateTimeOffset(days=2, hours=0, minutes=0)
        assert fset_spec._feature_transformation_code_local_path == "./code/test.zip"

        # infer empty
        mock_df.columns = [
            "customer_id",
            "driver_id",
            "timestamp",
        ]
        mock_df.schema = StructType(
            [
                StructField(name="customer_id", dataType=IntegerType()),
                StructField(name="driver_id", dataType=IntegerType()),
                StructField(name="timestamp", dataType=StringType()),
            ]
        )
        with self.assertRaises(Exception) as ve:
            fset_spec = create_feature_set_spec(infer_schema=True, spec_path=spec_path)
        self.assertIn(EMPTY_FEATURE_MESSAGE, str(ve.exception))
