"""
Global Gold Market Pulse - source data module
================================================
PRIMARY SOURCE (reserves + historical trend + net buyers/sellers): the
user-supplied World Gold Council / IMF International Financial Statistics
extracts, downloaded directly from https://www.gold.org/goldhub/data/gold-reserves-by-country:
  - World_official_gold_holdings_as_of_Sep2026_IFS.xlsx  (snapshot, 100 entities)
  - Quarterly_gold_and_FX_Reserves_Q2_2026.xlsx           (quarterly time series, Q1 2000-Q2 2026)
  - Changes_latest_as_of_Sep2026_IFS.xlsx                 (annual net change by country, 2002-2026 YTD)
  - CBGA_sales.xlsx                                       (1999-2009 Central Bank Gold Agreement sales, for historical context)
These are official IMF IFS reporting-country data as republished by the World
Gold Council; every number below traces back to a specific cell in those
files. Figures are NOT randomly generated or estimated.

SECONDARY SOURCES (production, price history, demand-by-sector - not covered
by the IFS reserve files): USGS Mineral Commodity Summaries 2026 and World
Gold Council Gold Demand Trends FY2025 / metalcharts.org, cited inline.

Generated for: Milad Shabani's BI/data portfolio (miladshabani.ir)
"""

GENERATED_NOTE = (
    "Reserve figures are the World Gold Council / IMF IFS official dataset "
    "as of the September 2026 IFS publication (user-supplied source files). "
    "Production, price and demand figures are compiled from USGS and World "
    "Gold Council Gold Demand Trends. See the Sources sheet / dashboard "
    "footer for exact citations and 'as of' dates for every table."
)

WORLD_TOTAL_RESERVES_TONNES = 36829.28
EURO_AREA_TOTAL_TONNES = 10807.64
RESERVES_AS_OF = "World Gold Council / IMF IFS, September 2026 publication (holdings dated Apr-Jul 2026 per country)"

RESERVES_BY_COUNTRY = [
    (1, "United States", 8133.46, 0.8141, "Jul 2026"),
    (2, "Germany", 3349.48, 0.8100, "Apr 2026"),
    (4, "Italy", 2451.84, 0.7706, "Jul 2026"),
    (5, "France", 2436.97, 0.7854, "Apr 2026"),
    (6, "China", 2366.33, 0.0808, "Jul 2026"),
    (7, "Russia", 2276.76, 0.4131, "Jul 2026"),
    (8, "Switzerland", 1039.94, 0.1238, "Jun 2026"),
    (9, "India", 880.51, 0.1624, "Jul 2026"),
    (10, "Japan", 845.97, 0.0851, "Jun 2026"),
    (11, "Poland", 640.21, 0.2817, "Jul 2026"),
    (12, "Netherlands", 612.45, 0.7001, "Apr 2026"),
    (13, "Turkey", 529.20, 0.5179, "Jul 2026"),
    (15, "Uzbekistan", 430.78, 0.8715, "Jul 2026"),
    (16, "Taiwan", 423.94, 0.0835, "Apr 2026"),
    (17, "Portugal", 382.66, 0.7575, "Apr 2026"),
    (18, "Kazakhstan", 369.76, 0.7550, "Jul 2026"),
    (19, "Saudi Arabia", 323.07, 0.0790, "May 2026"),
    (20, "United Kingdom", 310.29, 0.1924, "Jul 2026"),
    (21, "Lebanon", 286.83, 0.7908, "Mar 2025"),
    (22, "Spain", 281.58, 0.2948, "Apr 2026"),
    (23, "Austria", 280.05, 0.7134, "Jun 2026"),
    (24, "Thailand", 234.52, 0.1103, "Jul 2026"),
    (25, "Belgium", 227.40, 0.5500, "Jun 2026"),
    (26, "Singapore", 203.54, 0.0588, "Jul 2026"),
    (30, "Brazil", 172.44, 0.0607, "Jun 2026"),
    (33, "Philippines", 133.52, 0.1676, "Jul 2026"),
    (36, "South Africa", 125.53, 0.2217, "Jul 2026"),
    (37, "Mexico", 120.04, 0.0573, "Jun 2026"),
    (44, "Indonesia", 87.04, 0.0776, "Jul 2026"),
    (46, "Australia", 79.87, 0.1429, "Jul 2026"),
]
REGION = {
    "United States": "Americas", "Germany": "Europe", "Italy": "Europe", "France": "Europe",
    "China": "Asia-Pacific", "Russia": "Europe", "Switzerland": "Europe", "India": "Asia-Pacific",
    "Japan": "Asia-Pacific", "Poland": "Europe", "Netherlands": "Europe", "Turkey": "Europe",
    "Uzbekistan": "Asia-Pacific", "Taiwan": "Asia-Pacific", "Portugal": "Europe",
    "Kazakhstan": "Asia-Pacific", "Saudi Arabia": "Middle East", "United Kingdom": "Europe",
    "Lebanon": "Middle East", "Spain": "Europe", "Austria": "Europe", "Thailand": "Asia-Pacific",
    "Belgium": "Europe", "Singapore": "Asia-Pacific", "Brazil": "Americas", "Philippines": "Asia-Pacific",
    "South Africa": "Africa", "Mexico": "Americas", "Indonesia": "Asia-Pacific", "Australia": "Asia-Pacific",
}

