#!/usr/bin/env python
# coding: utf-8

# In[11]:


def R_title(soup):
    ''' This function extracts and returns the recipe title as a string.
    '''
    return soup.find('h1').get_text()

def R_yields(soup):
    ''' This function extracts and returns the yield (total servings) for each recipe.
    '''
    recipe_yield = soup.find('meta', {'itemprop': 'recipeYield'})
    if recipe_yield:
        return recipe_yield.get("content").strip('Original recipe yields servings')
    else:
        return soup.find('div',{'class': 'recipe-adjust-servings__original-serving'}).get_text().strip('Original recipe yields servings')

def R_category(soup):
    ''' This function extracts the food category for the recipe. If not found, it returns
        None. 
        '''
    try:
        category = soup.find("meta", {"itemprop": "recipeCategory"})['content']
        return category
    except:
        i = soup.find('script',{"type":"application/ld+json"}).text
        category = str(i[i.find('recipeCategory'):].split(":",1)[1].split(",")[0].strip("[]"'"'))
        return category
    else:
        return 'None'

def R_ingredients(soup):
    ''' This function extracts the ingredients for each recipe.
        They are returned as a list
        '''
    ingredients = soup.findAll('li',{'class': "checkList__line"})

    if not ingredients:
        ingredients = soup.findAll('span',{'class': 'ingredients-item-name'})

    return [ingredient.get_text()
        for ingredient in ingredients if ingredient.get_text(strip=True) not in (
                'Add all ingredients to list', '','ADVERTISEMENT')]


def R_ratings(soup):
    '''This function returns the overall rating stars for the recipe
        '''
    rating = (soup.find("meta", {"property": "og:rating"}) or
        soup.find("meta", {"name": "og:rating"}))
    rating = round(float(rating['content']), 2) if rating and rating['content'] else -1.0
    return rating

def R_num_reviews(soup):
    ''' This function returns the number of reviews for the recipe
        '''
    num_reviews = soup.find("meta", {"itemprop": "reviewCount"}) #or
        #soup.find("meta", {"name": "reviewCount"}))
    num_reviews = round(float(num_reviews['content']), 2) if num_reviews and num_reviews['content'] else -1.0
    if num_reviews == -1:
        i = soup.find('script',{"type":"application/ld+json"}).text
        num_reviews= i[i.find('ratingCount'):].split(":",1)[1].split(",")[0]
    return num_reviews

def R_profile(soup):
    ''' This function extracts the recipe creator's profile url page
        '''
    profile = ''
    try:
        profile = soup.find('div', {"class":"submitter"})
        profile = profile.find('a').attrs['href']
    except:
        profile = ''
    else:
        return profile

def R_location(soup):
    ''' This function attempts to scrape the recipe creator's location from their
        profile website. Unfortunately, many profiles do not contain location information.
        '''
    m = soup.findAll('script', {'type' : 'text/javascript'})[6]
    s = str(m).split("IsPrivate")[2]
    par = s.split(',')
    city = state = country = ''
    if par[2].split(':')[0].strip('"') == 'RegionName':
        city = par[1].split(':')[1].strip('"')
        state = par[2].split(':')[1].strip('"')
        country = par[3].split(':')[1].strip('"')
    else:
        city = par[1].split(':')[1].strip('"') + ',' + par[2].strip('"')
        state = par[3].split(':')[1].strip('"')
        country = par[4].split(':')[1].strip('"')
    if city.lower() == 'null' and state.lower() == 'null' and country.lower() == 'null':
        country = par[-2].split(':')[1].strip('"')
        state = par[-3].split(':')[1].strip('"')
        city = par[-4].split(':')[1].strip('"')
    if city.lower() == 'null' and state.lower() == 'null' and country.lower() == 'null':
        city = state = country = ''
    return(city,state,country)

def create_tables(cur):
    ''' This function creates table to store the basic Recipe info in one table,
        the ingredients for the recipe in a different table and the fame year in
        another SQL table. The recipe is referenced through a foreign key in these tables.
        '''
    cur.execute('DROP TABLE IF EXISTS Recipes')
    cur.execute('DROP TABLE IF EXISTS Ingredients')
    cur.execute('DROP TABLE IF EXISTS FameYears')
    R_sql = '''
    CREATE TABLE Recipes(
    recipe_id INTEGER PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    rating REAL,
    num_reviews INTGER,
    yield INTEGER,
    category TEXT,
    city TEXT,
    state TEXT,
    country TEXT
    )
    '''
    cur.execute(R_sql)
    I_sql = '''
    CREATE TABLE Ingredients(
    ingred_id INTEGER PRIMARY KEY NOT NULL,
    ingred TEXT,
    recipe_id INTEGER,
    FOREIGN KEY(recipe_id)
        REFERENCES Recipes (recipe_id)
    )
    '''
    cur.execute(I_sql)
    F_sql = '''
    CREATE TABLE FameYears(
    fame_year INTEGER,
    recipe_id INTEGER,
    PRIMARY KEY(fame_year,recipe_id),
    FOREIGN KEY(recipe_id)
        REFERENCES Recipes (recipe_id)
    )
    '''
    cur.execute(F_sql)
    
