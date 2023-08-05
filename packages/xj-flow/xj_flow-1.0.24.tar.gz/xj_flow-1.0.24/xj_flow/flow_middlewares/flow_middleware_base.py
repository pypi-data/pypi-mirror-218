# encoding: utf-8
"""
@project: djangoModel->flow_middleware_base
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 流程中间件基类
@created_time: 2023/7/7 14:10
"""
from abc import ABC


class FlowMiddlewareBase(ABC):
    def process(self, *args, **kwargs):
        pass
