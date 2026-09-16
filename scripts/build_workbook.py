#!/usr/bin/env python3
"""Build the Global Gold Market Pulse Excel workbook (native charts) and the
dashboard/data/gold_data.js data file consumed by the HTML dashboard.

Usage:  python scripts/build_workbook.py
Output: output/Global_Gold_Market_Pulse_2026.xlsx
        dashboard/data/gold_data.js
"""
import json
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

sys.path.insert(0, os.path.dirname(__file__))
import gold_data as gd

GOLD = "B8860B"
DARK_GOLD = "8B6508"
CREAM = "FFF8E7"
INK = "2B2117"
WHITE = "FFFFFF"

HEADER_FILL = PatternFill("solid", fgColor=GOLD)
HEADER_FONT = Font(bold=True, color=WHITE, size=11)
TITLE_FONT = Font(bold=True, color=DARK_GOLD, size=16)
SUBTITLE_FONT = Font(italic=True, color="6B5B3A", size=10)
THIN = Side(style="thin", color="D9CBA0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def style_header(ws, row, n_cols):
    for c in range(1, n_cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = BORDER


def add_title(ws, text, subtitle=None):
    ws["A1"] = text
    ws["A1"].font = TITLE_FONT
    if subtitle:
        ws["A2"] = subtitle
        ws["A2"].font = SUBTITLE_FONT


def autosize(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def as_table(ws, ref, name):
    tab = Table(displayName=name, ref=ref)
    tab.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium7", showRowStripes=True, showFirstColumn=False
    )
    ws.add_table(tab)


def build():
    wb = Workbook()
    wb.remove(wb.active)

    # ---------------- Sheet 1: Overview / KPIs ----------------
    ws = wb.create_sheet("Overview")
    add_title(ws, "Global Gold Market Pulse", gd.GENERATED_NOTE)
    ws["A2"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("A2:F2")
    ws.row_dimensions[2].height = 30

    kpis = [
        ("World official gold reserves", f"{gd.WORLD_TOTAL_RESERVES_TONNES:,.1f} t", "IMF IFS, Sep 2026"),
        ("Largest holder", "United States - 8,133.5 t (22.1% of world total)", "IMF IFS, Jul 2026"),
        ("Fastest-growing large holder (3yr)", "Poland +321.5 t (2023-2025)", "IMF IFS Annual Changes"),
        ("2025 gold price (avg)", "$3,432 / oz (+43.8% y/y)", "LBMA / metalcharts.org"),
        ("Record full-year demand 2025", f"{gd.DEMAND_TOTAL_2025:,.0f} t / ${gd.DEMAND_VALUE_2025_USD_BN:,.0f}bn", "WGC Gold Demand Trends FY2025"),
        ("2025 mine production (world)", f"{gd.PRODUCTION_WORLD_TOTAL_2025:,} t", "USGS MCS 2026"),
        ("Top producer country", "China - 380 t (2025 est.)", "USGS MCS 2026"),
        ("Central-bank net buying, 2025", "863 t (3rd straight 1,000t+ era easing)", "WGC Gold Demand Trends FY2025"),
    ]
    r = 4
    ws.cell(row=r, column=1, value="Metric")
    ws.cell(row=r, column=2, value="Value")
    ws.cell(row=r, column=3, value="Source")
    style_header(ws, r, 3)
    for label, val, src in kpis:
        r += 1
        ws.cell(row=r, column=1, value=label).border = BORDER
        c = ws.cell(row=r, column=2, value=val)
        c.font = Font(bold=True, color=DARK_GOLD)
        c.border = BORDER
        ws.cell(row=r, column=3, value=src).border = BORDER
    autosize(ws, [34, 46, 34])

    # ---------------- Sheet 2: Reserves by Country ----------------
    ws = wb.create_sheet("Reserves by Country")
    add_title(ws, "Official Gold Reserves by Country", f"As of {gd.RESERVES_AS_OF}")
    ws.merge_cells("A2:F2")
    hdr = ["IFS Rank", "Country", "Tonnes", "% of FX reserves", "% of world total", "Holdings as of"]
    r = 4
    for i, h in enumerate(hdr, start=1):
        ws.cell(row=r, column=i, value=h)
    style_header(ws, r, len(hdr))
    start = r + 1
    for rank, country, tonnes, pct_fx, asof in gd.RESERVES_BY_COUNTRY:
        r += 1
        ws.cell(row=r, column=1, value=rank)
        ws.cell(row=r, column=2, value=country)
        ws.cell(row=r, column=3, value=tonnes).number_format = "#,##0.0"
        ws.cell(row=r, column=4, value=pct_fx).number_format = "0.0%"
        ws.cell(row=r, column=5, value=tonnes / gd.WORLD_TOTAL_RESERVES_TONNES).number_format = "0.00%"
        ws.cell(row=r, column=6, value=asof)
        for c in range(1, 7):
            ws.cell(row=r, column=c).border = BORDER
    end = r
    as_table(ws, f"A4:F{end}", "ReservesTable")
    autosize(ws, [10, 20, 12, 16, 15, 15])

    # institutional holders block
    r += 2
    ws.cell(row=r, column=1, value="Institutional / supranational holders (not a single country):").font = Font(bold=True)
    r += 1
    for name, tonnes, asof in gd.INSTITUTIONAL_HOLDERS:
        r += 1
        ws.cell(row=r, column=2, value=name)
        ws.cell(row=r, column=3, value=tonnes).number_format = "#,##0.0"
        ws.cell(row=r, column=6, value=asof)
    r += 2
    ws.cell(row=r, column=1, value=f"Source: {gd.RESERVES_SOURCE}").font = SUBTITLE_FONT
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
    ws.merge_cells(f"A{r}:F{r}")

    # concentration + gold-allocation leaderboard block
    r += 2
    ws.cell(row=r, column=1, value="Concentration & allocation").font = Font(bold=True, color=DARK_GOLD)
    r += 1
    top5 = sum(sorted((x[2] for x in gd.RESERVES_BY_COUNTRY), reverse=True)[:5])
    ws.cell(row=r, column=1, value="Top 5 countries' share of world reserves")
    ws.cell(row=r, column=2, value=top5 / gd.WORLD_TOTAL_RESERVES_TONNES).number_format = "0.0%"
    r += 1
    ws.cell(row=r, column=1, value="Euro Area bloc total (incl. ECB) vs United States")
    ws.cell(row=r, column=2, value=f"{gd.EURO_AREA_TOTAL_TONNES:,.0f}t vs 8,133.5t")
    r += 2
    ws.cell(row=r, column=1, value="Gold as % of FX reserves - top allocators ('de-dollarization' leaderboard)").font = Font(bold=True, color=DARK_GOLD)
    r += 1
    ws.cell(row=r, column=1, value="Country")
    ws.cell(row=r, column=2, value="% of FX reserves in gold")
    style_header(ws, r, 2)
    astart = r + 1
    for rank, country, tonnes, pct, asof in sorted(gd.RESERVES_BY_COUNTRY, key=lambda x: -x[3])[:15]:
        r += 1
        ws.cell(row=r, column=1, value=country)
        ws.cell(row=r, column=2, value=pct).number_format = "0.0%"
    aend = r
    chart3 = BarChart()
    chart3.title = "Gold as % of FX Reserves - Top 15"
    data = Reference(ws, min_col=2, min_row=astart - 1, max_row=aend)
    cats = Reference(ws, min_col=1, min_row=astart, max_row=aend)
    chart3.add_data(data, titles_from_data=True)
    chart3.set_categories(cats)
    chart3.width, chart3.height = 20, 12
    ws.add_chart(chart3, "H24")

    # Bar chart - top 15 countries by reserves
    chart = BarChart()
    chart.title = "Top 15 Countries by Official Gold Reserves (tonnes)"
    chart.y_axis.title = "Tonnes"
    chart.style = 26
    n = 15
    data = Reference(ws, min_col=3, min_row=4, max_row=4 + n)
    cats = Reference(ws, min_col=2, min_row=5, max_row=4 + n)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.width, chart.height = 24, 12
    ws.add_chart(chart, "H4")

    # ---------------- Sheet 3: Reserve History ----------------
    ws = wb.create_sheet("Reserve History")
    add_title(ws, "World Official Gold Reserves, 2000-2026", None)
    ws["A2"] = gd.WORLD_RESERVES_TREND_SOURCE
    ws["A2"].font = SUBTITLE_FONT
    ws["A2"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("A2:C2")
    r = 4
    ws.cell(row=r, column=1, value="Year")
    ws.cell(row=r, column=2, value="World reserves (tonnes)")
    style_header(ws, r, 2)
    for yr, tonnes in gd.WORLD_RESERVES_TREND:
        r += 1
        label = "Q2 2026" if yr == 2026.5 else int(yr)
        ws.cell(row=r, column=1, value=label)
        ws.cell(row=r, column=2, value=tonnes).number_format = "#,##0.0"
    end = r
    chart = LineChart()
    chart.title = "World Official Gold Reserves, 2000-2026 (CBGA selling era -> buying era)"
    chart.y_axis.title = "Tonnes"
    chart.style = 12
    data = Reference(ws, min_col=2, min_row=4, max_row=end)
    cats = Reference(ws, min_col=1, min_row=5, max_row=end)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.width, chart.height = 26, 13
    ws.add_chart(chart, "D4")
    autosize(ws, [12, 22])

    # Country history table (selected countries)
    r = end + 3
    ws.cell(row=r, column=1, value="Selected country reserve history (tonnes)").font = Font(bold=True, color=DARK_GOLD)
    r += 1
    years_all = sorted({y for series in gd.COUNTRY_HISTORY.values() for y, _ in series})
    ws.cell(row=r, column=1, value="Year")
    for j, country in enumerate(gd.COUNTRY_HISTORY.keys(), start=2):
        ws.cell(row=r, column=j, value=country)
    style_header(ws, r, 1 + len(gd.COUNTRY_HISTORY))
    hist_start = r + 1
    for yr in years_all:
        r += 1
        label = "Q2 2026" if yr == 2026.5 else int(yr)
        ws.cell(row=r, column=1, value=label)
        for j, (country, series) in enumerate(gd.COUNTRY_HISTORY.items(), start=2):
            d = dict(series)
            if yr in d:
                ws.cell(row=r, column=j, value=d[yr]).number_format = "#,##0.0"
    autosize(ws, [12] + [14] * len(gd.COUNTRY_HISTORY))

    # ---------------- Sheet 4: Net Buyers & Sellers ----------------
    ws = wb.create_sheet("Buyers & Sellers")
    add_title(ws, "Central Banks: Net Reserve Changes", None)
    ws["A2"] = gd.CHANGES_SOURCE
    ws["A2"].font = SUBTITLE_FONT
    ws.merge_cells("A2:C2")
    ws["A2"].alignment = Alignment(wrap_text=True)

    def write_block(title, rows, start_row, start_col):
        rr = start_row
        ws.cell(row=rr, column=start_col, value=title).font = Font(bold=True, color=DARK_GOLD)
        rr += 1
        ws.cell(row=rr, column=start_col, value="Country")
        ws.cell(row=rr, column=start_col + 1, value="Tonnes")
        style_header(ws, rr, 0)
        for c in range(start_col, start_col + 2):
            ws.cell(row=rr, column=c).fill = HEADER_FILL
            ws.cell(row=rr, column=c).font = HEADER_FONT
        hdr_row = rr
        for name, val in rows:
            rr += 1
            ws.cell(row=rr, column=start_col, value=name)
            ws.cell(row=rr, column=start_col + 1, value=val).number_format = "#,##0.0"
        return hdr_row, rr

    h1, e1 = write_block("Top buyers - 2025 (tonnes)", gd.TOP_BUYERS_2025, 4, 1)
    h2, e2 = write_block("Top sellers - 2025 (tonnes)", gd.TOP_SELLERS_2025, 4, 4)
    h3, e3 = write_block("Top cumulative buyers, 2023-2025 (tonnes)", gd.TOP_BUYERS_3YR_2023_2025, e1 + 3, 1)
    h4, e4 = write_block("Top buyers, 2026 YTD (tonnes)", gd.TOP_BUYERS_2026_YTD, e1 + 3, 4)
    autosize(ws, [26, 12, 4, 26, 12])

    chart = BarChart()
    chart.type = "bar"
    chart.title = "Top Cumulative Central-Bank Buyers, 2023-2025 (tonnes)"
    data = Reference(ws, min_col=2, min_row=h3, max_row=e3)
    cats = Reference(ws, min_col=1, min_row=h3 + 1, max_row=e3)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.width, chart.height = 22, 12
    ws.add_chart(chart, "G4")

    r = e4 + 2
    ws.cell(row=r, column=1, value="Poland case study - reserve build (tonnes)").font = Font(bold=True, color=DARK_GOLD)
    r += 1
    ws.cell(row=r, column=1, value="Year")
    ws.cell(row=r, column=2, value="Tonnes")
    style_header(ws, r, 2)
    pstart = r + 1
    for yr, val in gd.POLAND_BUILD:
        r += 1
        ws.cell(row=r, column=1, value=yr)
        ws.cell(row=r, column=2, value=val).number_format = "#,##0.0"
    pend = r
    r += 2
    ws.cell(row=r, column=1, value=gd.POLAND_NOTE).font = SUBTITLE_FONT
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
    ws.merge_cells(f"A{r}:F{r}")
    chart2 = LineChart()
    chart2.title = "Poland: Gold Reserve Build, 2017-2026"
    data = Reference(ws, min_col=2, min_row=pstart - 1, max_row=pend)
    cats = Reference(ws, min_col=1, min_row=pstart, max_row=pend)
    chart2.add_data(data, titles_from_data=True)
    chart2.set_categories(cats)
    chart2.width, chart2.height = 20, 10
    ws.add_chart(chart2, "G22")

    # ---------------- Sheet 4b: CBGA Era ----------------
    ws = wb.create_sheet("CBGA Era")
    add_title(ws, "The Selling Era: Central Bank Gold Agreements, 1999-2019", None)
    ws["A2"] = gd.CBGA_SOURCE
    ws["A2"].font = SUBTITLE_FONT
    ws["A2"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("A2:F2")
    ws.row_dimensions[2].height = 45
    r = 5
    ws.cell(row=r, column=1, value="Agreement year (ending)")
    ws.cell(row=r, column=2, value="Reported gross sales (t)")
    ws.cell(row=r, column=3, value="Agreed limit (t)")
    style_header(ws, r, 3)
    astart = r + 1
    for yr, tonnes, lim in gd.CBGA_ANNUAL_SALES:
        r += 1
        ws.cell(row=r, column=1, value=yr)
        ws.cell(row=r, column=2, value=tonnes).number_format = "#,##0.0"
        if lim:
            ws.cell(row=r, column=3, value=lim)
    aend = r
    chart = LineChart()
    chart.title = "CBGA Reported Gold Sales by Agreement Year (tonnes)"
    data = Reference(ws, min_col=2, min_row=5, max_row=aend)
    cats = Reference(ws, min_col=1, min_row=astart, max_row=aend)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.width, chart.height = 24, 12
    ws.add_chart(chart, "E5")

    r = aend + 3
    ws.cell(row=r, column=1, value="Top sellers under CBGA1 (Sept 1999 - Sept 2004, tonnes)").font = Font(bold=True, color=DARK_GOLD)
    r += 1
    ws.cell(row=r, column=1, value="Country")
    ws.cell(row=r, column=2, value="Tonnes sold")
    style_header(ws, r, 2)
    tstart = r + 1
    for c, t in gd.CBGA_COUNTRY_TOTALS_CBGA1:
        r += 1
        ws.cell(row=r, column=1, value=c)
        ws.cell(row=r, column=2, value=t).number_format = "#,##0.0"
    tend = r
    chart2 = BarChart()
    chart2.title = "Top Sellers Under CBGA1"
    data = Reference(ws, min_col=2, min_row=tstart - 1, max_row=tend)
    cats = Reference(ws, min_col=1, min_row=tstart, max_row=tend)
    chart2.add_data(data, titles_from_data=True)
    chart2.set_categories(cats)
    chart2.width, chart2.height = 18, 10
    ws.add_chart(chart2, "D" + str(tstart + 1))
    autosize(ws, [24, 20, 16])

    # ---------------- Sheet 5: Production ----------------
    ws = wb.create_sheet("Production")
    add_title(ws, "Gold Mine Production by Country", f"{gd.PRODUCTION_AS_OF}")
    ws.merge_cells("A2:D2")
    r = 4
    ws.cell(row=r, column=1, value="Country")
    ws.cell(row=r, column=2, value="Tonnes (2025 est.)")
    ws.cell(row=r, column=3, value="% of world production")
    style_header(ws, r, 3)
    start = r + 1
    for country, tonnes in gd.PRODUCTION_BY_COUNTRY:
        r += 1
        ws.cell(row=r, column=1, value=country)
        ws.cell(row=r, column=2, value=tonnes).number_format = "#,##0"
        ws.cell(row=r, column=3, value=tonnes / gd.PRODUCTION_WORLD_TOTAL_2025).number_format = "0.0%"
    end = r
    as_table(ws, f"A4:C{end}", "ProductionTable")
    r += 2
    ws.cell(row=r, column=1, value=f"World total 2025: {gd.PRODUCTION_WORLD_TOTAL_2025:,} t  (2024: {gd.PRODUCTION_WORLD_TOTAL_2024:,} t)").font = Font(bold=True)
    r += 1
    ws.cell(row=r, column=1, value=gd.PRODUCTION_SOURCE).font = SUBTITLE_FONT
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
    ws.merge_cells(f"A{r}:F{r}")
    autosize(ws, [18, 18, 20])

    chart = PieChart()
    chart.title = "Gold Mine Production Share by Country (2025 est.)"
    data = Reference(ws, min_col=2, min_row=4, max_row=end)
    cats = Reference(ws, min_col=1, min_row=start, max_row=end)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.width, chart.height = 20, 13
    ws.add_chart(chart, "F4")

    # ---------------- Sheet 6: Price History ----------------
    ws = wb.create_sheet("Price History")
    add_title(ws, "Gold Price - LBMA Annual Average (USD/oz)", None)
    r = 4
    ws.cell(row=r, column=1, value="Year")
    ws.cell(row=r, column=2, value="Avg price USD/oz")
    ws.cell(row=r, column=3, value="YoY change")
    style_header(ws, r, 3)
    prev = None
    for yr, price in gd.PRICE_HISTORY:
        r += 1
        ws.cell(row=r, column=1, value=yr)
        ws.cell(row=r, column=2, value=price).number_format = "$#,##0"
        if prev:
            ws.cell(row=r, column=3, value=(price - prev) / prev).number_format = "0.0%"
        prev = price
    end = r
    r += 2
    ws.cell(row=r, column=1, value=gd.PRICE_SOURCE).font = SUBTITLE_FONT
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
    ws.merge_cells(f"A{r}:F{r}")
    autosize(ws, [10, 18, 14])
    chart = LineChart()
    chart.title = "Gold Price, Annual Average 2010-2025 (USD/oz)"
    data = Reference(ws, min_col=2, min_row=4, max_row=end)
    cats = Reference(ws, min_col=1, min_row=5, max_row=end)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.width, chart.height = 22, 12
    ws.add_chart(chart, "E4")

    r = end + 3
    ws.cell(row=r, column=1, value="Central bank annual net purchases vs. gold price").font = Font(bold=True, color=DARK_GOLD)
    r += 1
    ws.cell(row=r, column=1, value="Year")
    ws.cell(row=r, column=2, value="Central bank net purchases (t)")
    ws.cell(row=r, column=3, value="Avg price (USD/oz)")
    style_header(ws, r, 3)
    cbstart = r + 1
    price_map = dict(gd.PRICE_HISTORY)
    for yr, tonnes in gd.CENTRAL_BANK_ANNUAL_NET_PURCHASES:
        r += 1
        ws.cell(row=r, column=1, value=yr)
        ws.cell(row=r, column=2, value=tonnes).number_format = "#,##0.0"
        ws.cell(row=r, column=3, value=price_map.get(yr)).number_format = "$#,##0"
    cbend = r
    r += 2
    ws.cell(row=r, column=1, value=gd.CENTRAL_BANK_ANNUAL_SOURCE).font = SUBTITLE_FONT
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
    ws.merge_cells(f"A{r}:F{r}")
    chart_cb = BarChart()
    chart_cb.title = "Central Bank Net Purchases vs Gold Price, 2019-2025"
    data = Reference(ws, min_col=2, min_row=cbstart - 1, max_row=cbend)
    cats = Reference(ws, min_col=1, min_row=cbstart, max_row=cbend)
    chart_cb.add_data(data, titles_from_data=True)
    chart_cb.set_categories(cats)
    line_cb = LineChart()
    data2 = Reference(ws, min_col=3, min_row=cbstart - 1, max_row=cbend)
    line_cb.add_data(data2, titles_from_data=True)
    line_cb.y_axis.axId = 200
    line_cb.y_axis.title = "USD/oz"
    line_cb.y_axis.crosses = "max"
    chart_cb += line_cb
    chart_cb.width, chart_cb.height = 22, 12
    ws.add_chart(chart_cb, "E" + str(cbstart - 1))

    # ---------------- Sheet 7: Demand & Supply ----------------
    ws = wb.create_sheet("Demand & Supply")
    add_title(ws, "Global Gold Demand by Sector", gd.DEMAND_AS_OF)
    r = 4
    ws.cell(row=r, column=1, value="Sector")
    ws.cell(row=r, column=2, value="Tonnes")
    ws.cell(row=r, column=3, value="% of total")
    style_header(ws, r, 3)
    start = r + 1
    for sector, tonnes in gd.DEMAND_BY_SECTOR_2025:
        r += 1
        ws.cell(row=r, column=1, value=sector)
        ws.cell(row=r, column=2, value=tonnes).number_format = "#,##0"
        ws.cell(row=r, column=3, value=tonnes / gd.DEMAND_TOTAL_2025).number_format = "0.0%"
    end = r
    r += 1
    ws.cell(row=r, column=1, value="Total").font = Font(bold=True)
    ws.cell(row=r, column=2, value=gd.DEMAND_TOTAL_2025).number_format = "#,##0"
    r += 2
    ws.cell(row=r, column=1, value="Supply side (tonnes, FY2025, Metals Focus methodology)").font = Font(bold=True, color=DARK_GOLD)
    r += 1
    for label, val in gd.SUPPLY_FY2025:
        r += 1
        ws.cell(row=r, column=1, value=label)
        ws.cell(row=r, column=2, value=val).number_format = "#,##0.0"
    r += 2
    ws.cell(row=r, column=1, value=gd.DEMAND_SOURCE).font = SUBTITLE_FONT
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
    ws.merge_cells(f"A{r}:F{r}")
    autosize(ws, [30, 12, 12])
    chart = PieChart()
    chart.title = f"Global Gold Demand by Sector - FY2025 ({gd.DEMAND_TOTAL_2025:,.0f} t)"
    data = Reference(ws, min_col=2, min_row=4, max_row=end)
    cats = Reference(ws, min_col=1, min_row=start, max_row=end)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.width, chart.height = 20, 13
    ws.add_chart(chart, "E4")

    # ---------------- Sheet 8: Forecast ----------------
    ws = wb.create_sheet("Forecast")
    add_title(ws, "Illustrative 2026-2030 Trend Model", None)
    ws["A2"] = gd.FORECAST_NOTE
    ws["A2"].font = SUBTITLE_FONT
    ws["A2"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("A2:F2")
    ws.row_dimensions[2].height = 45

    # CAGR-based extrapolation, computed transparently from real 2015-2025 data
    price_2015 = dict(gd.PRICE_HISTORY)[2015]
    price_2025 = dict(gd.PRICE_HISTORY)[2025]
    price_cagr = (price_2025 / price_2015) ** (1 / 10) - 1
    reserves_2015 = dict((int(y), v) for y, v in gd.WORLD_RESERVES_TREND if y == int(y))[2015]
    reserves_2025 = dict((int(y), v) for y, v in gd.WORLD_RESERVES_TREND if y == int(y))[2025]
    reserves_cagr = (reserves_2025 / reserves_2015) ** (1 / 10) - 1

    r = 4
    ws.cell(row=r, column=1, value="Model inputs (from real 2015-2025 data)").font = Font(bold=True, color=DARK_GOLD)
    r += 1
    ws.cell(row=r, column=1, value="Gold price 10yr CAGR (2015-2025)")
    ws.cell(row=r, column=2, value=price_cagr).number_format = "0.0%"
    r += 1
    ws.cell(row=r, column=1, value="World reserves 10yr CAGR (2015-2025)")
    ws.cell(row=r, column=2, value=reserves_cagr).number_format = "0.0%"
    r += 2
    hdr_row = r
    ws.cell(row=r, column=1, value="Year")
    ws.cell(row=r, column=2, value="Projected price (USD/oz)")
    ws.cell(row=r, column=3, value="Projected world reserves (t)")
    style_header(ws, r, 3)
    fstart = r + 1
    for i, yr in enumerate(range(2026, 2031), start=1):
        r += 1
        ws.cell(row=r, column=1, value=yr)
        ws.cell(row=r, column=2, value=price_2025 * (1 + price_cagr) ** i).number_format = "$#,##0"
        ws.cell(row=r, column=3, value=reserves_2025 * (1 + reserves_cagr) ** i).number_format = "#,##0"
    fend = r
    autosize(ws, [30, 26, 26])
    chart = LineChart()
    chart.title = "Illustrative Price Trend-Projection, 2026-2030"
    data = Reference(ws, min_col=2, min_row=hdr_row, max_row=fend)
    cats = Reference(ws, min_col=1, min_row=fstart, max_row=fend)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.width, chart.height = 20, 11
    ws.add_chart(chart, "E4")

    r = fend + 3
    ws.cell(row=r, column=1, value="Qualitative outlook drivers (from real FY2025/2026-YTD data, not modeled numerically):").font = Font(bold=True)
    drivers = [
        "Central-bank buying: Poland (+90t YTD) and China (+60t YTD) remain the largest 2026 buyers so far.",
        "Investment demand (ETFs + bar/coin) was the primary driver of 2025's record $555bn total demand.",
        "Jewellery volumes fell -18% y/y in 2025 as high prices priced out some buyers, even as jewellery value rose to $172bn.",
        "Mine supply is growing slowly (~1%/yr); recycling is the more responsive supply lever when prices rise.",
    ]
    for d in drivers:
        r += 1
        ws.cell(row=r, column=1, value="- " + d)
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
        ws.merge_cells(f"A{r}:F{r}")

    # ---------------- Sheet 9: Sources ----------------
    ws = wb.create_sheet("Sources")
    add_title(ws, "Data Sources & Methodology", None)
    r = 3
    ws.cell(row=r, column=1, value="Table / topic")
    ws.cell(row=r, column=2, value="As of")
    ws.cell(row=r, column=3, value="Citation")
    ws.cell(row=r, column=4, value="URL")
    style_header(ws, r, 4)
    for topic, asof, cite, url in gd.SOURCES:
        r += 1
        ws.cell(row=r, column=1, value=topic)
        ws.cell(row=r, column=2, value=asof)
        c = ws.cell(row=r, column=3, value=cite)
        c.alignment = Alignment(wrap_text=True)
        ws.cell(row=r, column=4, value=url)
        ws.row_dimensions[r].height = 45
    autosize(ws, [28, 20, 70, 45])
    r += 2
    ws.cell(row=r, column=1, value=(
        "The reserve, reserve-history and net-change datasets in this workbook were "
        "downloaded by the project author directly from the World Gold Council's "
        "Goldhub 'Gold Reserves by Country' page, which republishes IMF "
        "International Financial Statistics (IFS) data. Production, price and "
        "demand-by-sector figures come from USGS and the World Gold Council's "
        "Gold Demand Trends report, as cited above."
    )).font = SUBTITLE_FONT
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
    ws.merge_cells(f"A{r}:D{r}")

    # order sheets
    order = ["Overview", "Reserves by Country", "Reserve History", "Buyers & Sellers", "CBGA Era",
             "Production", "Price History", "Demand & Supply", "Forecast", "Sources"]
    wb._sheets = [wb[s] for s in order]
    for s in wb.sheetnames:
        wb[s].sheet_view.showGridLines = False

    os.makedirs("output", exist_ok=True)
    out_path = "output/Global_Gold_Market_Pulse_2026.xlsx"
    wb.save(out_path)
    print("Saved", out_path)
    return out_path


def compute_gold_allocation_leaders():
    """Rank countries by the share of their own FX reserves held in gold -
    the 'de-dollarization' leaderboard. Purely a re-sort of existing pctFx
    values already in gold_data.py."""
    rows = [{"country": c, "pctFx": pct, "tonnes": t}
            for rank, c, t, pct, asof in gd.RESERVES_BY_COUNTRY]
    rows.sort(key=lambda r: -r["pctFx"])
    return rows


def compute_concentration():
    ranked = sorted(gd.RESERVES_BY_COUNTRY, key=lambda r: -r[2])
    top5 = sum(r[2] for r in ranked[:5])
    top10 = sum(r[2] for r in ranked[:10])
    return {
        "top5Tonnes": round(top5, 1), "top5Pct": round(top5 / gd.WORLD_TOTAL_RESERVES_TONNES, 4),
        "top10Tonnes": round(top10, 1), "top10Pct": round(top10 / gd.WORLD_TOTAL_RESERVES_TONNES, 4),
    }


def compute_momentum():
    """10-year (or longest available) % change in reserves for countries with
    enough history in gd.COUNTRY_HISTORY. Purely derived from real datapoints
    already in gold_data.py - no new figures introduced."""
    out = []
    for country, series in gd.COUNTRY_HISTORY.items():
        d = dict(series)
        years = sorted(d.keys())
        latest_y, latest_v = years[-1], d[years[-1]]
        # prefer the datapoint closest to 10 years before latest, else earliest available
        target = (latest_y if latest_y != 2026.5 else 2026) - 10
        base_y = min(years[:-1], key=lambda y: abs(y - target)) if len(years) > 1 else years[0]
        base_v = d[base_y]
        pct = (latest_v - base_v) / base_v
        out.append({
            "country": country, "baseYear": ("Q2 2026" if base_y == 2026.5 else int(base_y)),
            "baseTonnes": base_v,
            "latestYear": ("Q2 2026" if latest_y == 2026.5 else int(latest_y)),
            "latestTonnes": latest_v, "pctChange": round(pct, 4),
        })
    out.sort(key=lambda r: -r["pctChange"])
    return out


def compute_regional_breakdown():
    totals = {}
    for rank, country, tonnes, pct, asof in gd.RESERVES_BY_COUNTRY:
        region = gd.REGION.get(country, "Other")
        totals[region] = totals.get(region, 0) + tonnes
    return [{"region": r, "tonnes": t} for r, t in sorted(totals.items(), key=lambda kv: -kv[1])]


def compute_reserve_values(price_usd_per_oz):
    out = []
    for rank, country, tonnes, pct, asof in gd.RESERVES_BY_COUNTRY:
        usd_bn = tonnes * gd.TROY_OUNCES_PER_TONNE * price_usd_per_oz / 1e9
        out.append({"country": country, "tonnes": tonnes, "usdBn": round(usd_bn, 1)})
    out.sort(key=lambda r: -r["usdBn"])
    return out


def build_dashboard_data():
    """Emit dashboard/data/gold_data.js - a plain window.GOLD_DATA object so
    the HTML dashboard works offline via file:// with no server/CORS needed."""
    reserves = [
        {"rank": rank, "country": country, "tonnes": tonnes, "pctFx": pct,
         "asOf": asof, "pctWorld": round(tonnes / gd.WORLD_TOTAL_RESERVES_TONNES, 5),
         "iso3": gd.ISO3.get(country), "region": gd.REGION.get(country, "Other")}
        for rank, country, tonnes, pct, asof in gd.RESERVES_BY_COUNTRY
    ]
    latest_price = dict(gd.PRICE_HISTORY)[2025]
    world_value_usd_bn = gd.WORLD_TOTAL_RESERVES_TONNES * gd.TROY_OUNCES_PER_TONNE * latest_price / 1e9
    payload = {
        "generatedNote": gd.GENERATED_NOTE,
        "worldTotalReserves": gd.WORLD_TOTAL_RESERVES_TONNES,
        "euroAreaTotal": gd.EURO_AREA_TOTAL_TONNES,
        "reservesAsOf": gd.RESERVES_AS_OF,
        "reserves": reserves,
        "regionalBreakdown": compute_regional_breakdown(),
        "goldAllocationLeaders": compute_gold_allocation_leaders(),
        "concentration": compute_concentration(),
        "euroAreaComparison": [
            {"label": "Euro Area (bloc, incl. ECB)", "tonnes": gd.EURO_AREA_TOTAL_TONNES},
            {"label": "United States", "tonnes": dict((c, t) for _, c, t, _, _ in gd.RESERVES_BY_COUNTRY)["United States"]},
            {"label": "China", "tonnes": dict((c, t) for _, c, t, _, _ in gd.RESERVES_BY_COUNTRY)["China"]},
            {"label": "Russia", "tonnes": dict((c, t) for _, c, t, _, _ in gd.RESERVES_BY_COUNTRY)["Russia"]},
        ],
        "momentum": compute_momentum(),
        "reserveValues": compute_reserve_values(latest_price),
        "worldValueUsdBn": round(world_value_usd_bn, 0),
        "valuePriceUsed": latest_price,
        "price2025Range": {"low": gd.PRICE_2025_RANGE[0], "high": gd.PRICE_2025_RANGE[1]},
        "production": [
            {"country": c, "tonnes": t, "iso3": gd.ISO3.get(c), "region": gd.REGION.get(c, "Other")}
            for c, t in gd.PRODUCTION_BY_COUNTRY
        ],
        "institutional": [
            {"name": n, "tonnes": t, "asOf": a} for n, t, a in gd.INSTITUTIONAL_HOLDERS
        ],
        "worldReservesTrend": [
            {"year": ("Q2 2026" if y == 2026.5 else int(y)), "tonnes": t}
            for y, t in gd.WORLD_RESERVES_TREND
        ],
        "countryHistory": {
            country: [{"year": ("Q2 2026" if y == 2026.5 else int(y)), "tonnes": t} for y, t in series]
            for country, series in gd.COUNTRY_HISTORY.items()
        },
        "countryHistoryNotes": gd.COUNTRY_HISTORY_NOTES,
        "cbgaAnnualSales": [{"year": y, "tonnes": t, "limit": lim} for y, t, lim in gd.CBGA_ANNUAL_SALES],
        "cbgaCountryTotals": [{"country": c, "tonnes": t} for c, t in gd.CBGA_COUNTRY_TOTALS_CBGA1],
        "cbgaSource": gd.CBGA_SOURCE,
        "topBuyers2025": [{"country": c, "tonnes": t} for c, t in gd.TOP_BUYERS_2025],
        "topSellers2025": [{"country": c, "tonnes": t} for c, t in gd.TOP_SELLERS_2025],
        "topBuyers3yr": [{"country": c, "tonnes": t} for c, t in gd.TOP_BUYERS_3YR_2023_2025],
        "topBuyers2026Ytd": [{"country": c, "tonnes": t} for c, t in gd.TOP_BUYERS_2026_YTD],
        "polandBuild": [{"year": y, "tonnes": t} for y, t in gd.POLAND_BUILD],
        "polandNote": gd.POLAND_NOTE,
        "productionWorldTotal2025": gd.PRODUCTION_WORLD_TOTAL_2025,
        "productionWorldTotal2024": gd.PRODUCTION_WORLD_TOTAL_2024,
        "priceHistory": [{"year": y, "price": p} for y, p in gd.PRICE_HISTORY],
        "centralBankAnnualNetPurchases": [{"year": y, "tonnes": t} for y, t in gd.CENTRAL_BANK_ANNUAL_NET_PURCHASES],
        "centralBankAnnualSource": gd.CENTRAL_BANK_ANNUAL_SOURCE,
        "demandBySector": [{"sector": s, "tonnes": t} for s, t in gd.DEMAND_BY_SECTOR_2025],
        "demandTotal2025": gd.DEMAND_TOTAL_2025,
        "demandTotal2024": gd.DEMAND_TOTAL_2024,
        "demandValue2025UsdBn": gd.DEMAND_VALUE_2025_USD_BN,
        "supplyFy2025": [{"label": l, "tonnes": t} for l, t in gd.SUPPLY_FY2025],
        "forecastNote": gd.FORECAST_NOTE,
        "sources": [
            {"topic": t, "asOf": a, "citation": c, "url": u} for t, a, c, u in gd.SOURCES
        ],
    }
    os.makedirs("dashboard/data", exist_ok=True)
    with open("dashboard/data/gold_data.js", "w", encoding="utf-8") as f:
        f.write("// Auto-generated by scripts/build_workbook.py - do not edit by hand.\n")
        f.write("window.GOLD_DATA = ")
        json.dump(payload, f, indent=2)
        f.write(";\n")
    print("Saved dashboard/data/gold_data.js")


if __name__ == "__main__":
    build()
    build_dashboard_data()
