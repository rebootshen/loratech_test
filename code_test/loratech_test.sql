select index2,month2, avg(average_price) as average_price2
from (
    select
        m.index as index2, t.ticker as ticker2,
        avg(t.price) as average_price,
        TO_CHAR(m.month,'YYYYMM') as  month2
    from 
        imported_closes t   
    INNER JOIN monthly_members m
    ON t.ticker = m.ticker and TO_CHAR(t.day,'YYYYMM') = TO_CHAR(m.month,'YYYYMM')
    WHERE 
        TO_CHAR(m.month,'YYYYMM') BETWEEN '200801' AND '201812' 
    group by 
        m.index, t.ticker, month2
    ORDER BY  
        m.index, t.ticker, month2
) as s
GROUP BY
      index2, month2;