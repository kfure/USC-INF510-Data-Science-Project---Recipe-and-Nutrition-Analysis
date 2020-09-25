# USC-INF510-Project---Recipe-and-Nutrition-Analysis
Recipe and Nutrition Trends and Analysis using Python, Web-scraping of AllRecipes, Edamam API, USDA Recommendations, and SQLite Databases

USC INF 510 Fall 2019 Project by Kirsten Fure

## 1. Go to /src/fure_kirsten.ipynb (within GitHub) to see MAIN PROJECT and code.


2. How to run project code:
To run this project using the SQLite databases, make sure the necessary python packages are installed, and then simply clone the repo at https://github.com/kfure/USC-INF510-Project---Recipe-and-Nutrition-Analysis and execute this notebook.

The database "recipes.db" is in the /data folder within the github repository.
There is an environment.yml file in the github repo that has the associated environment for this project.
This project requires the following packages:

wordcloud, numpy, pillow, matplotlib, plotnine, pygal, cairo, beautiful soup, requests

If you would like to see interactive PyGal graphs in a browser, you can uncomment line_chart.render_in_browser() and execute.

If you would like to run the webscrapers and API for this project, you will need an Edamam API Key and Edamam API ID to insert into the parameters. When you have that, go to the very end of this program, create a new cell, enter main('remote',<your API key/ID parameters>) and execute. This will execute all the web-scraping and API code and create and populate the database "Recipes.db" in your environment.


3. Things that could be improved:
The colorful plot showing the top nutrient-dense recipes is squishing recipe titles together. I did work to make sure the titles were not overlapping, but they are very tight. If I had more time, I would figure out a way to display this data so the recipe titles are even easier to read.
Many recipe creators did not have a home location on their profile. I was hoping to do analaysis looking for possible correlations among location and recipes, ingredients or health trends. But, the location data was not consistent enough to include.


4. Other problems/notes:
I had some trouble installing PyGal in anaconda. I did it through pip and had to install cairo and that seemed to solve it.

I tried to write the code for easy readability so it is not in condensed python style, but I could re-write this in a condensed more pythonic style and it would be much shorter!


5. Project Overview:
I am interested in cooking and nutrition, so I decided to analyize popular recipes, their overall trends, and any related nutritional analysis. I chose to use AllRecipes.com, which is a community recipe collection and sharing website (vs. a collection of recipes created by professional chefs). I wanted to focus on the community and their trends. For the last 20 years, AllRecipes has produced an annual "Hall of Fame" Top 20 recipes list for that year. I webscraped those top recipes for the entire collection, which included every year from 1997 to 2017. I gathered relevant information for each recipe such as recipe title, ingredients, category, number of reviews, overall rating, the recipe creator's location (city/state/country), etc...

Here is the base website:

https://www.allrecipes.com/recipes/14452/everyday-cooking/special-collections/hall-of-fame/

I collected and formatted this information, so I could send it to the Edamam API, which sent back comprehensive nutrient information based upon each recipe's ingredients that I sent. I calculated the per serving nutrient values based upon each recipe's number of servings (yield).

I then webscraped the USDA's recommended daily percentage of nutrients website and used that information to calculate each recipe's per serving nutrient percentages, linking up with the nutrient name.

I put all the information into related SQLite databases joining them based upon their primary/foreign key commanilites, which is either a recipe id, fame year, ingredient id, or nutrient id.

I did analysis on the recipes looking for trends in their ingredients, popularity and healthiness as a whole and over the span of the last 20 year, using Pandas dataframes, python lists, tuples and dictionaries.


6. Discoveries and Conclusions:
I found that popular ingredients did change over the years. When I anlayzed single ingredient words, I found that words associated with baking goods, such as sugar, flour and butter were more popular in the 90s than now. The current popular ingredient words are more savory like chicken, cheese and sauce.

