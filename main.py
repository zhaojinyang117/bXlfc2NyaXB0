from modify_data_report import data_report
from modify_wechat_template_info import WeChat_template


def main():
    while True:
        try:
            index = int(
                input(
                    "请输入要启动的脚本编号：\n[1] 数据报告生成脚本\n[2] 微信模板生成脚本\n"
                )
            )
            break
        except ValueError:
            print("请输入一个有效的数字！")

    match index:
        case 1:
            data_report()
        case 2:
            WeChat_template()
        case _:
            print("输入错误，请重新运行脚本")


if __name__ == "__main__":
    main()
