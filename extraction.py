import re

import pandas as pd
from difflib import SequenceMatcher
from rake_nltk import Rake
from nltk.corpus import stopwords
from pymemcache.client import base

def list_dedupe(list_data):
    final_list = []
    for list_entry in list_data:
        if list_entry not in final_list:
            final_list.append(list_entry)
    return final_list


def experience_level():
    for phrase in phraselist:
        listoftimes = ["century", "centuries", "decades", "decade", "years", "year", "months", "month", "weeks", "week",
                       "days", "day", "hours", "hour", "minutes", "minute", "seconds", "second", "side"]
        for time in listoftimes:
            if any(str.isdigit(c) for c in phrase) and time in phrase:
                experienceduration.append(phrase)
                phraselist.remove(phrase)
                break
    return list_dedupe(experienceduration)


def get_skills():
    for phrase in phraselist:
        try:
            compsim = 0
            compskill = ""
            for skill in skillslist:
                skillkey = (skill + phrase)
                #similarity = mc_client.get(skillkey)
                #if similarity is None:
                similarity = SequenceMatcher(None, phrase, skill).ratio()
                #    mc_client.set(skillkey, similarity)
                #similarity = float(similarity)
                if len(phrase) > 10:
                    if similarity > 0.75:
                        if similarity > compsim:
                            compsim = similarity
                            if compskill in setofskills:
                                setofskills.remove(compskill)
                            setofphrases.append(phrase)
                            setofskills.append(compskill)
                else:
                    if similarity > 0.85:
                        if similarity > compsim:
                            compsim = similarity
                            if compskill in setofskills:
                                setofskills.remove(compskill)
                            setofphrases.append(phrase)
                            setofskills.append(compskill)
        except Exception as ex:
            print(ex)

    return list_dedupe(setofphrases)


stop_words = set(stopwords.words("english"))
# Creating a list of custom stopwords
new_words = ["using", "show", "result", "large", "also", "iv", "one", "two", "new", "previously", "shown", "well",
             "recently", "includes", "may", "im", "etc", "grad", "actually", "working", "worked", "ideal", "experience",
             "able", "additionally", "use", "got", "work", "states", "lots", "say", "much", "appropriate", "ask", "starting"
             "considering", "thing", "willing", "hoping", "helping", "went", "sent", "glad", "witch", "used", "done",
             "sure", "items", "description", "helping", "experienced", "ask", "learned", "years", "nerd", "things"]
stop_words = stop_words.union(new_words)

skillslist = []

dataset = pd.read_csv('sample-data/experience.csv')
experienceData = dataset.values.tolist()

complete_found_skill_list = []

f = open("sample-data/skills.txt", "r")
for x in f:
    skillslist.append(str(x).lower().strip())

mc_client = base.Client(('127.0.0.1', 11211), allow_unicode_keys=True)

with open('results.txt', 'a+') as result_file:
    for experience in experienceData:
        experienceText = experience[2]
        if type(experienceText) == float:
            continue
        r = Rake(stopwords=stop_words)

        # Strip Links
        experienceText = re.sub(r'^https?://.*[\r\n]*', '', experienceText, flags=re.MULTILINE)

        r.extract_keywords_from_text(experienceText)
        phraselist = r.get_ranked_phrases()

        experienceduration = []
        setofskills = []
        setofphrases = []

        found_skills = get_skills()
        print(found_skills)
        for result in found_skills:
            result_file.write(f"{result}\n")
        result_file.flush()
        complete_found_skill_list.append(experienceText)

print("==================================================")
print(complete_found_skill_list)
