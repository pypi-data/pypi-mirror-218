***Experimental code/package to fetch data from mcx. Do not use this code/package to programmatically get data from mcx exchange. This code/package is given here only for educational purpose.  The coder/ distrinutor is not liable for any type of damage caused by or arising from the use of this code.***

Functions:

Below Functions will return data in pandas dataframe.. Any of the functions accepts date/expiry as %d-%m-%Y / 
datetime.datetime / datetime.date

mcx_bhavcopy(bhavdate) -> Returns bhacopy for the given bhavdate.
mcx_marketwatch() -> Returns marketwatch.
mcx_circulars(from_date, to_date) -> By default returns circulars within 4 days.
mcx_topgainers() -> Returns top gainers.
mcx_toploosers() -> Returns top loosers.
mcx_mostactiveoptions() -> Returns most active options.
mcx_mostactivecontracts() -> Returns most active contracts.
mcx_optionchain(commodity, expiry) -> Returns option chain of the given commodity of the given expiry.
mcx_pcr(expirywise) -> Returns commoditywise pcr if expirywise is False. If not, returns pcr expiry wise.
mcx_expiry(commodity, expirytype) -> By default returns current expiry date of Crudeoil.
mcx_heatmap() -> Returns heatmap dataframe.
