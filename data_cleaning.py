#imports libraries
import pandas as pd

#imports the csv files that were previously scraped
batting_stats = pd.read_csv("ilt20_batting_stats_with_nationality_2025.csv")
bowling_stats = pd.read_csv("ilt20_bowling_stats_with_nationality_2025.csv")

#does an outside join on the two data frames, as there may be players who did not bat or did not bowl
merged_stats = pd.merge(batting_stats, bowling_stats, on="Player", how="outer", suffixes=("_batting", "_bowling"))

#replaces hyphens with 0s as the sourceused hyphens to represent 0s
merged_stats.replace("-", 0, inplace=True) 

#extracts the team name from the player name to another column and removes it 
merged_stats["Team"] = merged_stats["Player"].str.extract(r"\((.*?)\)")
merged_stats["Player"] = merged_stats["Player"].str.replace(r"\(.*?\)", "", regex=True)

#merges the nationalities into one column
merged_stats["Nationality"] = merged_stats["Nationality_batting"].combine_first(merged_stats["Nationality_bowling"])

#removes the old nationality columns
merged_stats = merged_stats.drop(columns=["Nationality_batting", "Nationality_bowling"])

#does the same with the matches played
merged_stats["Matches"] = merged_stats["Mat_batting"].combine_first(merged_stats["Mat_bowling"])
merged_stats = merged_stats.drop(columns=["Mat_batting", "Mat_bowling"])

#removes the span columns as they just say the season for whcih the data is taken from, as well as the player URL as thats not needed
merged_stats = merged_stats.drop(columns=["Span_batting", "Span_bowling", "Player Profile URL_batting", "Player Profile URL_bowling"])
merged_stats.rename(columns={"Mat_batting": "Matches"}, inplace=True)

#saves the merged data frame to a new csv file
merged_stats.to_csv("ilt20_final_statistics_2025.csv", index=False)