Interestingly, when I looked at statistics of ingredients phrases, not just their single words (for example "white sugar" instead of "white" and "sugar separately, overall throughout all the years, many baking ingredients still come out on top. All-purpose flour, butter, eggs, garlic, salt, vanilla extract and white sugar top the list, but their popularities change through the 20 year period.

When I began looking at nutrition and trends over time, I noticed a correlation in the popularity of carb content and sugar content in recipes. When carb contents rose, the sugar content also seems to rise over time. They both peaked around 2002 and hit a low around 2014. For fat content, both saturated fat and total fat fluctated without a decisive trend, except that the 90s really were the low-fat craze!!

I decided that analyzing each nutrient, vitamin and mineral separately would be too detailed for this particular project, so I developed a "nutrient score" algorithm which I applied to each recipe. The algorithm compiles all nutrient information per recipe and gives points for each nutrient based on what percent it delivers compared to the USDA's recommended daily amount. Note that the nutrient score did not include fat, calories, carb or sugar content. It is related to the vitamin and mineral content, and the higher the nutrient score, the more nutritious the reipce is. 2012 proved to be the stand-out year with the most nutritious recipes, and the 90s had the lowest nutritious recipes.

I am curious which nutrients our community has the hardest time getting through our favorite recipes. This could give us insight on which vitamins we need to focus on adding to our diet. I looked at the averages of all vitamins and minerals per year and then compared them. Vitamin D was the lowest for every year except 3 of the years! Excluding Vitamin D, other culprits that our favorite recipes run the most low on were: fiber for 8 years, potassium for 7 years, vitamin C for 4 years and calcium for 2 years.

Because different people have different diet goals, I created a chart to show the top 30 nutritious recipes, based upon their nutrient score. Then, the chart shows for each of those recipes, their saturated fat content, sugar content and number of reviews. People can look at this chart and choose popular recipes that are nutritious and make choices upon fat content and sugar content.

Finally, I produced a list of 25 nutritious recipes (according to my "nutrient score") that are rated highly, popular, and low in saturated fat for those interested in heart health and general health, but want tasty food.

Sweet Potato and Black Bean Chili
Cha Cha's White Chicken Chili
Chef John's Caramel Chicken
Slow Cooker Beef Pot Roast
Baked Pork Chops I
Baked Teriyaki Chicken
Blackened Salmon Tacos with Chunky Mango Avoca...
Breaded Pork Tenderloin
Slow Cooker Beef Stew I
Perfect Turkey
Homestyle Turkey, the Michigander Way
Stuffed Green Peppers I
Awesome Slow Cooker Pot Roast
Healthy Mexican Chicken Bake
One Skillet Mexican Quinoa
Just Like Wendy's® Chili
Strawberry Spinach Salad I
Heather's Grilled Salmon
Barbecued Beef
Zesty Slow Cooker Chicken Barbecue
Chef John's Stuffed Peppers
Mozzarella-Stuffed Pesto Turkey Meatballs
Awesome Sausage, Apple and Cranberry Stuffing
Chicken Cacciatore in a Slow Cooker


7. Difficulties I encountered:
I originally planned to use the USDA's nutrition API database to get nutrient information, but for every ingredient they offer a multitude of options to match on. (For example, squash could be many different varieties and it could be raw, cooked, roasted, sweetened, canned, mashed, etc... which all have different nutrient information.) This complexity was going require alot of programming decision making in order to decide which USDA ingredient was the best match for the recipe's ingredient. Then, I would also have to calculate the nutrient amount in each recipe using the amount of the ingredient the recipe calls for vs the amount the USDA is in. Many conversions for grams, cups, ounces, etc.. would be involved. Ultimately, I decided to look into other APIs that are built off of the USDA engine and found several options. I chose Edamam because of its comprehensive list of nutrient information.

The edamam API was good, but I did find times where the information was not complete. For example, I found that the sugar_added was not accurate. I compared the values with recipe ingredients, and I did not trust the results. I saw several times when the sugar_added was zero and the recipe clearly had sugar as an ingredient. So, I switched my program to rely on their total sugar content instead, which proved to be consistent and correct. There were a few other cases like this, but I tested results and data and made sure what I used was accurate.

Also, certain words included in ingredients would throw Edamam off and it would not return a match. So, I created a list of stopwords and stripped these from ingredients.

Edamam offers some diet and health categories, such as balanced, low-fat, low-sugar, etc... which I was hoping to utilize, but I found many of them to be inconsistent, so I relied on my individual nutrient data rather than the labels they offered.


8. Skills I learned:
I was not familiar with the concept of APIs and how to interact with them. But, through this class and this project, I am much more comfortable with the concept and now realize how many there are! These can be a big help in creating applications where you need an on-going specific data source. I also did not know how to do web-scraping and learned how fragile the environment can be as companies can change their websites at any moment without any documentation or warning. I wish I had more experience going into this class with github and the command line.


9. Ideas for project expansions / next steps:
I would include tons of recipes with recipe-creator location data so I can analyze trends in ingredients, recipes and healthiness across different regions, countries and/or states. There are similar websites popular in Europe and other countries, so it would be fun to combine the data with AllRecipes and analyze. Do you think Germans are eating more sausage than us? Or, do the French favor cheese in their recipes more?
I would also like to download data from FoodNetwork and other popular chef-specific recipe sites and do similar analysis, adding chef-specific trends that emerge.
Including analysis specific to each nutrient and looking at each vitamin and mineral separately would be interesting. I would also develop algorithms to "score" recipes for people concerned with different issues (in combination with the nutrient-score as getting maxiumum vitamins and minerals is my first goal): heart-health, diabetes-prevention, weight-loss, etc.
I would love to develop algorithms to offer recipe alterations to make recipes more healthy under certain conditions, automatically offering suggestions and ways to make recipes gluten-free, vegan, vegetarian, sugar-conscious, higher in Vitamin C, higher in Calcium, higher in Vitamin A, etc...
