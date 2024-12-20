import re
import pyperclip
import time


def WeChat_template():
    def parse_info(text):
        # 修改正则表达式，使用.*来匹配面积后的所有内容
        pattern = (
            r"((\d{4})?\s*(\d{1,2}:\d{2})\s+(\d+)\s+(.*)|(\d{6})-(\d{4})-(\d+)\s+(.*))"
        )
        match = re.match(pattern, text.strip())
        if match:
            # 第一种格式
            if match.group(2):  # 如果有年份
                date = match.group(2)
                time = match.group(3)
                area = match.group(4)
                address = match.group(5).strip()  # 添加strip()去除可能的首尾空格
            else:  # 第二种格式
                date = (
                    f"{match.group(6)[:2]}.{match.group(6)[2:4]}.{match.group(6)[4:]}"
                )
                time = f"{match.group(7)[:2]}:{match.group(7)[2:]}"
                area = match.group(8)
                address = match.group(9).strip()  # 添加strip()去除可能的首尾空格
            return date, time, area, address
        else:
            return None

    def modify_template1(template, date, time, area, address):
        template = template.replace("治理面积：130", f"治理面积：{area}")
        template = template.replace(
            "治理时间：2024.12.16 18:00", f"治理时间：{date} {time}"
        )
        template = template.replace(
            "上门地址：四川省成都市双流区成都市 双流区 怡心街道 星月湖畔 6栋 1402号",
            f"上门地址：{address}",
        )
        return template

    def modify_template2(template, time):
        template = template.replace("18:00", time)
        return template

    # 示例模板1和模板2
    template1 = """您好，我是希望树治理人员杜剑，已接收到您的订单
    治理面积：130
    治理时间：2024.12.16 18:00
    上门地址：四川省成都市双流区成都市 双流区 怡心街道 星月湖畔 6栋 1402号

    为了保障正常施工，现场情况需要跟您确认一下：
    1）卫生情况：确保家具表面无明显灰尘、水渍等；
    2）柜体情况：清空所有抽屉柜子内物品、保管好贵重物品；
    3）已使用场所：可把所有物品清理打包放在大理石桌面、或瓷砖地面上；
    4）如施工开始前，发现房屋内有物品破损，会拍照群内反馈
    5）为了保障数据检测准确性，检测室温要求在22～28℃左右；门窗密闭（形成独立空间）12小时左右；如到现场后，若未进行密闭则无法检测采样，请知悉

    如现场实际治理面积与所拍订单面积相差超过10平方米，需现场补差价，请悉知。
    """
    template2 = "您好，明天我们2名施工人员上门做空气治理的施工，施工当天的过程和部分细节，会同步在群内，明天我们预计会在18:00之前到达"

    # 交互式输入
    print("请输入治理信息（格式：日期 时间 面积 地址 或 日期-时间-面积 地址）：")
    input_info = input().strip()

    # 解析信息
    info = parse_info(input_info)
    if info:
        date, time_str, area, address = info
        modified_template1 = modify_template1(template1, date, time_str, area, address)
        modified_template2 = modify_template2(template2, time_str)

        # 将修改后的模板写入剪贴板，并等待一下确保操作系统有时间处理
        pyperclip.copy(modified_template1)
        print("\n修改后的模板1已复制到剪贴板：")
        print(modified_template1)
        time.sleep(1)  # 等待1秒以确保剪贴板历史记录有时间更新

        pyperclip.copy(modified_template2)
        print("\n修改后的模板2已复制到剪贴板：")
        print(modified_template2)
    else:
        print("无法解析输入信息。")

