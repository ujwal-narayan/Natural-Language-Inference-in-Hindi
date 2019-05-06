# Natural-Language-Inference-in-Hindi
Natural Language Inference in Hindi using Automated Theorem Proving 

## Introduction

The scope of the project invloves in finding wether given two sentence pairs s1 and s2, does s1 imply s2 or the other way around. Consider s1 to be "Twenty men are playing football" and s2 to be "Some men are playing a sport". Here we say s2 can be inferred from s1. 

## Existing Methods

There exists no implementation specializing in Hindi to do this task. The closest is the [Cross Lingual XNLI](https://www.aclweb.org/anthology/D18-1269) with an accuracy of 63%. 

## Pipeline 

The architecture for this processs is as follows:
1. The data is first cleaned up, and all function words are removed. Punctuation like the "|" are also removed.
2. The text is first parsed using a [dependency parser](https://bitbucket.org/iscnlp/parser/src/master/)
3. The words in each sentence are looked up using the [WordNet](http://www.cfilt.iitb.ac.in/wordnet/webhwn/)
4. Due to the fact that case markers are inflected morphologically in Hindi, a Hindi stemmer was developed and used to rip off the case markers on Nouns and Verbs so as to get relations from the WordNet look up.
5. A sentence pair is classified as Inference only if all the karaka relations are the same for each word or the corrseponding substituted word(different words in different sentences, but having the same sense) 

## Data 

[Facebook XNLI Corpus](https://research.fb.com/downloads/cross-lingual-nli-corpus-xnli/) was the data source for the Hindi data. THe Test set consisting of 5k sentence pairs was used to evaluate the architecture.


## Accuracy 

This system boasts of an accuracy of 66.7% on general tasks. A susbset of this task with just invloving Entailment and Contradiction(i.e without any neutral sentence) leads to an accuracy of around 74%. 

## Future Work 

+ Hindi is a resource poor language, and as the system depends on other subsystems in the pipeline it is bounded by their accurarcies. 
+ Contradiction and Neutral can also be handled to ensure that this system is comprehensive and is a complete NLI tool 
+ The stemmer is a very basic stemmer. Stemming also leads to a loss of information regarding gender, numbers etc. This handling can be improved upon. 

## Refrences 

+ [On Demand Injection of Lexical Knowledge](https://pdfs.semanticscholar.org/ce0e/9e71a0b09cb9227296ceec26c8654a58e5c9.pdf)
+ [Natural Languahe Inference](http://nlpprogress.com/english/natural_language_inference.html) 

