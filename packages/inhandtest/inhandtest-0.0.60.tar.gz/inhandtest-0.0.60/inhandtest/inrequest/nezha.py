# -*- coding: utf-8 -*-
# @Time    : 2023/7/5 13:28:22
# @Author  : Pane Li
# @File    : nezha.py
"""
nezha

"""
import logging
import random
import re
import time
from inhandtest.exception import TimeOutError, ResourceNotFoundError
from inhandtest.tools import generate_string, replace_str, get_time_stamp
from inhandtest.inrequest.inrequest import InRequest


class Base:
    def __init__(self, api, email, host):
        self.api = api
        self.host = host
        self.email = email

    @property
    def me(self) -> dict:
        """ 获取me的各种信息 包括oid

        :return:
        """
        return self.api.send_request('/api/v1/users/me', method='get', param={"expand": 'org'}).json().get('result')


class Device(Base):

    def info(self, sn: str) -> dict:
        """根据sn 转换属性 属性值有：  online: 在线|离线   True|False
                                       iccid:
                                       imei:
                                       imsi:
                                       version: 固件版本
                                       licenseStatus: 'licensed'
                                       sn: 序列号
                                       address
                                       _id: 设备_id
                                       name: 设备名字
                                       org:  {'_id': oid, 'name': 'org_name', 'email': 'org_email'}
        :param sn: 列表
        :return: {'sn': $sn, 'online': 1, 'iccid': '', 'imei'}
        """

        try:
            response = self.api.send_request('/api/v1/devices', method='get', param={'serialNumber': sn}).json()
            return response.get('result')[0]
        except Exception:
            raise ResourceNotFoundError(f'the device {sn} not exist')

    def add(self, sn: str, mac_or_imei: str) -> None:
        """添加设备，

        :param sn: 设备序列号
        :param mac_or_imei: 添加设备时需要依赖设备的mac地址或者IMEI号，去生产库查询该设备是否是映翰通设备
        :return:
        """
        validated_field = self.api.send_request(f'api/v1/serialnumber/{sn}/validate', method='post').json().get(
            'result').get('validatedField')
        try:
            self.info(sn)
        except ResourceNotFoundError:
            self.api.send_request('api/v1/devices', 'post',
                                  body={"name": sn + str(int(time.time())), "serialNumber": sn, 'oid': self.me.oid,
                                        validated_field: mac_or_imei})
        logging.info(f"the {sn} device add success")

    def assert_state(self, sn: str, state: dict, timeout=120, interval=5) -> None:
        """校验设备基本状态

        :param sn: 序列号
        :param state:   支持表达式${value} ex: {'version': "'${value}' in 'V1.1.3.r4956'"}
                        online: 在线|离线   True|False
                        iccid:
                        imei:
                        imsi:
                        version: 固件版本
                        licenseStatus: 'licensed'
                        sn: 序列号
                        address
        :param timeout: 校验信息，最大超时时间
        :param interval: 校验信息，校验间隔时间
        :return: True or False
        """
        if state:
            for i in range(0, timeout, interval):
                result = self.info(sn)
                for key, value in state.items():
                    if '${value}' in value:
                        value = replace_str(value, {'${value}': result.get(key)})
                        logging.debug(f'start assert {sn} state {key} {value}')
                        try:
                            if not eval(value):
                                logging.debug(f'the {sn} device {key} info eval {value} is false')
                                break
                        except Exception as e:
                            logging.error(e)
                            break
                    else:
                        logging.debug(f'start assert {sn} state {key} {value}')
                        if result.get(key) != value:
                            logging.debug(f'the {sn} device {key} info value is {result.get(key)} not {value}')
                            break
                else:
                    logging.info(f"check {sn} device all state success")
                    break
                logging.info(f"check {sn} device state failed, please wait for {interval}s")
                time.sleep(interval)
            else:
                logging.exception(f"the {sn} state {state} check failed")
                raise TimeOutError(f"the {sn} state {state} check failed")

    def delete(self, sn: str or list) -> None:
        """

        :param sn: 设备序列号，一个或多个, sn='all' 时，删除所有设备
        :return:
        """

        def delete(ids: list):
            if ids:
                for _id in ids:
                    self.api.send_request(f'api/v1/devices/{_id}', 'delete')
                    logging.debug(f'{_id} device delete success')

        if sn == 'all':
            while True:
                devices = self.api.send_request(f'api/v1/devices', 'get', {'limit': 100, 'page': 0}).json().get(
                    'result')
                if devices:
                    delete([device.get('_id') for device in devices])
                else:
                    break
                logging.info(f'{self.email} user delete all device success')
        else:
            sn = [sn] if isinstance(sn, str) else sn
            delete([self.info(sn_).get('_id') for sn_ in sn])
            logging.info(f'{self.email} user delete {sn} device success')

    def bind_license(self, sn: list, licenses: dict):
        """ 绑定license

        :param sn
        :param licenses: {'slug': 'star_pro'}
        """
        licenses_ = []
        org_license = self.api.send_request('/api/v1/billing/licenses', 'get',
                                            param={'expand': 'org,device,type', 'limit': 200, 'page': 0},
                                            code=200).json().get('result')
        if org_license:
            for org in org_license:
                if org['status'] != 'expired' and org.get('device') is None and org['type']['slug'] == licenses.get(
                        'slug'):
                    licenses_.append(org['_id'])
        if len(licenses_) < len(sn):
            logging.error(f'licenses not enough, please check the licenses')
        else:
            device_ids = [self.info(sn_).get('_id') for sn_ in sn]
            for license_, _id in zip(licenses_, device_ids):
                self.api.send_request(f'/api/v1/billing/licenses/{license_}/device', 'put',
                                      body={'deviceId': _id},
                                      code=200)
            logging.info(f'bind license success')

    def assert_cellular_history(self, sn: str, state, delta_day=-1, data_interval=None):
        """

        :param sn:
        :param state:
        :param delta_day: 查询开始时间的起点， 默认晚一天时间
        :param data_interval: 当查询的时间越长时，返回的数据会少，防止页面在渲染时卡顿，所以返回的数据间隔增大，可以对间隔做判断， 单位秒
        :return:
        """
        time.sleep(2)

        def time_reduction(time_list, delta):
            """
            校验数据点时间差
            :param time_list: list of timestamp
            :param delta: int
            :return:
            """
            tmp = []
            for each in time_list:
                each = time.strptime(each, "%Y-%m-%dT%H:%M:%SZ")
                tmp.append(int(time.mktime(each)))
            t0 = tmp[0]
            for i in tmp[1:]:
                assert abs(t0 - i) == delta
                t0 = i

        payload = {
            "after": get_time_stamp(delta=delta_day, delta_type='d', time_format='%Y-%m-%dT16:00:00.000Z'),
            "before": get_time_stamp(time_format='%Y-%m-%dT16:00:00.000Z')
        }
        resp = self.api.send_request(f'/api/v1/devices/{self.info(sn).get("_id")}/signal', 'get',
                                     param=payload, code=200).json().get('result').get('series')
        fields = resp[0]['fields']
        cellular_state = []
        if state:
            for each_type in resp:
                for data in each_type["data"]:
                    temp = {"name": "signal", "tags": {"type": each_type["type"]}, "fields": {}}
                    if data[1]:
                        temp["timestamp"] = data[0]
                        for i in range(1, len(data)):
                            if data[i] != 0:
                                if data[i]:
                                    if i == 5:
                                        temp["fields"]["level"] = data[i] - 1
                                    temp["fields"][fields[i]] = data[i]
                            elif data[i] == 0:
                                temp["fields"][fields[i]] = 0
                        temp["fields"].pop("strength")
                        cellular_state.append(temp)
                        assert temp in state, '查询结果不对'
            assert len(cellular_state) == len(state), '查询结果不对'
        if data_interval is not None:
            cellular_type = []
            for each_type in resp:
                cellular_type.append(each_type['type'])
                timestamp_ls = [i[0] for i in each_type['data']]
                time_reduction(timestamp_ls, delta=data_interval)
            assert len(cellular_type) == len(set(cellular_type)), '蜂窝历史返回数据不对'