INSTITUTIONAL_HOLDERS = [
    ("IMF", 2814.04, "Jun 2026"),
    ("European Central Bank", 508.41, "Jan 2026"),
    ("Bank for International Settlements", 102.0, "Mar 2026"),
]
RESERVES_SOURCE = (
    "World Gold Council / IMF International Financial Statistics, September "
    "2026 publication (source: https://www.gold.org/goldhub/data/gold-reserves-by-country, "
    "file: World_official_gold_holdings_as_of_Sep2026_IFS.xlsx). World total "
    "across all 100 IFS-reporting entities: 36,829.3 tonnes."
)

WORLD_RESERVES_TREND = [
    (2000, 33212.5), (2001, 32933.3), (2002, 32563.7), (2003, 32006.0),
    (2004, 31487.2), (2005, 30883.9), (2006, 30518.9), (2007, 30014.4),
    (2008, 30002.3), (2009, 30526.8), (2010, 30847.7), (2011, 31213.8),
    (2012, 31688.9), (2013, 32036.5), (2014, 32270.8), (2015, 33017.9),
    (2016, 33593.4), (2017, 34003.2), (2018, 34233.0), (2019, 34781.5),
    (2020, 35305.0), (2021, 35532.9), (2022, 35508.0), (2023, 36002.9),
    (2024, 36254.0), (2025, 36572.0), (2026.5, 36829.3),
]
WORLD_RESERVES_TREND_SOURCE = (
    "Quarterly_gold_and_FX_Reserves_Q2_2026.xlsx, 'Gold (Tonnes)' sheet, "
    "World row, Q4 snapshot of each year (Q2 2026 for the latest point). "
    "CBGA = Central Bank Gold Agreement (1999-2009), under which European "
    "central banks coordinated gross sales of gold; reserves have risen "
    "almost every year since 2009 as central banks became net buyers."
)

