
    What questions do you have about the data?
    How did you discover the data quality issues?
    What do you need to know to resolve the data quality issues?
    What other information would you need to help you optimize the data assets you're trying to create?
    What performance and scaling concerns do you anticipate in production and how do you plan to address them?

Hello Stakeholder,

I have attached the answers to your previous questions to this email. There were a few issues I ran into:
 - The data for receipts is missing the status of "accepted". There was a status of "Finished" which seemed to
 correspond with accepted receipts, so I used that when querying the data.
 - The more granular transaction data about each reciept (basically the breakdown of what items were on
 the receipt and their cost, etc) was incomplete. Some items were missing barcodes for example. I think this
 was perhaps related to how the data was previously stored. I ended up basically ignoring products that
 didn't have an ID of the brand they are from because of this.
 - If we want to scale the analysis of this data up, we should probably meet to discuss the quality of the
 data as well as the meaning of different items within the data. This is just because if we scale things up
 and use more data, inevitably more people will come to ask questions of it and we want it to be as accurate
 as possible. This initial exploration can have some leeway because I am able to directly communicate with
 you about it, but that obviously won't be the case with more data and more questions.
 - Performance wise, I think this can scale pretty well for a while, but if we are continuously adding data
 I think I will need to set something up in our cloud service provider instead of running and storing it all
 on my own laptop. This shouldn't be too much of a lift but it will be a new expense.

Let me know if you have any questions or concerns.

Thanks,
Colton