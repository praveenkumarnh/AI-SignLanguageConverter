from nltk.parse.stanford import StanfordParser
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.tokenize.stanford import StanfordTokenizer
from nltk.tree import *
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
import nltk

para=raw_input("Enter string")
sent=nltk.sent_tokenize(para)
final =[] #final sring to store last output

for s in sent:
    tokens=nltk.word_tokenize(s)
    def get_wordnet_pos(treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    lemmatizer = WordNetLemmatizer()
    tagged = nltk.pos_tag(tokens)
    lemmatized_tokens=[]
    for word, tag in tagged:
        wntag = get_wordnet_pos(tag)
        if wntag is None:# not supply tag in case of None
            lemma = lemmatizer.lemmatize(word)
            lemmatized_tokens.append(lemma)
        else:
            lemma = lemmatizer.lemmatize(word, pos=wntag)
            lemmatized_tokens.append(lemma)

    print(lemmatized_tokens)

    parser=StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    #o=parser.parse(s.split())
    #tree1=[tree for tree in parser.parse(s.split())]
    tree1=[tree for tree in parser.parse(lemmatized_tokens)]
    parsetree=tree1[0]
    dict={}
    #output = '(ROOT (S (PP (IN As) (NP (DT an) (NN accountant))) (NP (PRP I)) (VP (VBP want) (S (VP (TO to) (VP (VB make) (NP (DT a) (NN payment))))))))'
    #parsetree=Tree.fromstring(output)
    #parsetree=parser.raw_parse(s)
    print parsetree

    print "***********subtrees**********"
     
    ptree= ParentedTree.convert(parsetree)
    for sub in ptree.subtrees():
        #print sub
        dict[sub.treeposition()]=0
       # print sub.label()

    print "----------------------------------------------"

    tree2=Tree('ROOT',[])
    i=0
    for sub in ptree.subtrees():
        if(sub.label()=="NP" and dict[sub.treeposition()]==0 and dict[sub.parent().treeposition()]==0):
            dict[sub.treeposition()]=1
            tree2.insert(i,sub)
            i=i+1

            
        if(sub.label()=="VP" or sub.label()=="PRP"):
            
            for sub2 in sub.subtrees():
                if((sub2.label()=="NP" or sub2.label()=='PRP')and dict[sub2.treeposition()]==0 and dict[sub2.parent().treeposition()]==0):
                    dict[sub2.treeposition()]=1
                    tree2.insert(i,sub2)
                    i=i+1

    for sub in ptree.subtrees():
        for sub2 in sub.subtrees():
              # print sub2
               #print len(sub2.leaves())
               #print dict[sub2.treeposition()]
               if(len(sub2.leaves())==1 and dict[sub2.treeposition()]==0 and dict[sub2.parent().treeposition()]==0):
                   dict[sub2.treeposition()]=1
                #   print sub2
                 #  print sub2.treeposition()
                  # print dict[sub2.treeposition()]
                   tree2.insert(i,sub2)
                   i=i+1

                  
    print tree2

    print tree2.leaves()

    parsed_sent=tree2.leaves()
    print parsed_sent
    final.append(parsed_sent)
    final.append("EOL")
    #words=parsed_sent

print final