class Config(Base):

    def __init__(self, api, email, host):
        super().__init__(api, email, host)
        self.__device = Device(api, email, host)
        self.__group = Group(api, email, host)

    def send(self, sn: str, payload: dict, commit=True) -> dict:
        """下发设备配置

        :param sn: 设备序列号
        :param commit: 是否提交, 在云端可以保存配置，默认是提交
        :param payload: 配置内容，当配置中的key是随机id时， 可使用$id，下发时会自动替换成随机id
        :return:
        """

        def switch_config(in_payload: dict) -> dict:
            """转换配置，当配置中的key是随机id时， 可使用$id, 然后该函数会自动替换成随机id并返回

            :param in_payload: 需要修正的配置项，其中需要更新的key 使用$id来替换
            :return:
            """
            local_time = str(hex(int(time.time())))[2:]
            start = f'000{random.randint(1, 9)}{local_time}'
            in_payload = str(in_payload)
            for i in range(0, len(re.findall('\$id', in_payload))):
                in_payload = in_payload.replace('$id',
                                                f'{start}{generate_string(4, uppercase=False, special_chars=False)}',
                                                1)
            return eval(in_payload)

        payload = switch_config(payload)
        session_id = \
            self.api.send_request('/api/v1/config/init', 'post',
                                  param={'deviceId': self.__device.info(sn).get('_id')},
                                  ).json().get('result').get('_id')
        header = {'x-session-id': session_id}
        resp = self.api.send_request('/api/v1/config', 'put', body=payload, header=header).json()
        assert resp == {'result': 'ok'}, 'save config failed'
        if commit:
            resp = self.api.send_request('/api/v1/config/commit', 'post', header=header).json()
            assert resp == {'result': 'ok'}, 'commit config failed'
            logging.info(f'the device {sn} config commit success')
        return payload

    def get(self, sn: str, expect: dict, type_='actual') -> dict or None:
        """获取校验备配置

        :param sn: 设备序列号
        :param expect: 配置内容，完整的配置路径，如{'lan': {'type': 'dhcp'}}
        :param type_: actual 实际设备上传的配置
                      group 设备所在组的配置
                      pending 正在下发的配置
                      target 目标配置
                      individual 个性化配置
        :return: 如果 expect 为None 就返回设备当前实际的配置
        """
        expect = {'result': {type_: expect}}
        if expect is not None:
            self.api.send_request(f'/api/v1/devices/{self.__device.info(sn).get("_id")}/config', 'get',
                                  expect=expect)
        else:
            return self.api.send_request(f'/api/v1/devices/{self.__device.info(sn).get("_id")}/config',
                                         'get').json().get('result').get(type_)

    def clear_config(self, sn: str):
        """清除设备配置

        :param sn:
        :return:
        """
        self.api.send_request(f'/api/v1/config/layer/device/{self.__device.info(sn).get("_id")}', 'delete',
                              expect={
                                  "result": 'ok'})
        self.get(sn, expect={}, type_='individual')

    def copy_config(self, source_sn: str, target_sns: list = None, target_group: list = None,
                    target_group_id: list = None):
        """清除设备配置

        :param source_sn: 源设备sn
        :param target_sns: 目标设备sn
        :param target_group: 目标分组名称
        :param target_group_id: 目标分组id
        :return:
        """
        if target_sns:
            body = {"sourceDeviceId": self.__device.info(source_sn).get("_id"),
                    "targetDeviceIds": [self.__device.info(device).get('_id') for device in target_sns]}
            self.api.send_request(f'/api/v1/config/layer/bulk-copy', 'post', body=body, expect={"result": 'ok'})
        if target_group or target_group_id:
            if not target_group_id:
                [self.__group.info(name).get('_id') for name in target_group]
            body = {"sourceDeviceId": self.__device.info(source_sn).get("_id"),
                    "targetGroupId": target_group_id}
            self.api.send_request(f'/api/v1/config/layer/bulk-copy', 'post', body=body, expect={"result": 'ok'})


