"""voting_activity.py - Create graphs about voting_activity"""

import api
import pandas as pd
import numpy as np

from plotnine import (ggplot, ggsave, aes, geom_smooth, geom_point, geom_line,
scale_color_manual, scale_y_continuous, scale_x_continuous, labs, xlab, ylab)

def main():
    years = [2018, 2020, 2022, 2024]
    frames = []
    for year in years:
        data = api.votes_by_hour(year)["children"]
        total = data["total"]

        print(total["vote_count"], total["voter_count"], total["percentage"])

        votes = data["votes"]

        df = pd.DataFrame.from_dict(votes)
        if year != years[-1]:
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

    ggsave(plot, filename="plot.png", width=10, height=5)

if __name__ == "__main__":
    main()