COUNTRY_HISTORY = {
    "United States": [(2000,8136.9),(2005,8135.1),(2010,8133.5),(2015,8133.5),(2020,8133.5),(2025,8133.5),(2026.5,8133.5)],
    "Germany":       [(2000,3468.6),(2005,3427.8),(2010,3401.0),(2015,3381.0),(2020,3362.4),(2025,3350.3),(2026.5,3349.5)],
    "China":         [(2000,395.0),(2005,600.0),(2009,1054.1),(2015,1762.3),(2019,1948.3),(2022,2010.5),(2025,2306.3),(2026.5,2366.3)],
    "Russia":        [(2000,384.4),(2005,386.9),(2010,788.6),(2015,1414.5),(2019,2271.2),(2022,2332.7),(2025,2326.5),(2026.5,2277.0)],
    "India":         [(2000,357.8),(2009,557.7),(2015,557.7),(2018,600.4),(2021,754.1),(2024,876.2),(2026.5,880.5)],
    "Poland":        [(2000,102.8),(2017,103.0),(2019,228.6),(2022,228.7),(2023,358.7),(2024,448.2),(2025,550.2),(2026.5,632.4)],
    "Japan":         [(2000,763.5),(2020,765.2),(2021,846.0),(2026.5,846.0)],
    "Netherlands":   [(2000,911.8),(2005,694.9),(2008,612.5),(2026.5,612.5)],
    "United Kingdom":[(2000,487.5),(2001,355.2),(2002,313.9),(2005,310.8),(2010,310.3),(2015,310.3),(2020,310.3),(2025,310.3),(2026.5,310.3)],
    "Switzerland":   [(2000,2419.4),(2002,1916.7),(2004,1354.3),(2006,1290.1),(2008,1040.1),(2015,1040.0),(2020,1040.0),(2025,1039.9),(2026.5,1039.9)],
    "Turkey":        [(2000,116.3),(2016,116.1),(2017,202.0),(2019,379.0),(2021,394.2),(2022,541.8),(2024,587.6),(2025,614.3),(2026.5,530.6)],
    "Kazakhstan":    [(2000,57.2),(2010,67.3),(2015,221.8),(2019,385.5),(2021,402.4),(2023,294.2),(2025,341.0),(2026.5,368.4)],
}
COUNTRY_HISTORY_SOURCE = WORLD_RESERVES_TREND_SOURCE
COUNTRY_HISTORY_NOTES = {
    "United Kingdom": "The 2000-2002 drop is the Bank of England's famous 'Brown's Bottom' sale of ~395t at a multi-decade price low.",
    "Switzerland": "The Swiss National Bank sold roughly 1,380t of gold between 2000-2008 following a 1997 referendum revaluing its reserves; holdings have been essentially flat since.",
    "Turkey": "Reported reserves fell from 614.3t (Q4 2025) to 530.6t (Q2 2026) per IFS data, even after 2025 was a net-buying year (+40.25t) — a reminder that official figures can move for reasons beyond open-market buying/selling (e.g. commercial-bank gold swaps that the central bank intermediates).",
    "Saudi Arabia": "Holdings jumped from 143t to 323t in a single step in 2008 — a one-time statistical reclassification of previously-held gold onto the central bank's balance sheet, not a market purchase.",
}

# ---------------------------------------------------------------------------
# CBGA (Central Bank Gold Agreement) sales, 1999-2019 - the "selling era"
# Source: CBGA_sales.xlsx, sheets "CBGA" (per-country CBGA1 breakdown) and
# "Sheet1" (agreement-year totals, mapped to calendar year of the agreement
# year's end). Retired forever - the agreements were not renewed after 2019
# as central banks had become structural net buyers.
# ---------------------------------------------------------------------------
CBGA_ANNUAL_SALES = [
    (2000, 400.0, 400), (2001, 404.0, 400), (2002, 393.1, 400), (2003, 418.1, 400),
    (2004, 385.0, 400), (2005, 497.2, 500), (2006, 395.6, 500), (2007, 475.2, 500),
    (2008, 358.3, 500), (2009, 156.6, 500), (2010, 136.1, 400), (2011, 53.3, 400),
    (2012, 5.9, 400), (2013, 5.1, 400), (2014, 6.8, 400), (2015, 3.4, None),
    (2016, 3.1, None), (2017, 4.2, None), (2018, 4.0, None), (2019, 3.0, None),
]
CBGA_COUNTRY_TOTALS_CBGA1 = [  # 5-year totals, Sept 1999 - Sept 2004, tonnes
    ("Switzerland", 1170.0), ("United Kingdom", 345.0), ("Netherlands", 235.2),
    ("Portugal", 124.8), ("Austria", 90.0), ("Germany", 35.2),
]
CBGA_SOURCE = (
    "CBGA_sales.xlsx (World Gold Council, sourced from IMF IFS / ECB Weekly "
    "Financial Statement), sheets 'CBGA' and 'Sheet1'. Under three "
    "successive Central Bank Gold Agreements (1999-2019), European central "
    "banks coordinated and capped their gross gold sales; the agreements "
    "were quietly left to lapse after 2019 as signatories had become "
    "structural net buyers instead."
)

