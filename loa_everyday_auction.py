def calc_auction_price(value: int) -> str:
    def floor(val): return int(val)

    base = value * 0.95

    result = []
    for people, ratio in [(4, 3/4), (8, 7/8), (16, 15/16)]:
        buy_price = floor(base * ratio)
        bid_price = floor(buy_price / 1.1)
        result.append(f"{people}인 : {buy_price:,} G | {bid_price:,} G")

    output = "구매 최적가 | 입찰 적정가\n" + "\n".join(result)
    return output
