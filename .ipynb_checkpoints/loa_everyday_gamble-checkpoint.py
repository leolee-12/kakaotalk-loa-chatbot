import random

def run_gamble():
    templates = [
        "실리안: 기사의 긍지를! {숫자}",
        "웨이: 시화류... 오의! {숫자}",
        "바훈투르: 이건 나의 에센스~ {숫자}",
        "니나브: 날... 믿어!! {숫자}",
        "이난나: 위대한 선조의 힘이여. {숫자}",
        "아제나: 여기서 끝내 주지. {숫자}",
        "샨디: 환영의 힘을 보여주마! {숫자}",
        "카단: 여긴 내가 맡지. {숫자}",
    ]
    number = random.randint(1, 100)
    template = random.choice(templates)
    return template.replace("{숫자}", str(number))
