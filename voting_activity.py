"""voting_activity.py - Create graphs about voting_activity"""

import api

import pandas as pd
import numpy as np
import datetime

from plotnine import (ggplot, ggsave, aes, geom_smooth, geom_point, geom_line,
scale_color_manual, scale_y_continuous, scale_x_continuous, labs, xlab, ylab)

def get_data(years):
    datasets = {}
    for year in years:
        data = api.votes_by_hour(year)
        datasets[year] = (data)

    return datasets

def get_year_data(datasets):
    year_data = {}
    for year in datasets:
        total = datasets[year]["children"]["total"]
        year_data[year] = {
                "vote_count": total["vote_count"],
                "voter_count": total["voter_count"],
                "percentage": total["percentage"],
        }

    return year_data


def create_dataframes(datasets):
    frames = []
    for year in datasets:
        votes = datasets[year]["children"]["votes"]

        df = pd.DataFrame.from_dict(votes)
        if year != 2024:
            max_hours = 60
            hours = len(df)
            step = max_hours / hours
            df.insert(1, "hour", np.arange(0, max_hours, step), True)
        else:
            df.insert(1, "hour", range(0, len(df)), True)

        df.insert(2, "year", [str(year)] * len(df), True)
        frames.append(df)

    df = pd.concat(frames)
    df = df.sort_values(by="year", ascending=False)

    return df

def create_plot(df, filename):
    colors = ["#ea76cb33", "#e6455366", "#df8e1d99", "#209fb5ff"]

    last = df[df["year"] == "2024"]
    others = df[df["year"] != "2024"]

    plot = (ggplot()
            + geom_point(data=others, mapping=aes(x="hour",
                y="cumulative_count", color="year"))
            + geom_line(data=others, mapping=aes(x="hour",
                y="cumulative_count", color="year"))

            + geom_point(data=last, mapping=aes(x="hour",
                y="cumulative_count", color="year"))
            + geom_line(data=last, mapping=aes(x="hour",
                y="cumulative_count", color="year"))

            + scale_x_continuous(breaks = range(0,60,5))

            + scale_color_manual(values=colors)

            + labs(
                title = "Äänestysaktiivisuus HYYn edustajistovaaleissa",
                subtitle = "Äänien jakautuminen äänestystunneille vuosina 2018-2024",
                caption = "lähde: http://vaalitulos.hyy.fi",
                color = "Vuosi"
                )
            + xlab("Äänestystunti")
            + ylab("Äänimäärä")
            )

    ggsave(plot, filename=filename, width=10, height=5)

def create_html(year_data):
    statistics = ""
    for year in year_data:
        voter_count = year_data[year]["voter_count"]
        vote_count = year_data[year]["vote_count"]
        percentage = year_data[year]["percentage"]
        stat = f"""
<div class="year" id="{year}">
    <h3>{year}</h3>
    <ul>
    <li>Äänioikeutettuja: {voter_count}</li>
    <li>Ääniä annettu: {vote_count}</li>
    <li>Äänestysprosentti: {percentage}%</li>
    </ul>
</div>\n
"""

        statistics += stat

    with open("template.html", "r") as f:
        template = f.read()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html = template.format(statistics=statistics, updated=now)
        
        with open("voting_activity.html", "w") as g:
            g.write(html)


def main():
    years = [2018, 2020, 2022, 2024]
    datasets = get_data(years)
    df = create_dataframes(datasets)
    create_plot(df, "voting_activity.png")

    year_data = get_year_data(datasets)
    create_html(year_data)

if __name__ == "__main__":
    main()