def create_nutrient_table(cur):
    ''' This table stores nutrient data related to the specific recipe. This data is a 
        result from an API. The recipe is referenced through a foreign key.
        '''
    cur.execute('DROP TABLE IF EXISTS Nutrients')
    N_sql = '''
    CREATE TABLE Nutrients(
    nutrient_id INTEGER PRIMARY KEY NOT NULL,
    cal REAL,
    is_balanced INTEGER,
    is_highprotein INTEGER,
    is_highfiber INTEGER,
    is_lowfat INTEGER,
    is_lowcarb INTEGER,
    is_lowsodium INTEGER,
    is_vegan INTEGER,
    is_vegetarian INTEGER,
    is_lowsugar INTEGER,
    is_sugarconscious INTEGER,
    is_nooil INTEGER,
    totfat REAL,
    satfat REAL,
    carbs REAL,
    fiber REAL,
    sugar REAL,
    sugar_add REAL,
    protein REAL,
    sodium REAL,
    calcium REAL,
    magn REAL,
    potas REAL,
    iron REAL,
    zinc REAL,
    vitA REAL,
    vitC REAL,
    vitB1 REAL,
    ribf REAL,
    niacin REAL,
    vitB6 REAL,
    folate REAL,
    vitB12 REAL,
    vitD REAL,
    daycal REAL,
    dayfat REAL,
    daysatfat REAL,
    daycarbs REAL,
    dayfiber REAL,
    dayprotein REAL,
    daysodium REAL,
    daycalcium REAL,
    daymagn REAL,
    daypotas REAL,
    dayiron REAL,
    dayzinc REAL,
    dayvitA REAL,
    dayvitC REAL,
    dayvitB1 REAL,
    dayribf REAL,
    dayniacin REAL,
    dayvitB6 REAL,
    dayfolate REAL,
    dayvitB12 REAL,
    dayvitD REAL,
    recipe_id INTEGER,
    FOREIGN KEY(recipe_id)
        REFERENCES Recipes (recipe_id)
    )
    '''
    cur.execute(N_sql)
    
def create_daily_percents(cur):
    ''' This table will store recipe-specific information regarding the recipe's nutrient percents
    compared to the daily recommended totals for each nutrient. We reference the recipe through
    a foreign key in the SQL table.
    '''
    cur.execute('DROP TABLE IF EXISTS Daily_Percents')
    DP_sql = '''
    CREATE TABLE Daily_Percents(
    dailyp_id INTEGER NOT NULL,
    day_carbs REAL,
    day_fiber REAL,
    day_protein REAL,
    day_sodium REAL,
    day_calcium REAL,
    day_magn REAL,
    day_potas REAL,
    day_iron REAL,
    day_zinc REAL,
    day_vitA REAL,
    day_vitC REAL,
    day_vitB1 REAL,
    day_ribf REAL,
    day_niacin REAL,
    day_vitB6 REAL,
    day_folate REAL,
    day_vitB12 REAL,
    day_vitD REAL,
    recipe_id INTEGER,
    PRIMARY KEY(dailyp_id),
    FOREIGN KEY(recipe_id)
        REFERENCES Recipes (recipe_id)
    )
    '''    
    cur.execute(DP_sql)
        
