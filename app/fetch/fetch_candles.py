from __future__ import annotations
from sqlalchemy.orm import Session
from typing import Optional
from app.models.pool_assets import PAssets
from app.models.assets import Asset_s


def get_pool_id(db: Session, pid: int):
    return (
        db.query(PAssets.pool_id, Asset_s.decimals)
		.join(Asset_s, Asset_s.id == PAssets.asset_1_id)
        .filter(PAssets.pool_id == pid)
		.filter(Asset_s.id == PAssets.asset_1_id)
        .filter(PAssets.pool == "TMPOOL11")
        .all()
    )


def get_candle_count(
    db: Session, timeframe: Optional[str] = None, pool_id: Optional[int] = None
):
    return db.execute(
        f"""
						WITH buckets AS (
							SELECT count(*) AS count_1
							FROM (						
							SELECT
							pool_id,
							time_bucket('{timeframe}', timestamp) AS datetime
							FROM tx_pool
							WHERE pool_id = {pool_id}
							GROUP BY datetime, pool_id
							ORDER BY datetime asc
							)s)
						select count_1 from buckets
						"""
    )


def candleStickss(
    db: Session,
    limit: Optional[int] = None,
    timeframe: Optional[str] = None,
    pool_id: Optional[int] = None,
    offset: Optional[int] = None,
    roundd: Optional[int] = None,
    from_: Optional[int] = None,
    to_: Optional[int] = None,
):
    return db.execute(
        f""" 
			SELECT
			time_bucket('{timeframe}', timestamp) AS datetime,
			CASE
			WHEN lag(last(time, timestamp)) over(order by time_bucket('{timeframe}', timestamp)) is NULL
				THEN FIRST(time, timestamp)
			ELSE lag(last(time, timestamp)) over(order by time_bucket('{timeframe}', timestamp))
			END as open_time,						
			CASE
			WHEN lag(last(liquidity_2/liquidity_1, timestamp)) over(order by time_bucket('{timeframe}', timestamp)) is NULL
				THEN FIRST(liquidity_2/liquidity_1, timestamp)
			ELSE lag(last(liquidity_2/liquidity_1, timestamp)) over(order by time_bucket('{timeframe}', timestamp))
			END as open,
			LAST(liquidity_2/liquidity_1, timestamp) AS close,
			MIN(liquidity_2/liquidity_1) AS low,
			MAX(liquidity_2/liquidity_1) AS high,
			SUM(amount_2) as volume
			FROM tx_pool
			WHERE pool_id = {pool_id} and time >= {from_} and time <= {to_} and round >= {roundd}
			GROUP BY datetime, pool_id
			ORDER BY datetime asc
		"""
    )


def candleSticks(
    db: Session,
    limit: Optional[int] = None,
    timeframe: Optional[str] = None,
    pool_id: Optional[int] = None,
    offset: Optional[int] = None,
    roundd: Optional[int] = None,
    from_: Optional[int] = None,
    to_: Optional[int] = None,
):
    return db.execute(
        f"""						
			SELECT
			time_bucket('{timeframe}', timestamp) AS datetime,
			CASE
			WHEN lag(last(liquidity_2/liquidity_1, timestamp)) over(order by time_bucket('{timeframe}', timestamp)) is NULL
				THEN FIRST(liquidity_2/liquidity_1, timestamp)
			ELSE lag(last(liquidity_2/liquidity_1, timestamp)) over(order by time_bucket('{timeframe}', timestamp))
			END as open,
			LAST(liquidity_2/liquidity_1, timestamp) AS close,
			MIN(liquidity_2/liquidity_1) AS low,
			MAX(liquidity_2/liquidity_1) AS high,
			SUM(amount_2) as volume
			FROM tx_pool
			WHERE pool_id = {pool_id} and round >= {roundd}
			GROUP BY datetime, pool_id
			ORDER BY datetime asc
			LIMIT {limit} OFFSET {offset}
		"""
    )


def aggregateCandles(
    db: Session,
    limit: Optional[int] = None,
    timeframe: Optional[str] = None,
    pool_id: Optional[int] = None,
    offset: Optional[int] = None,
):
    return db.execute(
        f"""						
			select
			a.pool_id,
			bucket as datetime,
			CASE
			WHEN lag(close) over(order by bucket) is NULL
				THEN open
			ELSE lag(close) over(order by bucket)
			END as open,
			high,
			low,
			close,
			volume
			from {timeframe} aa
			INNER JOIN pool_assets a on aa.pool_id = a.pool_id
			WHERE a.pool_id = {pool_id}
			ORDER BY bucket asc
			LIMIT {limit} OFFSET {offset}
		"""
    )


def candleCount(db: Session, pool_id: Optional[int] = None):
    return db.execute(
        f"""
			select round from tx_pool where pool_id = {pool_id} order by timestamp asc limit 1 offset 20
		"""
    )


def getAggregateCount(
    db: Session, timeframe: Optional[str] = None, pool_id: Optional[int] = None
):
    return db.execute(
        f"""
			WITH buckets AS (
				SELECT count(*) AS count_1
				FROM (						
				SELECT
				a.pool_id
				from {timeframe} aa
				inner join pool_assets a on aa.pool_id = a.pool_id
				where a.pool_id = {pool_id}
				)s)
			select count_1 from buckets
		"""
    )

