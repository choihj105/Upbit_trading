def Change(cur_price, rate):
    cur_price = float(cur_price)
    rate = float(rate)
    cur_price += (cur_price * (rate/100))
    
    # .. while 문으로 바꾸기..
    if cur_price > 0 and cur_price < 10:
        return round(cur_price, 4)
    elif cur_price >= 10 and cur_price <100:
        return round(cur_price, 3)
    elif cur_price >= 100 and cur_price <1000:
        return round(cur_price, 2)
    elif cur_price >= 1000 and cur_price <10000:
        return round(cur_price, 1)
    elif cur_price >= 10000 and cur_price <100000:
        return round(cur_price, 0)
    elif cur_price >= 100000 and cur_price <1000000:
        return round(cur_price, -1)
    elif cur_price >= 1000000 and cur_price <10000000:
        return round(cur_price, -2)
    elif cur_price >= 10000000 and cur_price <100000000:
        return round(cur_price, -3)
    elif cur_price >= 100000000 and cur_price <1000000000:
        return round(cur_price, -4)
    else:
        print("값이 없음")