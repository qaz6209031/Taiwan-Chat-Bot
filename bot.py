import io
import random
import string # to process standard python strings
import warnings
import nltk
from nltk.stem import WordNetLemmatizer
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings('ignore')

nltk.download('popular', quiet=True) #downloads packages

f=open('taiwan_data.txt','r',errors = 'ignore')
raw=f.read()
raw = raw.lower() #converts to lowercase to reduce repetition of words like The and the or When and when

sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
   return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
   return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("你好", "嗨", "hello", "hi", "sup","hey")
GREETING_RESPONSES = ["你好啊", "哈囉", "hello", "hi", "sup","yo"]

def greeting(sentence):
   for word in sentence.split():
      if word.lower() in GREETING_INPUTS:
         return random.choice(GREETING_RESPONSES)

def response(user_response):
   robot_response=''
   sent_tokens.append(user_response)
   TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
   tfidf = TfidfVec.fit_transform(sent_tokens)
   vals = cosine_similarity(tfidf[-1], tfidf)
   idx=vals.argsort()[0][-2]
   flat = vals.flatten()
   flat.sort()
   req_tfidf = flat[-2]
   if(req_tfidf==0):
      robot_response=robot_response+"I think I need to read more about that..."
      return robot_response
   else:
      robot_response = robot_response+sent_tokens[idx]
      return robot_response

flag=True
print("TaiwanBot: 你好 I am Taiwanbot. I am an expert of Taiwan, you can ask me anything. Go ahead! Enter bye to leave the program")

while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("TaiwanBot: Anytime")
        else:
            if(greeting(user_response)!=None):
                print("TaiwanBot: "+greeting(user_response))
            else:
                print("TaiwanBot: ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("TaiwanBot: 後會有期")
