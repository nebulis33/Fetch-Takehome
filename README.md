# Intro:
All of the files are read into duckDB databases. To create the databases and get the results from the
queries simply run these commands from the root of`fetch_takehome` after cloning the repo:

```
docker build -t fetch_takehome .
docker run fetch_takehome
```

# Data Quality Issues:
The `receipts` file had the most data quality issues. Mostly things like missing data, or data that was incomplete.
I went into more detail in the stakeholder letter, but it was difficult to accurately match the information
about purchases to the `brands` data because of this. I also noticed there were a lot of brands that had the
same number of transactions (likey because of this) so that made it difficult to accurately pick a definitive top 5.
The other data was fine, though there were some repeated rows but that was easy to deal with. I also had to
give up on setting a `foreign key` constraint in the tables, because it turned out not everything matched. For example,
user `5f9c74f7c88c1415cbddb839` existed in the `receipts` file but not the `users` file.

# Design Decision Notes:
* I made the decision to have all the tables built and run, as well as all the queries run on calling the file
(instead of having them able to run individualy) because it is just clener and easier on the end user,
including future me.
* I used transactions when inserting data just to keep everything clean and together, even though it's
probably a little overkill, it's better to be safe than sorry.

