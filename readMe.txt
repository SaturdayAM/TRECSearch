
/*********************************************************
 *		ReadMe for TREC Engine			 				 *
 *                                                       * 
 *  Jerry Lee                                            *
 *********************************************************/
A search engine with relevance feedback query expansion.
Retrieves over NIST Text Retrieval Conference test collections.

Components of the project include:
 tokenization, indexing, 
query processing, cosine vector space relevance ranking, and 
pseudo-relevance feedback query expansion. 

Run from command line:
python queryExpansion.py [N feedback docs] [T top terms]

Outputs to rankings folder as "expandedCosineVSM.txt."

Evaluate with trecEval

parameters N = number of top documents to feed back per query
and T = number of top terms to feed back per query. The
program is run from the command line as follows:

python queryExpansion.py [N feedback docs] [T top terms]

So to run queryExpansion with N = 5 and T = 3, type:

python queryExpansion.py 5 3

The output is in the rankings folder, under the name 
"expandedCosineVSM.txt."

Mean Average Precision scores can be calculated using
NIST's trec_eval software found at:
http://trec.nist.gov/trec_eval/