class Org(Base):

    def org_info(self, name, _id=None, level=None) -> dict:
        for i in range(0, 20):  # 20次查询，如果组织数量超过100，就需要多次查询
            orgs = self.api.send_request('/api/v1/orgs', 'get', param={'depth': 5, 'limit': 100, 'page': i}).json()
            for org in orgs.get('result'):
                if level == 1 and org.get('level') == 1:
                    return org
                elif level:
                    if (org.get('name') == name or org.get('_id') == _id) and org.get('level') == level:
                        return org
                else:
                    if org.get('name') == name or org.get('_id') == _id:
                        return org
            if len(orgs.get('result')) <= 100:
                raise ResourceNotFoundError(f'org not found')

    def create(self, name: str, parent_name: str = None, level=2, email='', phone='', **kwargs) -> str:
        """创建组织, 创建2级组织时，parent_name和parent_id可以不传

        :param name: 组织名称 (在实现自动化时可让名称唯一，来实现创建组织的唯一性)
        :param parent_name: 父组织名称，如果组织名称唯一，可以传入，如果不唯一就拿第一个创建
        :param level: 组织层级，2 二级组织，3 三级组织 4 四级组织 5 五级组织
        :param email: 组织邮箱
        :param phone: 组织电话
        :param kwargs: 组织信息
               parent_id: 父组织id，唯一id，传入它时可以不用传入parent_name
               description: 组织描述
               force: 是否强制创建，如果组织已存在，是否强制创建
        :return: 组织id
        """
        if level in (2, 3, 4, 5):
            parent_level = level - 1
            parent_id = self.org_info(parent_name, kwargs.get('parent_id'), level=parent_level).get('_id')
            body = {'name': name, 'parent': parent_id, 'phone': phone, 'email': email,
                    'description': kwargs.get('description')}
            logging.info(f'create org {name} success')
            return self.api.send_request('/api/v1/orgs', 'post', body=body).json().get('result').get('_id')
        else:
            raise ValueError('level must be in (2, 3, 4, 5)')

    def delete(self, name: str, _id=None, ):
        """删除组织, 不能删除一级组织

        :param name: 组织名称, _id 为None时，使用名称删除，搜索到名称一致的组织就全部删除
        :param _id: 组织id, 使用id删除，精确删除
        :return:
        """
        id_ = self.org_info(name, _id).get('_id')
        self.api.send_request(f'/api/v1/orgs/{id_}', 'delete')
        logging.info(f'delete org success')

    def update_user(self, email: str, **kwargs):
        """更新用户

        :param email: 用户邮箱
        :param kwargs:
               password: 密码
        :return:
        """
        users = self.api.send_request('api/v1/users', 'get',
                                      param={'email': email, 'limit': 20, 'expand': 'roles,mfa,org'}).json().get(
            'result')
        if users:
            if kwargs.get('password'):
                for user in users:
                    if email == user.get('email'):
                        self.api.send_request(f'api/v1/users/{user.get("_id")}/password', 'put',
                                              body={'password': kwargs.get('password')})
                        logging.info(f'the {email} user update password success')
                        if self.email == email:
                            self.api = InRequest(self.host, email, kwargs.get('password'), 'star')  # 重新登录
                        break
                else:
                    logging.warning(f'the {email} user not exist')
        else:
            logging.warning(f'the {email} user not exist')


