#encoding: utf8

from semantic_network import *
from bayes_net import *


class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)
        # IMPLEMENT HERE (if needed)
        pass

    def source_confidence(self,user):
        # Wrong and correct answers counter
        countWrong = 0
        countCorrect = 0

        # For each declaration the user did
        for dcl in [d for d in self.query_local(user) if isinstance(d.relation, AssocOne)]:
            # Answers count
            answersCount = {}

            # Get user answer
            userAnswer = dcl.relation.entity2

            # Get all answers
            allAnswers = [d for d in self.query_local(e1=dcl.relation.entity1, relname=dcl.relation.name) if isinstance(d.relation, AssocOne)] 

            # Get answers count
            for d in allAnswers:
                # If answer in dict we increment
                if d.relation.entity2 in answersCount:
                    answersCount[d.relation.entity2] = answersCount[d.relation.entity2] + 1
                # If answer not in dict we set value
                else:
                    answersCount[d.relation.entity2] = 1

            # Get most frequent answer
            mostFreqAnswer = max(answersCount, key=answersCount.get)

            # Count correct and wrong answers or if its a stalemate
            if userAnswer == mostFreqAnswer or answersCount[userAnswer] == answersCount[mostFreqAnswer]:
                countCorrect = countCorrect + 1
            else:
                countWrong = countWrong + 1
                
        return (1 - 0.75**countCorrect)*0.75**countWrong

    def query_with_confidence(self,entity,assoc):
        # get parents results
        parentsResults = [self.query_with_confidence(d.relation.entity2,assoc) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        
        # number of parents
        numParents = len(parentsResults)
        
        # Get average of results from parents
        inheritedResults = {}

        # for each result we create a dict with the average
        for rslt in parentsResults:
            # if there is a result
            if rslt:
                # for each key in result
                for key in rslt.keys():
                    if key in inheritedResults:
                        inheritedResults[key] = inheritedResults[key] + rslt[key]/numParents
                    else:
                        inheritedResults[key] = rslt[key]/numParents

        # number of occurences locally
        localResults = {}

        # Number of declarations of assoc in entity
        T = 0

        # Get local occurences
        localAnswers = [d for d in self.query_local(e1=entity, relname=assoc) if isinstance(d.relation, AssocOne)]
        
        # Get number of occurences for each alternative value
        for answr in localAnswers:
            # Increment number of declarations
            T = T + 1

            # Check if value already registered on local dict
            if answr.relation.entity2 in localResults:
                localResults[answr.relation.entity2] = localResults[answr.relation.entity2] + 1
            else:
                localResults[answr.relation.entity2] = 1
        
        # for each key
        for k in localResults.keys():
            # Get confidence value locally
            localResults[k] = conf(localResults[k], T)
        
        # return avgConf
        return avgConf(localResults, inheritedResults)

def avgConf(local, inherited):
    # final result of confidence
    finalResult = {}

    # If there are no local and no inherited results we return empty
    if not local and not inherited:
        return finalResult

    # If there are no inherited results, the local results should be returned
    if local and not inherited:
        return local

    # If there are no local results, the inherited results should be returned with a discount of 10% (i.e. multiply confidences by 0.9)
    if not local and inherited:
        # for each key we add it to the finalResult dict with a 10% discount on weight
        for key in inherited.keys():
            finalResult[key] = inherited[key]*0.9
        return finalResult

    # If there are local and inherited results, the final confidence values are computed by weighted average, with 0.9 for the local confidences and 0.1 for the inherited confidences.
    if local and inherited:
        # for each key on local results we add it with a weight of 0.9
        for key in local.keys():
            finalResult[key] = local[key]*0.9

        # for each key on local results we add it with a weight of 0.1  
        for key in inherited.keys():
            if key in finalResult:
                finalResult[key] = finalResult[key] + inherited[key]*0.1
            else:
                finalResult[key] = inherited[key]*0.1
        return finalResult

def conf(n, T):
    return n/(2*T) + (1 - n/(2*T))*(1 - 0.95**n)*0.95**(T - n)


class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)

    def individual_probabilities(self):
        probs = dict()

        # For each variable
        for var in self.dependencies.keys():
            # Get all vars besides this one
            variaveis = [k for k in self.dependencies.keys() if k!=var]

            # Get conjuctions
            conjList = self.conjunctions(variaveis)

            # Calculate probability for each var
            probs[var] = round(sum([self.jointProb([(var, True)] + c) for c in conjList]), 4)

        # Return probabilities
        return probs

    def conjunctions(self, variaveis):
        # Terminal case
        if len(variaveis) == 1:
            return [[(variaveis[0], True)],[(variaveis[0], False)]]

        l = []
        for c in self.conjunctions(variaveis[1:]):
            l.append([(variaveis[0], True)] + c)
            l.append([(variaveis[0], False)] + c)

        return l

