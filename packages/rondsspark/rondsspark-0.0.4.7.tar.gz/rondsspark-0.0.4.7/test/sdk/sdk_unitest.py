import unittest
from datetime import date, datetime
from typing import Callable

import pandas as pd
from pyspark.sql import SparkSession

import ronds_sdk.transforms.pandas.transforms as py_df
from ronds_sdk.options.pipeline_options import PipelineOptions, SparkRunnerOptions
from ronds_sdk.pipeline import Pipeline
from ronds_sdk.tools.utils import RuleParser
from ronds_sdk.transforms import ronds


def mock_data():
    return [(1, 1., 'string1', date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
            (2, 2., 'string2', date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
            (3, 3., 'string3', date(2000, 3, 1), datetime(2000, 1, 3, 12, 0))]


class SdkUnitTest(unittest.TestCase):

    def test_rules_load(self):
        rule_parser = RuleParser('./rule_config.json')
        rules = rule_parser.load()
        self.assertTrue(isinstance(rules, list))
        self.assertTrue(len(rules) > 0)

    def test_spark_json_load(self):
        spark = SparkSession.builder.getOrCreate()
        rules_parser = RuleParser("rule_config.json")
        df = spark.createDataFrame(rules_parser.load())
        print(df.schema)
        rules = df.collect()
        print(rules)
        self.assertTrue(len(rules) > 1)

    def test_spark_runner_options(self):
        options = PipelineOptions(
            spark_repartition_num=3
        )
        num = options.view_as(SparkRunnerOptions).spark_repartition_num
        print('num: %d' % num)
        self.assertTrue(num == 3)

    def test_rule_cassandra_scan_console(self):
        options = PipelineOptions(
            spark_transform_package='ronds_sdk.transforms.pandas_dataframe',
            spark_repartition_num=1
        )
        with Pipeline(options=options) as p:
            p | "Rule Cassandra Scan" >> ronds.RulesCassandraScan('rule_config.json') \
                | "Console" >> ronds.Console()
        self.assertTrue(True)

    def test_list_str(self):
        data = [
            {'a': 1, 'b': [[2, 3]], 'c': [{'d': 1}, 3]},
            {'a': 2, 'b': [[3]], 'c': [{'d': 1}, 3]},
            {'a': 3, 'b': [[4]], 'c': [{'d': 1}, 3]},
        ]
        dt = pd.DataFrame(data)
        self.assertTrue(dt['c'][0][0]['d'] == 1)
        dt_dict = dt.to_dict('records')
        self.assertTrue(id(dt['c'][0]) == id(dt_dict[0]['c']))
        print("records json: %s" % dt_dict)
        print("dict json: %s" % dt.to_dict())
        print("index json: %s" % dt.to_dict('index'))
        print("*" * 20)
        for i, row in dt.iterrows():
            print("%s: table json: %s" % (i, row.to_json(orient='table')))
            print("%s: records json: %s" % (i, row.to_json(orient='records')))
            print("%s: split json: %s" % (i, row.to_json(orient='split')))
            print("%s: index json: %s" % (i, row.to_json(orient='index')))

    def test_pd_dt(self):
        data = [RuleParser('test_data.json').load()]
        dt = pd.DataFrame(data)
        print(dt)
        assert isinstance(data[0], dict)
        nodes = data[0]['nodes']
        self.assertTrue(id(nodes) == id(dt['nodes'][0]))

    def test_list_tuple(self):
        rows = [('key1', 'v1'), ('key2', 'v2')]
        for key, value in rows:
            print(key, value)
        self.assertTrue(True)

    def test_algorithm(self):
        options = PipelineOptions(
            algorithm_path='AlgMock',
            algorithm_funcname='alg_mock.alg_mock'
        )
        alg = py_df.Algorithm(ronds.Algorithm(), options)
        func = alg.algorithm_func
        self.assertTrue(isinstance(func, Callable))
        result = func("test data")
        self.assertTrue('test data' == result)


if __name__ == '__main__':
    unittest.main()