class Group(Base):
    def __init__(self, api, email, host):
        super().__init__(api, email, host)
        self.__org = Org(api, email, host)
        self.__device = Device(api, email, host)

    def info(self, name, _id=None) -> dict:
        for i in range(0, 20):  # 20次查询，如果组织数量超过100，就需要多次查询
            groups = self.api.send_request('/api/v1/devicegroups', 'get', param={'page': i, 'limit': 100}).json()
            for group in groups.get('result'):
                if group.get('name') == name or group.get('_id') == _id:
                    return group
            if len(groups.get('result')) <= 100:
                raise ResourceNotFoundError(f'group not found')

    def create(self, name: str, product: str, firmware: str, org_name: str, org_id=None) -> str:
        """创建分组

        :param name: 分组名称(在实现自动化时可让名称唯一，来实现创建分组的唯一性)
        :param product: 产品名称
        :param firmware: 固件版本
        :param org_name: 所属组织名称
        :param org_id: 组织id，唯一id，传入它时可以不用传入org_name
        :return: 组织id
        """
        org_id = org_id if org_id else self.__org.org_info(org_name).get('_id')
        body = {"name": name, "product": product, "firmware": firmware, "oid": org_id}
        result = self.api.send_request('/api/v1/devicegroups', 'post', body=body).json()
        logging.info(f'create group {name} success')
        return result.get('result').get('_id')

    def delete(self, name: str or list, _id: str or list = None, ):
        """删除分组

        :param name: 分组名称, _id 为None时，使用名称删除，搜索到名称一致的分组只删除第一个
        :param _id: 分组id, 使用id删除，精确删除
        :return:
        """
        if _id:
            if isinstance(_id, str):
                _id = [_id]
        else:
            if name:
                if isinstance(name, str):
                    _id = [self.info(name=name).get('_id')]
                else:
                    _id = [self.info(group_name).get('_id') for group_name in name]
        if _id:
            self.api.send_request('/api/v1/devicegroups/remove', 'post', body={'ids': _id})
        logging.info(f'delete groups success')

    def move(self, sn: list, group_name: str, group_id: str = None, type_='in'):
        """移动设备到分组

        :param sn: 设备sn列表
        :param group_name: 分组名称
        :param group_id: 分组id 二选一, 传入id时，不用传入group_name
        :param type_: 移动类型，in: 移入分组， out: 移出分组
        :return:
        """
        group = self.info(group_name, group_id)
        if type_ == 'in':
            items = [{"deviceId": info.get('_id'), "deviceGroupId": group.get('_id'), 'oid': group.get('oid')} for info
                     in [self.__device.info(sn_) for sn_ in sn]]
        else:
            items = [{"deviceId": info.get('_id'), 'oid': group.get('oid')} for info in
                     [self.__device.info(sn_) for sn_ in sn]]
        self.api.send_request('/api/v1/devices/move', 'put', body={'items': items})
        logging.info(f'move device {sn} {type_} group success')

    def get_config(self, group_name: str, expect: dict, type_='actual', group_id: str = None) -> dict or None:
        """分组获取配置校验

        :param group_name: 设备序列号
        :param expect: 配置内容，完整的配置路径，如{'lan': {'type': 'dhcp'}}
        :param type_: actual 实际设备上传的配置
                      group 设备所在组的配置
                      pending 正在下发的配置
                      target 目标配置
                      individual 个性化配置
        :param group_id: 分组id 二选一, 传入id时，不用传入group_name
        :return: 如果 expect 为None 就返回分组当前实际的配置
        """
        expect = {'result': {type_: expect}}
        _id = self.info(group_name, group_id).get('_id')
        if expect is not None:
            self.api.send_request(f'/api/v1/config/layer/group/{_id}', 'get', expect=expect)
        else:
            return self.api.send_request(f'/api/v1/config/layer/group/{_id}', 'get').json().get('result').get(type_)


class StarInterface:

    def __init__(self, email, password, host='star.inhandcloud.cn'):
        """ 须确保用户关闭了多因素认证

        :param email  平台用户名
        :param password  平台密码
        :param host: 'star.inhandcloud.cn'|'star.inhandcloud.cn'|'star.nezha.inhand.dev'|'star.nezha.inhand.design' 平台是哪个环境,
        """
        self.api = InRequest(host, email, password, 'star')
        self.device = Device(self.api, email, host)
        self.config = Config(self.api, email, host)
        self.org = Org(self.api, email, host)
        self.group = Group(self.api, email, host)


if __name__ == '__main__':
    from inhandtest.log import enable_log

    enable_log(console_level='debug')
    star = StarInterface('liwei@inhand.com.cn', '123456', 'star.nezha.inhand.design')
    print(star.device.delete('MR8051234501166'))