def candlestick_in_usd(
    db: Session,
    limit: Optional[int] = None,
    timeframe: Optional[str] = None,
    pool_id: Optional[int] = None,
    offset: Optional[int] = None
	):
	return db.execute(
	f"""
		with FirstToLastDate as (
			select
			aa.bucket,
			a.pool_id
			from {timeframe} aa
			INNER JOIN pool_assets a on a.pool_id = aa.pool_id
			where a.pool_id = {pool_id}
			order by aa.bucket
			LIMIT {limit} OFFSET {offset}
		)
		SELECT
			LAST(pool_id, pool_id),
			FIRST(bucket, bucket),
			LAST(bucket, bucket)
			from FirstToLastDate
	"""
	)
def joinAlgoTable(
    db: Session,
    timeframe: Optional[str] = None,
	firstDate: Optional[str] = None,
    lastDate: Optional[str] = None,
	mainStatement: Optional[str] = None,
):
	return print(
	f"""
		with pucker as (
			SELECT 
			a.pool_id,
			time_bucket_gapfill('{timeframe}', timestamp) AS bucket,
			locf(LAST(liquidity_1/liquidity_2, timestamp)) AS close,
			locf(first(liquidity_1/liquidity_2, timestamp)) AS open,
			locf(MIN(liquidity_1/liquidity_2)) AS low,
			locf(MAX(liquidity_1/liquidity_2)) AS high
			FROM tx_pool s
			INNER JOIN pool_assets a ON a.pool_id = s.pool_id				
			WHERE a.pool_id = 552647097
			and time_bucket('{timeframe}', timestamp) >= '{firstDate}'
			and time_bucket('{timeframe}', timestamp) <= '{lastDate}'
			GROUP BY bucket, a.pool_id
			ORDER BY bucket
		) {mainStatement}
	"""
	)

def candlesticksUsd(
    limit: Optional[int] = None,
	offset: Optional[int] = None,
    timeframe: Optional[str] = None,
    pool_id: Optional[int] = None,
	firstDate: Optional[str] = None,
    lastDate: Optional[str] = None	
):
	return f"""
		select
		pool_assets.pool_id,
		aa.bucket as datetime,
		CASE
		WHEN lag(aa.close) over(order by aa.bucket) is NULL
			THEN round(aa.open*a.open, 6)
		ELSE lag(round(aa.close*a.close, 6)) over(order by aa.bucket)
		END as open,
		round(aa.high*a.high, 6) as high,
		round(aa.low*a.low, 6) as low,
		round(aa.close*a.close, 6) as close,
		aa.volume
		from {timeframe} aa
		INNER JOIN pucker a on a.bucket = aa.bucket	
		INNER JOIN pool_assets on pool_assets.pool_id = aa.pool_id
		where pool_assets.pool_id = {pool_id}
		and aa.bucket >='{firstDate}' and
		aa.bucket <= '{lastDate}'		
		order by aa.bucket
		LIMIT {limit}
	"""
	
# 	"""
# 	 with pucker as (
# 			select
# 			first(aa.bucket, aa.bucket),
# 			last(aa.bucket, aa.bucket)
# 			from candles_hourly aa
# 			INNER JOIN pool_assets on pool_assets.pool_id = aa.pool_id
# 			where pool_assets.pool_id = 552655440
# 			group by pool_assets.pool_id, aa.bucket
# 			order by aa.bucket
# 			limit 100 offset 0
# )
# 			select
# 			first(first, first),
# 			last(last, last)
# 			from pucker
# ) select
# 			pool_assets.pool_id,
# 			zzz.first,
# 			aa.bucket as datetime,
# 			CASE
# 			WHEN lag(aa.close) over(order by aa.bucket) is NULL
# 				THEN round(aa.open*a.open, 6)
# 			ELSE lag(round(aa.close*a.close, 6)) over(order by aa.bucket)
# 			END as open,
# 			round(aa.high*a.high, 6) as high,
# 			round(aa.low*a.low, 6) as low,
# 			round(aa.close*a.close, 6) as close,
# 			aa.close,
# 			aa.volume
# 			from candles_hourly aa
# 			LEFT JOIN zzz on zzz.first = aa.bucket
# 			left join (
# 							SELECT 
# 							a.pool_id,
# 							time_bucket('1 hour', timestamp) AS bucket, 
# 							CASE
# 								WHEN lag(last(liquidity_1/liquidity_2, timestamp)) over(order by time_bucket('1h', timestamp)) is NULL
# 									THEN FIRST(liquidity_1/liquidity_2, timestamp)
# 								ELSE lag(last(liquidity_1/liquidity_2, timestamp)) over(order by time_bucket('1h', timestamp))
# 							END as open,
# 							LAST(liquidityq_1/liquidity_2, timestamp) AS close,
# 							MIN(liquidity_1/liquidity_2) AS low,
# 							MAX(liquidity_1/liquidity_2) AS high
# 							FROM tx_pool s
# 							INNER JOIN pool_assets a ON a.pool_id = s.pool_id				
# 							WHERE a.pool_id = 552647097 and  timestamp > '2022-01-19 09:00:00+00' and timestamp < '2022-01-23 14:00:00+00'
# 							GROUP BY bucket, a.pool_id
# 							ORDER BY bucket
# 			) a on a.bucket = aa.bucket			
# 			INNER JOIN pool_assets on pool_assets.pool_id = aa.pool_id
# 			where pool_assets.pool_id = 552655440
# 			order by aa.bucket
# 			limit 100
# 	"""