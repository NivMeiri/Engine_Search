import  configuration
import  search_engine_1
import  search_engine_2
import  search_engine_3
import  search_engine_4
import  search_engine_5
import search_engine_best

if __name__ == '__main__':
    config=configuration.ConfigClass()
    config.corpusPath="data/benchmark_data_train.snappy.parquet"
    # search_engine=search_engine_best.SearchEngine(config)
    # search_engine1=search_engine_1.SearchEngine(config)
    # search_engine2=search_engine_2.SearchEngine(config)
    # search_engine3=search_engine_3.SearchEngine(config)
    # search_engine4=search_engine_4.SearchEngine(config)
    search_engine5=search_engine_5.SearchEngine(config)

    stemming = False
    queries = ["Dr. Anthony Fauci wrote in a 2005 paper published in Virology Journal that hydroxychloroquine was effective in treating SARS.	fauci paper hydroxychloroquine sars",
    "The seasonal flu kills more people every year in the U.S. than COVID-19 has to date. 	flu kills more than covid",
    "Coronavirus is less dangerous than the flu	coronavirus less dangerous flu",
    "The coronavirus pandemic is a cover for a plan to implant trackable microchips and that the Microsoft co-founder Bill Gates is behind it	gates implant microchips",
    'Microsoft co-founder Bill Gates said "only the people who have all the vaccines will still be able to move freely".	vaccines move freely',
    "Bill Gates owns the patent and vaccine for coronavirus.	Gates own covid vaccine",
    "Herd immunity has been reached.	Herd immunity reached",
    "Children are “almost immune from this disease.”	children immune to coronavirus",
    "A study from the CDC and the WHO “proves face masks do not prevent the spread of a virus.”	face masks prevent spread",
    "hydroxychloroquine, zinc, and Zithromax can cure coronavirus	zinc can cure coronavirus",
    "U.S. has “one of the lowest mortality rates in the world” from COVID-19	US lowest covid mortality",
    "The spread of COVID-19 will slow down as the weather warms up	warm weather slows covid-19 spread",
    "5G helps the spread of Covid-19	5G spreads covid-19",
    "Injecting or consuming bleach or disinfectant can cure coronavirus	disinfectant can cure coronavirus",
    'The COVID-19 pandemic was planned by the Rockefeller Foundation in "Operation Lockstep."	operation lockstep rockefeller',
    "COVID-19 could lose its epidemic status in the United States because of declining coronavirus death rates according to CDC data.	epidemic status death rate",
    "healthy people should NOT wear masks	wear masks healthy people",
    "coronavirus is a bioweapon created in a lab in Wuhan	bioweapon lab wuhan",
    "The outbreak began because people ate bat soup	people ate bat soup",
    "Outbreak people ate bat	Outbreak people ate bat",
    "coronavirus eat bat soup	coronavirus eat bat soup",
    "Wearing a mask to prevent the spread of COVID-19 is unnecessary because the disease can also be spread via farts.	covid-19 spread farts"
    "For younger people, seasonal flu is “in many cases” a deadlier virus than COVID-19	flu deadlier than covid-19",
    "The coronavirus disease (COVID-19) is caused by a virus	coronavirus caused by virus",
    "Covid-19 is not caused by bacteria	Covid-19 not caused by bacteria",
    "The prolonged use of medical masks when properly worn, DOES NOT cause CO2 intoxication nor oxygen deficiency	masks do not cause oxygen deficiency",
    "Masks don't cause CO2 intoxication.	Masks don't cause CO2 intoxication.",
    "The COVID-19 coronavirus pandemic caused a nationwide shortage of U.S. coins in circulation during the summer of 2020	covid-19 caused by coin shortage"
    "Coins shortage due to coronavirus	coin shortage coronavirus",
    "People should NOT wear masks while exercising	not wear masks while exercising",
    "Paper published in 2005 states that hydroxychloroquine is effective in treating SARS.	hydroxychloroquine treating SARS",
    "Bill Gates is responsible for Covid-19	Bill Gates is responsible for Covid-19",
    "A common cold can cause a positive COVID-19 test.	cold can cause positive COVID-19 test",
    "wearing masks has been “proven ineffective.”	wearing masks proven ineffective"
    "This virus has a cure.	virus has a cure"]

    output_path = 'posting'
    num_docs_to_retrieve = 20
    # search_engine.main( output_path, stemming, queries, 20)
    # search_engine1.main( output_path, stemming, queries, 20)
    # search_engine2.main( output_path, stemming, queries, 20)
    # #search_engine3.main( output_path, stemming, queries, 20)
    # search_engine4.main( output_path, stemming, queries, 20)
    search_engine5.main( output_path, stemming, queries, 20)

    #search_engine.load_index("index_best")
    #print(search_engine.search(queries[0]))
