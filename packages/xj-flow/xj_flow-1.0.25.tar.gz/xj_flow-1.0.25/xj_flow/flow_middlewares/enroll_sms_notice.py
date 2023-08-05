# encoding: utf-8
"""
@project: djangoModel->enroll_sms_notice
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2023/7/7 12:03
"""
from .flow_middleware_base import FlowMiddlewareBase
from ..utils.custom_tool import dynamic_load_class, write_to_log


class EnrollSMSNotice(FlowMiddlewareBase):
    def get_send_phones(self, flow_node_id, relate_data_value):
        """获取要发送的搜手机号"""
        try:
            if not flow_node_id or not relate_data_value:
                return [], None

            Enroll, import_err = dynamic_load_class(import_path="xj_enroll.models", class_name="Enroll")
            if import_err:
                return [], import_err
            EnrollRecord, import_err = dynamic_load_class(import_path="xj_enroll.models", class_name="EnrollRecord")
            if import_err:
                return [], import_err
            FlowNode, import_err = dynamic_load_class(import_path="xj_flow.models", class_name="FlowNode")
            if import_err:
                return [], import_err
            BaseInfo, import_err = dynamic_load_class(import_path="xj_user.models", class_name="BaseInfo")
            if import_err:
                return [], import_err

            flow_id_map = FlowNode.objects.filter(id=flow_node_id).values("flow_id").first()
            if not flow_id_map or not flow_id_map.get("flow_id") == 3:
                return [], import_err

            user_id_map = Enroll.objects.filter(id=relate_data_value).values("user_id").first()
            user_id_list = list(EnrollRecord.objects.filter(enroll_id=relate_data_value).exclude(enroll_status_code__in=[124, 234]).values("user_id"))
            user_id_list = [i["user_id"] for i in user_id_list] + [user_id_map.get("user_id")]
            phone_list = BaseInfo.objects.filter(id__in=user_id_list).values("phone")
            phone_list = [i["phone"] for i in phone_list]
        except Exception as e:
            write_to_log(prefix="process 触发发送短信验证码-index-0", err_obj=e)
            return [], None
        return phone_list, None

    def process(self, *args, **kwargs):
        # ============ section 报名联动触发短信 start ============
        try:
            phone_list, err = self.get_send_phones(
                flow_node_id=kwargs.get("flow_node_id"),
                relate_data_value=kwargs.get("relate_data_value")
            )
            SmsService, import_err = dynamic_load_class(import_path="xj_captcha.services.sms_service", class_name="SmsService")
            assert not import_err

            # 获取绑定的用户关系
            call_params = {"platform": "ALi", "type": "UNIFY"}
            # 触发发送短信验证码
            for i in phone_list:
                call_params["phone"] = i
                write_to_log(prefix="process 触发发送短信验证码-index-1", content=call_params)
                res, err = SmsService.bid_send_sms(call_params)

            if err:
                write_to_log(prefix="process 触发发送短信验证码-index-2", content=err)
        except Exception as e:
            write_to_log(prefix="process 触发发送短信验证码-index-3", err_obj=e)

        return "ok", None
        # ============ section 报名联动触发短信 end   ============
