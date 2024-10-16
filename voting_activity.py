"""voting_activity.py - Create graphs about voting_activity"""

import api
import pandas as pd

from plotnine import ggplot, ggsave, aes, geom_smooth, geom_point, geom_line

def main():
    years = [2018, 2020, 2022, 2024]
    frames = []
    for year in years:
        data = api.votes_by_hour(year)["children"]
        votes = data["votes"]

        df = pd.DataFrame.from_dict(votes)
        df.insert(1, "hour", range(0, len(df)), True)
        df.insert(2, "year", [str(year)] * len(df), True)
        frames.append(df)

    df = pd.concat(frames)

    print(df.columns)

    plot = (ggplot(
                data = df,
                mapping = aes(x="hour", y="cumulative_count", colour="year")
            )
            + geom_point()
            # + geom_smooth()
            + geom_line()
            )

    ggsave(plot, filename="plot.png")

if __name__ == "__main__":
    main()