TOP_BUYERS_2025 = [
    ("Poland", 101.98), ("Kazakhstan", 56.99), ("Azerbaijan (SOFAZ)", 53.40),
    ("Brazil", 42.79), ("Turkey", 40.25), ("China", 26.75), ("Czech Rep.", 20.43),
    ("Iraq", 11.97), ("Cambodia", 7.96), ("Uzbekistan", 7.78),
]
TOP_SELLERS_2025 = [
    ("Singapore", -26.41), ("Ghana", -11.92), ("Russia", -6.22),
    ("Germany", -1.28), ("Mexico", -0.17),
]
TOP_BUYERS_3YR_2023_2025 = [
    ("Poland", 321.54), ("China", 295.79), ("Azerbaijan (SOFAZ)", 98.20),
    ("India", 92.97), ("Turkey", 71.95), ("Czech Rep.", 59.65),
    ("Iraq", 44.29), ("Brazil", 42.79), ("Singapore", 39.81), ("Libya", 30.01),
]
TOP_BUYERS_2026_YTD = [
    ("Poland", 89.99), ("China", 60.03), ("Uzbekistan", 40.43),
    ("Kazakhstan", 28.71), ("Czech Rep.", 12.47), ("Singapore", 9.98),
    ("Chile", 9.55), ("Malaysia", 5.91), ("Ghana", 5.79),
]
CHANGES_SOURCE = (
    "Changes_latest_as_of_Sep2026_IFS.xlsx, 'Annual' sheet (World Gold "
    "Council / IMF IFS). 2026 column is year-to-date through the September "
    "2026 publication, not a full calendar year."
)

POLAND_BUILD = [
    ("2017", 103.0), ("2019", 228.6), ("2022", 228.7), ("2023", 358.7),
    ("2024", 448.2), ("2025", 550.2), ("Q2 2026", 632.4),
]
POLAND_NOTE = (
    "Poland has been the single largest net buyer of gold of any central "
    "bank over 2023-2026 (+321.5t cumulative 2023-2025, +90t further in "
    "2026 YTD), more than quintupling its reserve since 2017 as part of a "
    "publicly stated diversification strategy."
)

PRODUCTION_AS_OF = "2025 estimate (USGS Mineral Commodity Summaries 2026)"
PRODUCTION_BY_COUNTRY = [
    ("China", 380), ("Russia", 310), ("Australia", 280), ("Canada", 200),
    ("United States", 160), ("Ghana", 150), ("Mexico", 140), ("Kazakhstan", 130),
    ("Uzbekistan", 130), ("Peru", 110), ("Indonesia", 100), ("South Africa", 95),
    ("Brazil", 80), ("Sudan", 75), ("Mali", 65),
]
PRODUCTION_WORLD_TOTAL_2025 = 3300
PRODUCTION_WORLD_TOTAL_2024 = 3280
PRODUCTION_SOURCE = (
    "USGS, Mineral Commodity Summaries 2026 - Gold "
    "(https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-gold.pdf): world "
    "total ~3,300t (2025) vs 3,280t (2024); China, Russia, Australia, Canada "
    "and the United States are named as the top five producers, in that "
    "order. Full top-15 country tonnages are a secondary compilation of the "
    "same USGS dataset (flagged as such since USGS's own PDF table could "
    "not be fully extracted here)."
)

PRICE_HISTORY = [
    (2010, 1224.5), (2011, 1571.5), (2012, 1669.0), (2013, 1411.2),
    (2014, 1266.4), (2015, 1160.1), (2016, 1250.8), (2017, 1257.6),
    (2018, 1269.2), (2019, 1392.6), (2020, 1770.0), (2021, 1799.3),
    (2022, 1800.1), (2023, 1940.5), (2024, 2386.2), (2025, 3432.0),
]
PRICE_SOURCE = (
    "LBMA Gold Price annual averages, as tabulated by Bangko Sentral ng "
    "Pilipinas (2010-2023) and metalcharts.org (2024-2025). 2025 average "
    "$3,432/oz, +43.8% y/y, trading range $2,615-$4,550."
)
PRICE_2025_RANGE = (2615.0, 4550.0)  # intraday low/high, metalcharts.org
TROY_OUNCES_PER_TONNE = 32150.7  # exact conversion constant

# Annual central-bank net gold purchases, tonnes (Metals Focus / WGC methodology,
# includes estimated unreported buying - NOT directly comparable to the IFS-only
# "reported" annual-change figures elsewhere in this file, which is why both are
# kept, cited separately, and never summed together).
CENTRAL_BANK_ANNUAL_NET_PURCHASES = [
    (2019, 668.0), (2020, 255.0), (2021, 463.1), (2022, 1136.0),
    (2023, 1037.0), (2024, 1092.4), (2025, 863.3),
]
CENTRAL_BANK_ANNUAL_SOURCE = (
    "World Gold Council, Gold Demand Trends (Q1 2021, Full Year 2021, Full "
    "Year 2023 and Full Year 2025 editions), Metals Focus / Refinitiv GFMS "
    "methodology. Central banks have been net buyers every year since 2010; "
    "the 2010-2021 annual average was 473t. This 'estimated' series (which "
    "includes modelled unreported buying) is a different methodology to the "
    "IFS-reported-only annual-change figures above and should not be summed "
    "with them."
)

