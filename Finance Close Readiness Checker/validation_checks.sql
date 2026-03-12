-- 1. Missing sales values
SELECT COUNT(*) AS missing_sales_count
FROM public.finance_data
WHERE sales IS NULL;

-- 2. Negative profit
SELECT COUNT(*) AS negative_profit_count
FROM public.finance_data
WHERE profit < 0;

-- 3. Duplicate records
SELECT
    date,
    country,
    product,
    sales,
    profit,
    COUNT(*) AS duplicate_count
FROM public.finance_data
GROUP BY date, country, product, sales, profit
HAVING COUNT(*) > 1;

-- 4. Remove fully blank rows for clean analysis
CREATE OR REPLACE VIEW public.finance_data_clean AS
SELECT *
FROM public.finance_data
WHERE NOT (
    date IS NULL
    AND country IS NULL
    AND product IS NULL
    AND sales IS NULL
    AND profit IS NULL
);

-- 5. Duplicate check on cleaned data
SELECT
    date,
    country,
    product,
    sales,
    profit,
    COUNT(*) AS duplicate_count
FROM public.finance_data_clean
GROUP BY date, country, product, sales, profit
HAVING COUNT(*) > 1;