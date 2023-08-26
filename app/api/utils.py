from fastapi.encoders import jsonable_encoder

def paginationFast(count, pools, offset, limit, sort_by, order):
    response = {
        "count": count,
        "next": None,   
        "previous": None,   
        "results": list(pools)
    }
    if offset is not None and offset >= count:
        if offset > 10:
            response["previous"] = f"{offset-10}"
        else:
            response["previous"] = None
    else:
        if offset is not None and offset >= 10:
            response["previous"] = f"{offset-10}"
        else:
            response["previous"] = None
    if offset is not None and (count-offset) <= 10:
        response["next"] = None
    else:
        if offset is None:
            response["next"] = f"10&"
        else:
            response["next"] = f"{offset+10}"
    return jsonable_encoder(response)

def paginationFastt(count, pools, offset):
    # print(jsonable_encoder(list(pools)))
    limit = 100
    response = {
        "c": count,
        "n": None,   
        "p": None,
        "l": None,
        "results": jsonable_encoder(list(pools))
    }
    # print(response)
    if offset is not None and offset >= count:
        if offset < count:
            response["p"] = f"{offset+100}"
        else:
            response["p"] = None
    else:
        if offset is not None and count-offset >= 100:
            response["p"] = f"{offset+100}"
        else:
            response["p"] = None
    if offset is not None and offset <= 0:
        response["n"] = None
    else:
        if offset is None:
            response["n"] = f"{count-100}"
        else:
            if offset <= 100:
                response["n"] = f"{0}"
            else:
                response["n"] = f"{offset-100}"
    if offset <= 100 and offset != 0:
        response["l"] = (offset - limit) + 100
                    
    return jsonable_encoder(response)

def paginationFasttt(count, pools, offset, limit):
    response = {
        "count": count,
        "next": None,   
        "previous": None,   
        "results": list(pools)
    }
    if offset is not None and offset >= count:
        if offset > limit:
            response["previous"] = f"{offset-limit}"
        else:
            response["previous"] = None
    else:
        if offset is not None and offset >= limit:
            response["previous"] = f"{offset-limit}"
        else:
            response["previous"] = None
    if offset is not None and (count-offset) <= limit:
        response["next"] = None
    else:
        if offset is None:
            response["next"] = f"10"
        else:
            response["next"] = f"{offset+limit}"
    return jsonable_encoder(response)

def paginationFastttt(count, pools, offset, limit, price):
    response = {
        "count": count,
        "next": None,   
        "previous": None,   
        "price_change": price,
        "results": list(pools)
    }
    if offset is not None and offset >= count:
        if offset > limit:
            response["previous"] = f"{offset-limit}"
        else:
            response["previous"] = None
    else:
        if offset is not None and offset >= limit:
            response["previous"] = f"{offset-limit}"
        else:
            response["previous"] = None
    if offset is not None and (count-offset) <= limit:
        response["next"] = None
    else:
        if offset is None:
            response["next"] = f"10"
        else:
            response["next"] = f"{offset+limit}"
    return jsonable_encoder(response)    

def get_time_table(timeframe):
    if timeframe == '12h':
        timeframe = 'candles_twelveH'
    if timeframe == '1d':
        timeframe = 'candles_daily'
    if timeframe == '4h':
        timeframe = 'candles_fourH'
    if timeframe == '1h':
        timeframe = 'candles_hourly'
    if timeframe == '30m':
        timeframe = 'candles_thirteenM'
    if timeframe == '15m':
        timeframe = 'candles_fifteenM'            
    if timeframe == '5m':
        timeframe = 'candles_fiveM'   
    if timeframe == '1m':
        timeframe = 'candles_oneM'           
    return timeframe