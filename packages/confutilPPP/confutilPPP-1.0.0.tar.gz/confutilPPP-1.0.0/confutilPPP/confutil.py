import argparse
import os

import logPPP
import yaml


class confutil:
    def __init__(self):
        pass

    # 获取参数
    @staticmethod
    def _parse_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument("--configpath", nargs="+", help="配置文件")
        return parser.parse_args()

    # 检查解析参数
    @staticmethod
    def check_config(_object=None, filename='config'):
        if _object is None:
            _object = {}
        # 解析参数
        args = confutil._parse_arguments()
        args_config_path = args.configpath
        # 默认自定义配置
        default_path = os.path.join(os.getcwd(), f'{filename}.yaml')
        if not args_config_path:
            logPPP.warning("未填写自定义配置文件路径参数.")
        else:
            default_path = args_config_path[0]  # 自定义配置
        config_full_path_ = os.path.join(os.getcwd(), default_path)

        # 如果文件不存在或者为空，创建文件并写入
        if not os.path.isfile(config_full_path_) or os.path.getsize(config_full_path_) == 0:
            # 如果文件不存在，创建文件并写入
            with open(config_full_path_, 'w', encoding='utf_8') as f:
                f.write(yaml.dump(_object, indent=4, allow_unicode=True, sort_keys=False, default_flow_style=False))

        # 再次判断是否存在并规范路径
        if os.path.exists(config_full_path_):
            config_full_path_ = os.path.normpath(config_full_path_)
        if config_full_path_:
            logPPP.info(f"使用{config_full_path_}作为配置文件.")
            # 读取YAML文件
            with open(config_full_path_, 'r', encoding='utf_8') as f:
                try:
                    return yaml.safe_load(f)
                except OSError:
                    logPPP.error("配置 格式错误，检查配置文件格式是否正确！")
                    return False
        else:
            logPPP.error(f"未找到 {default_path} 配置文件\n请确定自定义配置文件已添加")
            return False
