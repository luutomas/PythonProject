# PythonProject
Python Project for IES FSV UK class

# Proposition - bezrealitky.cz
Scrape the properties of flat in the Czech Republic (can be focused on Prague only) via bezrealitky.cz. Create two seperate databases, one is flat for sale and the second one is the flat for renting. Thus obtaining two cross-section database.
The idea is to assign to each flat for sale a renting value, which it can generate. This help to determine whether the flat has a good investment value.

# Ideas for analytical part - Proposition - bezrealitky.cz
 - regression - e.g. quantile regression of price determinants [1]
 - spatial clustering - find geo patterns in Prague's rent and sale real estate markets
 - Buying house as an investment generating rent? - assign a renting value to a property for sale


## References
[1] Zietz et al.(2008), Determinants of House Prices: A Quantile Regression Approach. J Real Estate Finance Econ 37

# Jan's comments
 - selected Nove Mesto as test dataset
 - adjusted scraping of coordinates for OpenStreetMaps
 - easy histograms and scatters

# Tasks
 - create separate notebooks for downloader and EDA
 - regression - OLS, quantile, simple equation (possible use of large dummy matrix) [1]
 - how to parse locations?
 - 
