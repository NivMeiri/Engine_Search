import search_engine_best
import  configuration
import  search_engine1
import  search_engine2
import  spellchecker
import  time
if __name__ == '__main__':
    config=configuration.ConfigClass()
    #search_engine=search_engine_best.SearchEngine(config)
    search_engine=search_engine2.SearchEngine(config)

    from textblob import TextBlob
    a = "cmputr"  # incorrect spelling
    #b = TextBlob(a)
    b=spellchecker.SpellChecker()
    start=time.time()
    # prints the corrected spelling
    print("corrected text: " + str(b.correction(a)))
    print(time.time()-start)



    def SpellChecker(word_list):
        after = []
        print("this is before spell checking :" + str(word_list))
        spell = spellchecker.SpellChecker()
        for value in word_list:
            after.append(spell.correction(value))
        print("this is after spell checking :" + str(after))
        return after
    print(SpellChecker(["Fauci"]))

    stemming = False
    queries = [
        "com. Anthony Fauci wrote in a 2005 paper published in Virology Journal that hydroxychloroquine was effective in treating SARS.",
        "The seasonal flu kills more people every year in the U.S. than COVID-19 has to date.",
        "Coronavirus is less dangerous than the flu",
        "The coronavirus pandemic is a cover for a plan to implant trackable microchips and that the Microsoft co-founder Bill Gates is behind it",
        "Microsoft co-founder Bill Gates sai `only the people who have all the vaccines will still be able to move freely`",
        "Bill Gates owns the patent and vaccine for coronavirus.",
        "Herd immunity has been reached.",
        "Children are “almost immune from this disease.”",
        "A study from the CDC and the WHO “proves face masks do not prevent the spread of a virus.”",
        "hydroxychloroquine, zinc, and Zithromax can cure coronavirus",
        "U.S. has “one of the lowest mortality rates in the world” from COVID-19",
        "The spread of COVID-19 will slow down as the weather warms up",
        "5G helps the spread of Covid-19",
        "Injecting or consuming bleach or disinfectant can cure coronavirus",
        "The COVID-19 pandemic was planned by the Rockefeller Foundation in “Operation Lockstep.“",
        "COVID-19 could lose its epidemic status in the United States because of declining coronavirus death rates according to CDC data.",
        "healthy people should NOT wear masks",
        "coronavirus is a bioweapon created in a lab in Wuhan",
        "The outbreak began because people ate bat soup",
        "Outbreak people ate bat",
        "coronavirus eat bat soup",
        "Wearing a mask to prevent the spread of COVID-19 is unnecessary because the disease can also be spread via farts.",
        "For younger people, seasonal flu is “in many cases” a deadlier virus than COVID-19.",
        "The coronavirus disease (COVID-19) is caused by a virus",
        "Covid-19 is not caused by bacteria",
        "The prolonged use of medical masks when properly worn, DOES NOT cause CO2 intoxication nor oxygen deficiency",
        "Masks don't cause CO2 intoxication.",
        "The COVID-19 coronavirus pandemic caused a nationwide shortage of U.S. coins in circulation during the summer of 2020.",
        "Coins shortage due to coronavirus",
        "People should NOT wear masks while exercising"]

    output_path = 'posting'
    num_docs_to_retrieve = 20
    search_engine.main( output_path, stemming, queries, num_docs_to_retrieve)
