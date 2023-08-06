from huhk.testcase.apache.data import *
from huhk.unit_apache_beam import ApacheFun


class TestTimes:
    # 按事件时间标记时间戳
    def test_times_001(self):
        ApacheFun(data_list_dict3, data_type=data_type).timestamped_value("season").print()

    def test_times_002(self):
        ApacheFun(data_list_dict3, data_type=data_type).timestamped_value("season2").print()

    def test_times_003(self):
        ApacheFun(data_list_dict3, data_type=data_type).timestamped_value().print()