def get_nutrients(cur, url, header):    
    ''' This function extracts recipe and related ingredient data out of SQL tables and into a dictionary.
        The API is called within the loop sending the recipe and ingredient data.
        The API results are parsed, extracted and inserted into a SQL table referecing the recipe
        through a foreign key. Boolean variables are created to track whether certain health
        or diet labels are true for each recipe.
        Do not run this too many times because the API has limit restrictions.
    '''
    import requests
    import json
    recipe_d = {}
    stopwords = ['kitchen twine', 'twine', 'toothpicks','toothpick', '1 (1 ounce) packet dry au jus mix',
             '1 (1 ounce) packet ranch dressing mix', 'olive oil cooking spray', '(<sup>&reg;</sup>)'
            ]
    n_id = 1
    cur.execute('SELECT title, yield, recipe_id from Recipes')
    titles = cur.fetchall()
    for rtitle in titles:
        totfat=satfat=carbs=fiber=sugar=sugar_add=protein=sodium=calcium=magn=potas=iron=zinc=vitA=0
        vitC=vitB1=ribf=niacin=vitB6=folate=vitB12=vitD=daycal=dayfat=daysatfat=daycarbs=0
        dayfiber=dayprotein=daysodium=daycalcium=daymagn=daypotas=dayiron=dayzinc=dayvitA=0
        dayvitC=dayvitB1=dayribf=dayniacin=dayvitB6=dayfolate=dayvitB12=dayvitD=cal=0
        serves=1
        recipe_d['title'] = rtitle[0]
        recipe_d['yield'] = rtitle[1]
        rec_id = rtitle[2]
        cur.execute('SELECT ingred from Ingredients where recipe_id = ?', (rec_id,))
        ingreds = cur.fetchall()
        ing = []
        for i in range(len(ingreds)):
            if ingreds[i][0] not in stopwords:
                one = ingreds[i][0].replace('brioche','bread')   
                one = one.replace('kosher','')  
                one = one.replace("(such as Cattlemen's(<sup>&reg;</sup>) or Jack Daniel's(<sup>&reg;</sup>))",'')
                ing.append(one)
        recipe_d['ingr'] = ing
        try:
            json_resp = requests.post(url, json = recipe_d, headers = header)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print("Error:",err)            
        result = json_resp.json()
        try:
            serves = result['yield']
        except KeyError:
            serves = 1
        try:
            cal = result['calories']/serves
        except KeyError:
            cal = 0
        try:
            dietlabels = result['dietLabels']
        except KeyError:
            dietlabels = []
        try:
            healthlabels = result['healthLabels']
        except KeyError:
            healthlabels = []
        try:     
            totfat = result['totalNutrients']['FAT']['quantity']/serves
        except KeyError:
            totfat = 0
        try:
            satfat = result['totalNutrients']['FASAT']['quantity']/serves
        except KeyError:
            satfat = 0
        try:
            carbs = result['totalNutrients']['CHOCDF']['quantity']/serves
        except KeyError:
            carbs = 0
        try:
            fiber = result['totalNutrients']['FIBTG']['quantity']/serves
        except KeyError:
            fiber = 0
        try:    
            sugar = result['totalNutrients']['SUGAR']['quantity']/serves
        except KeyError:
            sugar = 0
        try:    
            sugar_add = result['totalNutrients']['SUGAR.added']['quantity']/serves
        except KeyError:
            sugar_add = 0
        try:
            protein = result['totalNutrients']['PROCNT']['quantity']/serves
        except KeyError:
            protein =0
        try:
            sodium = result['totalNutrients']['NA']['quantity']/serves
        except KeyError:
            sodium = 0
        try:
            calcium = result['totalNutrients']['CA']['quantity']/serves
        except KeyError:
            calcium = 0
        try:
            magn = result['totalNutrients']['MG']['quantity']/serves
        except KeyError:
            magn = 0
        try:
            potas = result['totalNutrients']['K']['quantity']/serves
        except KeyError:
            potas = 0
        try:
            iron = result['totalNutrients']['FE']['quantity']/serves
        except KeyError:
            iron = 0
        try:
            zinc = result['totalNutrients']['ZN']['quantity']/serves
        except KeyError:
            zinc = 0
        try:
            vitA = result['totalNutrients']['VITA_RAE']['quantity']/serves
        except KeyError:
            vitA = 0
        try:
            vitC = result['totalNutrients']['VITC']['quantity']/serves
        except KeyError:
            vitC = 0
        try:
            vitB1 = result['totalNutrients']['THIA']['quantity']/serves
        except KeyError:
            vitB1 = 0
        try:
            ribf = result['totalNutrients']['RIBF']['quantity']/serves
        except KeyError:
            ribf = 0
        try:
            niacin = result['totalNutrients']['NIA']['quantity']/serves
        except KeyError:
            niacin = 0
        try:
            vitB6 = result['totalNutrients']['VITB6A']['quantity']/serves
        except KeyError:
            vitB6 = 0
        try:
            folate = result['totalNutrients']['FOLDFE']['quantity']/serves
        except KeyError:
            folate = 0
        try:
            vitB12 = result['totalNutrients']['VITB12']['quantity']/serves
        except KeyError:
            vitB12 = 0
        try:
            vitD = result['totalNutrients']['VITD']['quantity']/serves
        except KeyError:
            vitD = 0
        try:
            daycal = result['totalDaily']['ENERC_KCAL']['quantity']/serves
        except KeyError:
            daycal = 0
        try:
            dayfat = result['totalDaily']['FAT']['quantity']/serves
        except KeyError:
            dayfat = 0
        try:
            daysatfat = result['totalDaily']['FASAT']['quantity']/serves
        except KeyError:
            daysatfat = 0
        try:
            daycarbs = result['totalDaily']['CHOCDF']['quantity']/serves
        except KeyError:
            daycarbs = 0
        try:
            dayfiber = result['totalDaily']['FIBTG']['quantity']/serves
        except KeyError:
            dayfiber = 0
        try:
            dayprotein = result['totalDaily']['PROCNT']['quantity']/serves
        except KeyError:
            dayprotein = 0
        try:
            daysodium = result['totalDaily']['NA']['quantity']/serves
        except KeyError:
            daysodium = 0
        try:
            daycalcium = result['totalDaily']['CA']['quantity']/serves
        except KeyError:
            daycalcium = 0
        try:
            daymagn = result['totalDaily']['MG']['quantity']/serves
        except KeyError:
            daymagn = 0
        try:
            daypotas = result['totalDaily']['K']['quantity']/serves
        except KeyError:
            daypotas = 0
        try:
            dayiron = result['totalDaily']['FE']['quantity']/serves
        except KeyError:
            dayiron = 0
        try:
            dayzinc = result['totalDaily']['ZN']['quantity']/serves
        except KeyError:
            dayzinc = 0
        try:
            dayvitA = result['totalDaily']['VITA_RAE']['quantity']/serves
        except KeyError:
            dayvitA = 0
        try:
            dayvitC = result['totalDaily']['VITC']['quantity']/serves
        except KeyError:
            dayvitC = 0
        try:
            dayvitB1 = result['totalDaily']['THIA']['quantity']/serves
        except KeyError:
            dayvitB1 = 0
        try:
            dayribf = result['totalDaily']['RIBF']['quantity']/serves
        except KeyError:
            dayribf = 0
        try:
            dayniacin = result['totalDaily']['NIA']['quantity']/serves
        except KeyError:
            dayniacin = 0
        try:
            dayvitB6 = result['totalDaily']['VITB6A']['quantity']/serves
        except KeyError:
            dayvitB6 = 0
        try:
            dayfolate = result['totalDaily']['FOLDFE']['quantity']/serves
        except KeyError:
            dayfolate = 0
        try:
            dayvitB12 = result['totalDaily']['VITB12']['quantity']/serves
        except KeyError:
            dayvitB12 = 0
        try:
            dayvitD = result['totalDaily']['VITD']['quantity']/serves
        except KeyError:
            dayvitD = 0            
        is_balanced = is_highprotein = is_highfiber = is_lowfat = is_lowcarb = is_lowsodium = 0
        is_vegan = is_vegetarian = is_lowsugar = is_sugarconscious = is_fatfree = 0
        for d in dietlabels:
            if d.lower() =='balanced':
                is_balanced = 1
            elif d.lower() == 'high_protein':
                is_highprotein = 1
            elif d.lower() =='high_fiber':
                is_highfiber = 1
            elif d.lower() == 'low_fat':
                is_lowfat = 1
            elif d.lower() == 'low_carb':
                is_lowcarb = 1
            elif d.lower() == 'low_sodium':
                is_lowsodium = 1
        for h in healthlabels:
            if h.lower() =='vegan':
                is_vegan = 1
            elif h.lower() == 'vegetarian':
                is_vegetarian = 1
            elif h.lower() =='no_sugar_added':
                is_lowsugar = 1
            elif h.lower() == 'sugar_conscious':
                is_sugarconscious = 1
            elif h.lower() == 'no_oil_added':
                is_fatfree = 1
    
        n_sql = '''INSERT OR IGNORE INTO Nutrients 
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        cur.execute(n_sql,(n_id, cal,is_balanced,is_highprotein,is_highfiber, is_lowfat, is_lowcarb,
        is_lowsodium, is_vegan, is_vegetarian, is_lowsugar, is_sugarconscious, is_fatfree, totfat,
        satfat, carbs, fiber, sugar, sugar_add, protein, sodium, calcium, magn, potas, iron, zinc, vitA,
        vitC, vitB1, ribf, niacin, vitB6, folate, vitB12, vitD, daycal, dayfat, daysatfat, daycarbs,
        dayfiber, dayprotein, daysodium, daycalcium, daymagn, daypotas, dayiron, dayzinc, dayvitA,
        dayvitC, dayvitB1, dayribf, dayniacin, dayvitB6, dayfolate, dayvitB12, dayvitD, rec_id))  
        n_id += 1

def get_daily_recommendations(soupmain,cur):
    ''' This function parses the results from web scraping and extracts the nutrient data
        The data is stripped and cast to floats because they will be used in calculations later.
        This resulting data is then stored in a SQL table.
        '''
    day_protein = soupmain.find('td', {'headers':"pro-g cal-m-19-30 m-19-30"}).text.replace(',','')
    day_carbs = soupmain.find('td', {'headers':"carb-g cal-m-19-30 m-19-30"}).text.replace(',','')
    day_fiber = soupmain.find('td', {'headers':"fiber cal-m-19-30 m-19-30"}).text.replace(',','')
    day_calcium = soupmain.find('td', {'headers':"calc cal-m-19-30 m-19-30"}).text.replace(',','')
    day_iron = soupmain.find('td', {'headers':"iron cal-m-19-30 m-19-30"}).text.replace(',','')
    day_magn = soupmain.find('td', {'headers':"mag cal-m-19-30 m-19-30"}).text.replace(',','')
    day_phos = soupmain.find('td', {'headers':"phos cal-m-19-30 m-19-30"}).text.replace(',','')
    day_potas = soupmain.find('td', {'headers':"ptsm cal-m-19-30 m-19-30"}).text.replace(',','')
    day_sodium = soupmain.find('td', {'headers':"sod cal-m-19-30 m-19-30"}).text.replace(',','')
    day_zinc = soupmain.find('td', {'headers':"zinc cal-m-19-30 m-19-30"}).text.replace(',','')
    day_vitA = soupmain.find('td', {'headers':"a cal-m-19-30 m-19-30"}).text.replace(',','')
    day_vitE = soupmain.find('td', {'headers':"e cal-m-19-30 m-19-30"}).text.replace(',','')
    day_vitD = soupmain.find('td', {'headers':"d cal-m-19-30 m-19-30"}).text.replace(',','')
    day_vitC = soupmain.find('td', {'headers':"c cal-m-19-30 m-19-30"}).text.replace(',','')
    day_vitB1_thia = soupmain.find('td', {'headers':"thi cal-m-19-30 m-19-30"}).text.replace(',','')
    day_ribf = soupmain.find('td', {'headers':"ribo cal-m-19-30 m-19-30"}).text.replace(',','')
    day_niacin = soupmain.find('td', {'headers':"nia cal-m-19-30 m-19-30"}).text.replace(',','')
    day_vitB6 = soupmain.find('td', {'headers':"b6 cal-m-19-30 m-19-30"}).text.replace(',','')
    day_vitB12 = soupmain.find('td', {'headers':"b12 cal-m-19-30 m-19-30"}).text.replace(',','')
    day_folate = soupmain.find('td', {'headers':"fol cal-m-19-30 m-19-30"}).text.replace(',','')
    daily_sql = '''INSERT OR IGNORE INTO Daily_Recs(nutrient_name, value)
                    VALUES(?,?)'''
    cur.execute(daily_sql,('protein',float(day_protein)))
    cur.execute(daily_sql,('carbs',float(day_carbs)))
    cur.execute(daily_sql,('fiber',float(day_fiber)))
    cur.execute(daily_sql,('calcium',float(day_calcium)))
    cur.execute(daily_sql,('iron',float(day_iron)))
    cur.execute(daily_sql,('magn',float(day_magn)))
    cur.execute(daily_sql,('potas',float(day_potas)))
    cur.execute(daily_sql,('sodium',float(day_sodium)))
    cur.execute(daily_sql,('zinc',float(day_zinc)))
    cur.execute(daily_sql,('vitA',float(day_vitA)))
    cur.execute(daily_sql,('vitE',float(day_vitE)))
    cur.execute(daily_sql,('vitD',float(day_vitD)))
    cur.execute(daily_sql,('vitC',float(day_vitC)))
    cur.execute(daily_sql,('vitB1',float(day_vitB1_thia)))
    cur.execute(daily_sql,('ribf',float(day_ribf)))
    cur.execute(daily_sql,('niacin',float(day_niacin)))
    cur.execute(daily_sql,('vitB6',float(day_vitB6)))
    cur.execute(daily_sql,('vitB12',float(day_vitB12)))
    cur.execute(daily_sql,('folate',float(day_folate)))


def create_daily_rec_table(cur):
    ''' Creates table to store recommended daily nutrient amounts which were scraped
    '''
    cur.execute('DROP TABLE IF EXISTS Daily_Recs')
    D_sql = '''
    CREATE TABLE Daily_Recs(
    daily_id INTEGER NOT NULL,
    nutrient_name TEXT NOT NULL,
    value REAL,
    PRIMARY KEY(daily_id)
    )
    '''
    cur.execute(D_sql)

def get_stripped_ingredients(ingred_by_year_l, x, strip_words):
    '''  Removing action and measuring words from ingredients in order to get a stripped down ingredient list in order to do statistical analysis on.
         Adding another attribute to each recipe tuple with stripped down ingredient
         Returns a list of tuples that includes the ingredients, stripped ingredients and related fame year
     '''
    strip_words=['(', ')' ,',' ,'/' ,"\\" ,':','-','1','2','3','4','5','6','7','8','9','0','1/2','1/4','1/3','3/4','2/3','quarts','quart','pints','pint',
             'numbers','cups','cup','teaspoons','teaspoon', 'pounds','pound', 'softened', 'or','crushed','old-fashioned','cold','iced','hot','cubed',
            'as','needed','container','divided','to','taste','trimmed','tablespoons','tablespoon','heads','head','stocks','bite-sized','baked',
            'cloves','clove','ounces','ounce','oz.','oz','cans','can','skinless','boneless','packages','package','crumbled', 'for','garnish','serving',
                 'refrigerated','more','split','drained','torn','into','pieces','your','favorite','overripe','over-ripe','ripened','ripe','undrained'
                 'lightly','toasted','bottles','bottle','cut','inches','inch','chopped','ground','mashed','beaten', 'melted','grated','boiled','preferably'
                 'cubed','sliced','slices','slice','diced','such','as','cleaned','and','uncooked','cooked','shredded','bunches','bunch','separated','separately'
                 'havled','seeded','finely','minced','peeled','pitted','juiced','desired','rinsed','sections','section','slivered','distilled',
                 'cuts','cut','bite-size','coarsely','of','fat','quartered','cored','optional','wedges','wedge''crushed','dry','pinch','tops','tough','ends',
                 'removed','thawed','deveined','tails','tail','canned','packets','packet','freshly','fresh','more','dried','halves','halved','halve','half',
                 'large','in','at','joint','%','fluid','room','temperature','lengthwise','reserved','for','coating','pounded','thick','chilled','small',
                 'medium','sized','boiling','a','warm','warmed','degree','degrees','F','C','membranes','membrane','butterflied','packed','F/45','not','instant','and/or',
                 'discarded','thin','strips','very','using','kitchen','shears','if','undrained','skinned','preferably','cubes','plus','freezer','frozen','joints','tips',
                 'including','with','skin','loaf','crusty','soft','softened','broken','chunks','stripped','segmented','segments','segment','portions','portion','bulk'
                 'sprig','blanched','roasted','dry-roasted','salted','unsalted','enough','cover','florets','floret','thinly','unbaked','little','whole','part','mini','jar',
                 'squeezed','squeeze','decoration','decorating','hearty','the','jars',"Trader Joe's®", "Trader Joe's","Beecher's® Smoked Flagship","Cattlemen's(R Jack Daniel's(R",
                 "(R"
            ]
    strip_words.sort(reverse=True)  
    ingred_by_year = list()
    temp = []
    if x == 1:
        full = ingred_by_year_l.split()  
        result_t = [word.strip('1234567890)(/\\:,-½¼1¾⅔⅓.1½⅛') for word in full if word.lower().strip('1234567890)(/\\:,-') not in strip_words]     
        for word in result_t:
            if word in strip_words:
                temp.append(word)
        if temp:
            for w in temp:
                result_t.remove(w)
            temp = []
        stripped_t = ' '.join(result_t)
        stripped_t = stripped_t.strip()
        return(stripped_t)
    else:
        for ingred in ingred_by_year_l:
            t = list(ingred)
            full = t[0].split()
            result_t = [word.strip('1234567890)(/\\:,-½¼1¾⅔⅓.1½⅛') for word in full if word.lower().strip('1234567890)(/\\:,-') not in strip_words]     
            for word in result_t:
                if word in strip_words:
                    temp.append(word)
            if temp:
                for w in temp:
                    result_t.remove(w)
                temp = []
            stripped_t = ' '.join(result_t)
            stripped_t = stripped_t.strip()
            t.append(stripped_t)
            ingred = tuple(t)
            ingred_by_year.append(ingred)
        return ingred_by_year

def calc_and_store_daily_recipe_percents(cur):
    ''' create dictionary to get recommended daily amounts from SQL table and compare with recipe nutrients
        calculates daily percent by dividing daily recommendation for each recipe nutrient from the nutreint 
        table and stores in a SQL table
        '''
    x = cur.execute('select * from Daily_Recs')
    day_nutrs = cur.fetchall()
    daily = {}
    for day in day_nutrs:
        daily[day[1]]=day[2]
    dayP_sql = '''INSERT OR IGNORE INTO Daily_Percents (day_carbs,day_fiber,day_protein,
            day_sodium,day_calcium,day_magn,day_potas,day_iron,day_zinc,day_vitA,day_vitC,
            day_vitB1,day_ribf,day_niacin,day_vitB6,day_folate,day_vitB12,day_vitD, recipe_id )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    m = cur.execute('select carbs,fiber,protein,sodium,calcium, magn,potas,iron, zinc, vitA,vitC,vitB1,ribf,niacin,vitB6,folate,vitB12,vitD,recipe_id from Nutrients')
    recipe_nutrs = cur.fetchall()
    for r in recipe_nutrs:
        r = [int(0) if e is None else e for e in r]
        cur.execute(dayP_sql,(r[0]/daily['carbs']*100 or 0,r[1]/daily['fiber']*100 or 0,r[2]/daily['protein']*100 or 0,r[3]/daily['sodium']*100 or 0,
            r[4]/daily['calcium']*100 or 0,r[5]/daily['magn']*100 or 0,r[6]/daily['potas']*100 or 0,r[7]/daily['iron']*100 or 0,
            r[8]/daily['zinc']*100 or 0,r[9]/daily['vitA']*100 or 0,r[10]/daily['vitC']*100 or 0,r[11]/daily['vitB1']*100 or 0,
            r[12]/daily['ribf']*100 or 0,r[13]/daily['niacin']*100 or 0,r[14]/daily['vitB6']*100 or 0,r[15]/daily['folate']*100 or 0,
            r[16]/daily['vitB12']*100 or 0,r[17]/daily['vitD']*100 or 0, r[18]))
   


