import pandas
import re
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer, word_tokenize
# nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
# nltk.download('punkt')

# load the dataset
dataset = pandas.read_csv('sample-data/experience.csv')

# print("Top Occupations")
# occupationFrequency = pandas.Series(dataset['Profession'].apply(lambda x: x.lower()).value_counts()[:50])
# print(occupationFrequency)

# Creating a list of stop words and adding custom stopwords
stop_words = set(stopwords.words("english"))

# Creating a list of custom stopwords
new_words = ["using", "show", "result", "large", "also", "iv", "one", "two", "new", "previously", "shown", "well", "recently", "includes", "may", "im", "etc", "grad", "actually", "working", "worked"]
stop_words = stop_words.union(new_words)

corpus = []
for respondent in dataset.values:

    try:
        if respondent[2]:
            data = str(respondent[2]).lower()

            # Strip Links
            data = re.sub(r'^https?://.*[\r\n]*', '', data, flags=re.MULTILINE)

            # Strip out all characters except letters and spaces
            data = re.sub('[^a-z\s]+', '', data)

            data = word_tokenize(data)

            # Convert to lowercase
            # text = text.lower()

            # remove tags
            # text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)

            # remove special characters and digits
            # text = re.sub("(\\d|\\W)+", " ", text)

            # Stemming
            ps = PorterStemmer()
            # Lemmatisation
            lem = WordNetLemmatizer()

            text = [lem.lemmatize(word) for word in data if word not in stop_words]
            text = " ".join(text)
            corpus.append(text)
    except Exception as ex:
        print(ex)

# Output result
print(corpus)
