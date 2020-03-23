import pandas as pd
import nltk
from difflib import SequenceMatcher
from rake_nltk import Rake

experience = ""
r = Rake()
r.extract_keywords_from_text(experience)
phraselist = r.get_ranked_phrases()
skillslist = []
f = open("sample-data/skills.txt", "r")
for x in f:
  skillslist.append(x.lower())

def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

experienceduration = []
setofskills = []
setofphrases = []

def experiencelevel():
    for phrase in phraselist:
        listoftimes = ["century", "centuries", "decades", "decade", "years", "year", "months", "month", "weeks", "week", "days", "day", "hours", "hour", "minutes", "minute", "seconds", "second"]
        for time in listoftimes:
            if any(str.isdigit(c) for c in phrase) and time in phrase:
                experienceduration.append(phrase)
                phraselist.remove(phrase)
                break
    return Remove(experienceduration)

def getskills():
    for phrase in phraselist:
        compsim = 0
        compskill = ""
        for skill in skillslist:
            similarity = SequenceMatcher(None, phrase, skill).ratio()
            if len(phrase) > 10:
                if similarity > 0.75:
                    if similarity > compsim:
                        compsim = similarity
                        if compskill in setofskills:
                            setofskills.remove(compskill)
                        compskill = skill.replace("\n","")
                        setofphrases.append(phrase)
                        setofskills.append(compskill)
            else:
                if similarity > 0.85:
                    if similarity > compsim:
                        compsim = similarity
                        if compskill in setofskills:
                            setofskills.remove(compskill)
                        compskill = skill.replace("\n","")
                        setofphrases.append(phrase)
                        setofskills.append(compskill)
    return Remove(setofphrases)