DEMAND_AS_OF = "Full Year 2025 (World Gold Council Gold Demand Trends)"
DEMAND_BY_SECTOR_2025 = [
    ("Bar & coin investment", 1374.0),
    ("Jewellery", 1477.0),
    ("Central banks (net)", 863.0),
    ("Gold ETFs (net inflows)", 801.0),
    ("Technology", 335.0),
    ("OTC & statistical residual", 152.0),
]
DEMAND_TOTAL_2025 = 5002.0
DEMAND_TOTAL_2024 = 4974.0
DEMAND_VALUE_2025_USD_BN = 555.0
DEMAND_SOURCE = (
    "World Gold Council, Gold Demand Trends Full Year 2025 "
    "(https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-full-year-2025): "
    "record 5,002t / $555bn total demand; investment demand (ETFs +801t net "
    "inflows, bar & coin 1,374t) was the primary driver; jewellery volume "
    "-18% y/y even as jewellery value rose to $172bn; central banks added "
    "863t; mine production 3,671.6t (Metals Focus methodology - not directly "
    "comparable to the USGS country table above)."
)
SUPPLY_FY2025 = [("Mine production", 3671.6), ("Recycled gold", 1384.0)]
SUPPLY_SOURCE = (
    "World Gold Council Gold Demand Trends FY2025 (Metals Focus data): mine "
    "production 3,671.6t (+1% y/y), recycling +3% y/y."
)

FORECAST_NOTE = (
    "The 2026-2030 lines in the 'Forecast' sheet are a simple trend-"
    "extrapolation model (CAGR off the real 2015-2025 price/reserve series), "
    "built to demonstrate a planning workflow - NOT a price prediction. The "
    "qualitative direction (continued central-bank buying led by Poland and "
    "China, soft jewellery volumes, strong investment demand) reflects the "
    "actual FY2025/2026-YTD data above."
)

ISO3 = {
    "United States": "USA", "Germany": "DEU", "Italy": "ITA", "France": "FRA",
    "Russia": "RUS", "China": "CHN", "Switzerland": "CHE", "India": "IND",
    "Japan": "JPN", "Netherlands": "NLD", "Poland": "POL", "Turkey": "TUR",
    "Uzbekistan": "UZB", "Saudi Arabia": "SAU", "United Kingdom": "GBR",
    "Kazakhstan": "KAZ", "Portugal": "PRT", "Singapore": "SGP", "Spain": "ESP",
    "Austria": "AUT", "Australia": "AUS", "Canada": "CAN", "Ghana": "GHA",
    "Mexico": "MEX", "Peru": "PER", "Indonesia": "IDN", "South Africa": "ZAF",
    "Brazil": "BRA", "Taiwan": "TWN", "Lebanon": "LBN", "Belgium": "BEL",
    "Thailand": "THA", "Philippines": "PHL",
}

SOURCES = [
    ("Official gold reserves by country (snapshot)", RESERVES_AS_OF, RESERVES_SOURCE,
     "https://www.gold.org/goldhub/data/gold-reserves-by-country"),
    ("World & country reserve history, Q1 2000-Q2 2026", "Quarterly", WORLD_RESERVES_TREND_SOURCE,
     "https://www.gold.org/goldhub/data/gold-reserves-by-country"),
    ("Annual net change in reserves by country, 2002-2026 YTD", "Annual", CHANGES_SOURCE,
     "https://www.gold.org/goldhub/data/gold-reserves-by-country"),
    ("Central bank annual net purchases (estimated), 2019-2025", "Annual", CENTRAL_BANK_ANNUAL_SOURCE,
     "https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-full-year-2025/central-banks"),
    ("Central Bank Gold Agreement sales, 1999-2019", "Annual, by agreement year", CBGA_SOURCE,
     "https://www.gold.org/goldhub/data/gold-reserves-by-country"),
    ("Gold mine production by country", PRODUCTION_AS_OF, PRODUCTION_SOURCE,
     "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-gold.pdf"),
    ("Gold price history (annual average)", "2010-2025", PRICE_SOURCE,
     "https://metalcharts.org/gold-price-history/2025"),
    ("Global gold demand by sector & supply", DEMAND_AS_OF, DEMAND_SOURCE,
     "https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-full-year-2025"),
]
