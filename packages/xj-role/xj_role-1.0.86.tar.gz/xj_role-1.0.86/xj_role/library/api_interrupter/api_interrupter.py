# encoding: utf-8
"""
@project: djangoModel->api_interrupter
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: API阻断器
@created_time: 2023/7/5 10:30
"""


class APIInterrupter():
    """API接口阻断器"""

    def _get_open_api(self):
        """
        获取开放API
        :return: data, err
        """
        pass

    def _get_system_api(self):
        """
        获取系统所有API
        :return: data, err
        """
        pass

    def api_switch(self, *args, user_id, api_route, **kwargs):
        """
        接口
        :param user_id:
        :param api_route:
        :return: data, err
        """
        pass

    def api_filter_value(self, *args, user_id, api_route, **kwargs):
        """
        接口值过滤
        :param user_id: 用户ID
        :param api_route: 接口路由
        :return: data, err
        """
        pass
