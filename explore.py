import pandas as pd

daily = pd.read_parquet("data/1_prepared_views/prepared_daily_view.parquet")
print(daily.shape)   # (56110, 44): one row per machine per day
print(daily.head()) #hello


import duckdb

duckdb.sql("""
    SELECT machine_id,
           SUM(house_win_usd)                    AS house_win,
           SUM(theo_usd)                         AS expected_win,
           SUM(house_win_usd) / NULLIF(SUM(coin_in_usd), 0) AS observed_hold,
           SUM(available_hours) /
               (SUM(c.scheduled_seconds) / 3600.0) AS availability
    FROM 'data/1_prepared_views/prepared_daily_view.parquet' AS d
    JOIN 'data/2_machine_decision/calendar_day.parquet' AS c
      USING (gaming_date)
    WHERE d.active
    GROUP BY machine_id
    ORDER BY house_win
    LIMIT 10
""").show()