# In[9]:



def main(run_type, APP_KEY, APP_ID):
    '''Main program
       run program from command line with -source=remote (or =local or =noapi) as a parameter
       for final project -- will pass in App Key and APP ID as argument parameters also
       '''


    url = 'https://api.edamam.com/api/nutrition-details?app_id='+APP_ID+'&app_key='+APP_KEY
    header = {'Content-Type': 'application/json'}
    import requests
    import pandas as pd
    import sqlite3
    import json
    from bs4 import BeautifulSoup

    full_remote=local=scrape_only=0

    if run_type == 'remote':
        full_remote = 1
    elif run_type == 'local':
        local = 1
    elif run_type == 'noapi':
        scrape_only = 1
    conn = sqlite3.connect('recipes.db')
    if conn is None:
            raise DatabaseError ("Could not get connection")
    cur = conn.cursor()
    if full_remote or scrape_only:
        create_tables(cur)
        conn.commit()
        url_main = 'https://www.allrecipes.com/recipes/14452/everyday-cooking/special-collections/hall-of-fame/'
        try:
            req_main = requests.get(url_main)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print("Error:",err)
        soupmain = BeautifulSoup(req_main.content, 'html.parser')
        mainall = soupmain.findAll('a', {'class': "grid-col--subnav"})
        unique_recipes = {}
        r_id = i_id =1
        #This will loop through each annual Hall of Fame URL Set
        for fame20 in mainall:
            fame_url = fame20['href']
            fame_year = fame_url.split('/')[-2]
            if fame_year == '20th-birthday-hall-of-fame':
                fame_year = 2017
            #This will loop through each recipe url in the top 20 recipes of that Hall of Fame Set
            fame_year = int(fame_year)
            try:
                req_fame = requests.get(fame_url)
            except requests.exceptions.HTTPError as errh:
                print("Http Error:",errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:",errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:",errt)
            except requests.exceptions.RequestException as err:
                print("Error:",err)
            famesoup = BeautifulSoup(req_fame.content, 'html.parser')
            recipe_list = famesoup.findAll('article', {'class': "fixed-recipe-card"})
            for r in recipe_list:
                recipe_url = r.find('a').attrs['href']
                if recipe_url not in unique_recipes:   #some recipes are repeated in different fame years
                    unique_recipes[recipe_url] = r_id  #create dict of unique recipe urls and ids to avoid duplicate data
                    try:
                        req_recipe = requests.get(recipe_url)
                    except requests.exceptions.HTTPError as errh:
                        print("Http Error:",errh)
                    except requests.exceptions.ConnectionError as errc:
                        print("Error Connecting:",errc)
                    except requests.exceptions.Timeout as errt:
                        print("Timeout Error:",errt)
                    except requests.exceptions.RequestException as err:
                        print("Error:",err)
                    recipe_soup = BeautifulSoup(req_recipe.content, 'html.parser')
                    title = R_title(recipe_soup)
                    servings = R_yields(recipe_soup)
                    ingred = R_ingredients(recipe_soup)
                    for i in range(len(ingred)):
                        ingred[i] = ingred[i].strip('\n'"\n"", ").replace("\u2009","")
                    rating = R_ratings(recipe_soup)
                    num_reviews = R_num_reviews(recipe_soup)
                    category = R_category(recipe_soup)
                    profile_link = R_profile(recipe_soup)
                    if profile_link != '' and profile_link != None:
                        try:
                            prof_req = requests.get(profile_link)
                        except requests.exceptions.HTTPError as errh:
                            print("Http Error:",errh)
                        except requests.exceptions.ConnectionError as errc:
                            print("Error Connecting:",errc)
                        except requests.exceptions.Timeout as errt:
                            print("Timeout Error:",errt)
                        except requests.exceptions.RequestException as err:
                            print("Error:",err)
                        prof_soup = BeautifulSoup(prof_req.content, 'html.parser')
                        (city,state,country) = R_location(prof_soup)
                    else:
                        (city,state,country) = ('', '','')
                    city=(city,state,country)[0]
                    state = (city,state,country)[1]
                    country = (city,state,country)[2]
                    #Inserting data into SQL tables to store, recipes, related fame years and ingredients
                    rec_sql = '''INSERT OR IGNORE INTO Recipes(recipe_id,title, rating,num_reviews, yield, category,city,state,country)
                        VALUES(?,?,?,?,?,?,?,?,?)'''
                    cur.execute(rec_sql,(r_id,title,rating,num_reviews,servings,category,city,state,country))
                    conn.commit()
                    fame_sql = '''INSERT OR IGNORE INTO FameYears(fame_year, recipe_id)
                        VALUES(?,?)'''
                    cur.execute(fame_sql,(fame_year,r_id))
                    conn.commit()
                    ing_sql = '''INSERT OR IGNORE INTO Ingredients(ingred_id, ingred,recipe_id)
                        VALUES(?,?,?)'''
                    for i in ingred:
                        cur.execute(ing_sql,(i_id,i,r_id))
                        conn.commit()
                        i_id += 1 

                    r_id +=1   #increment after every NEW recipe
                else:
                    #reference the year for the duplicate recipe (do not create a duplicate recipe)
                    dup_r_id = unique_recipes[recipe_url]
                    fame_sql = '''INSERT OR IGNORE INTO FameYears(fame_year, recipe_id)
                        VALUES(?,?)'''
                    cur.execute(fame_sql,(fame_year,dup_r_id))
                    conn.commit()
        create_daily_rec_table(cur)   #create SQL table to store data
        conn.commit()
        u = 'https://health.gov/dietaryguidelines/2015/guidelines/appendix-7/'
        req = requests.get(u)        #scrape data for daily recommendations of nutrients
        soupmain = BeautifulSoup(req.content, 'html.parser')
        get_daily_recommendations(soupmain,cur)
        conn.commit()
        create_daily_percents(cur)   #create another SQL table to store recipe-specific daily recommendations data
        conn.commit()        
    if full_remote:      #This calls the API (which I have limits on)
        create_nutrient_table(cur)
        conn.commit()
        get_nutrients(cur, url, header)
        conn.commit()
    if scrape_only or full_remote:
        #creates dictionary to get recommended daily amounts and compare with recipe nutrients
        #calculates daily percent by dividing by daily recommendation for each recipe and store in SQL table
        calc_and_store_daily_recipe_percents(cur)
        conn.commit()
    if local or full_remote or scrape_only:
        #creates dataframes and lists of tuples from SQL relationshisp to work with data
        cur.execute('select * from sqlite_master')
        tables = cur.fetchone()
        if tables is None:
            print('Tables have not been created yet! Please run this program in remote mode in order to gather \ndata from the web and populate the database.')
        else:
            print('**Displaying some data models that will be used in final analysis:\n')
            r_df_sql = 'select * from Recipes order by city desc, state, country'
            recipe_df = pd.read_sql(r_df_sql, conn,index_col='recipe_id')
            print(f'Dataframe for recipes: \n{recipe_df}')
            i_df_sql = 'select ingred, fame_year from Ingredients natural join Recipes natural join FameYears'
            ingred_by_year_df = pd.read_sql(i_df_sql, conn)
            print(f'Dataframe for ingredients by Year: \n{ingred_by_year_df}')
            n_df_sql = 'select * from Nutrients natural join Recipes natural join FameYears group by recipe_id'
            nutrient_df = pd.read_sql(n_df_sql, conn)
            print(f'Dataframe for recipe-specific nutrient information and percent daily: \n{nutrient_df}')
            d_df_sql = 'select * from Daily_Recs'
            daily_df = pd.read_sql(d_df_sql, conn, index_col='daily_id')
            print(f'Dataframe for daily nutrient recommendations: \n{daily_df}')
            ry_df_sql = 'select fame_year, title, num_reviews, rating, category from Recipes natural join FameYears order by num_reviews desc, rating desc'
            recipe_by_year_df = pd.read_sql(ry_df_sql, conn)
            print(f'Dataframe for recipes by fame year: \n{recipe_by_year_df}')
            r_df_sql = 'select recipe_id,title,yield, rating,num_reviews,category from Recipes'
            recipe_cur = cur.execute(r_df_sql)
            recipe_l = list(recipe_cur)
            print(f'List of recipes: \n')
            for rec in recipe_l:
                  print(rec) 
            n_df_sql = 'select * from Nutrients natural join Recipes natural join FameYears group by recipe_id order by vitA desc'
            nutrient_l = list(cur.execute(n_df_sql))
            print(f'\nPartial output of 20 recipe-specific nutrient information and percent daily\n (Showing recipes high in Vitamin A as an example): \n')
            for n in nutrient_l[:20]:
                  print(f'{n}')

