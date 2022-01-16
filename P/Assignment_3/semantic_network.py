from collections import Counter

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# Subclasse AssocOne
class AssocOne(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   ao = AssocOne('socrates','pai','sofronisco')

# Subclasse AssocNum
class AssocNum(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,float(e2))

#   Exemplo:
#   an = AssocNum('homem','temperatura',36.8)

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None,rel_type=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) 
                and (rel_type == None or isinstance(d.relation, rel_type)) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    # 2.1.
    def list_associations(self):
        return list(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association)]))

    # 2.2.
    def list_objects(self):
        return list(set([d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member)]))

    # 2.3.
    def list_users(self):
        return list(set(d.user for d in self.declarations))

    # 2.4.
    def list_types(self):
        return list(set(
            [d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member, Subtype))]
            +
            [d.relation.entity1 for d in self.declarations if isinstance(d.relation, Subtype)]
        ))

    # 2.5.
    def list_local_associations(self, entity):
        return list(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association) and entity in [d.relation.entity1, d.relation.entity2]]))

    # 2.6.
    def list_relations_by_user(self, user):
        return list(set([d.relation.name for d in self.declarations if d.user==user]))

    # 2.7.
    def associations_by_user(self, user):
        return len(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association) and d.user==user]))

    # 2.8.
    def list_local_associations_by_user(self, entity):
        return list(set([(d.relation.name, d.user) for d in self.declarations if isinstance(d.relation, Association) and entity in [d.relation.entity1, d.relation.entity2]]))

    # 2.9.
    def predecessor(self, A, B):
        """
        First check if there is any relation Member(B, A) or Subtype(B, A)
        Then check recursivly if there is any relation Subtype(B, C), with Subtype(C, A)
        """
        directPredecessors = [d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == B]        
        
        return A in directPredecessors or any([self.predecessor(A, predecessor) for predecessor in directPredecessors])

    # 2.10.
    def predecessor_path(self, ent1, ent2):
        """
        ent1 predecessor of ent2 (=) Member(ent2, ent1) or Subtype(ent2, ent1)
        Get path between ent1 and ent2
        """
        # Find direct predecessors of ent2
        directPredecessors = [d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == ent2]
        
        # If direct predecessor, return path
        if ent1 in directPredecessors:
            return [ent1, ent2]

        # Otherwise, get path for upper predecessors
        for path in [self.predecessor_path(ent1, predecessor) for predecessor in directPredecessors]:
            if path:
                return path + [ent2]

        # If ent1 is not predecessor of ent2 (not direct nor recursively)
        return None

    # 2.11. a)
    def query(self, entity, rel=None):
        """
        This method complements query_local(), by finding the inherited ASSOCIATIONs for an entity
        1.  Make query recursively foreach predecessor
        2.  Make local query with query_local()
            Here we use e1, because we want the entity one of the Association
            P.e. from altura(mamifero, 1.82), we want mamifero, not 1.82!
        Returns the merge of this teo queries
        """
        # Find direct predecessors of entity and foreach one make query for Association
        predecessorsQueries = [self.query(d.relation.entity2, rel) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        # Transform list of lists of declarations in list of declarations
        predecessorsQuery = [declaration for listOfQueries in predecessorsQueries for declaration in listOfQueries]

        # Make local query for Association
        localQuery = self.query_local(e1=entity, rel=rel, rel_type=Association)

        return localQuery + predecessorsQuery

    # 2.11. b)
    def query2(self, entity, rel=None):
        """
        This method complements query(), by finding the MEMBER and SUBTYPE local relations
        1. Find the inherited ASSOCIATION relations using query()
        2.  Make local query with query_local() for MEMBER and SUBTYPE
        """
        # Get inherited Association declarations
        q = self.query(entity, rel)

        # Make local query for Member and Subtype
        localQuery = self.query_local(e1=entity, rel=rel, rel_type=(Member, Subtype))

        return localQuery + q

    # 2.12.
    def query_cancel(self, entity, relName):
        """
        This method is similar to query(), but it ignores iherited associations when they are already defined locally
        The relName is mandatory, has it defines the Association type
        """
        # Find direct predecessors of entity and foreach one make query for Association
        predecessorsQueries = [self.query_cancel(d.relation.entity2, relName) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]

        # Make local query for Association
        localQuery = self.query_local(e1=entity, rel=relName, rel_type=Association)
        
        # Transform list of lists of declarations in list of declarations
        # Ignore iherited associations that are already defined locally 
        predecessorsQuery = [declaration for listOfQueries in predecessorsQueries for declaration in listOfQueries if not any(declaration.relation.name==d.relation.name for d in localQuery)]

        return localQuery + predecessorsQuery

    # 2.13.
    def query_down(self, entity, assocName=None, firstCall=True):
        """
        Finds assocName Associations for the descendants of entity
        (It ignores the assocName Associations for the entity)
        """
        pdqs = [ self.query_down(d.relation.entity1, assocName, False) for d in self.declarations if d.relation.entity2==entity and isinstance(d.relation, (Member, Subtype)) ]
        pdq = [ d for query in pdqs for d in query ]

        # Don't call query_local on first call (only on recursion)
        localQuery = self.query_local(e1=entity, rel=assocName, rel_type=Association) if not firstCall else []

        return localQuery + pdq


    # 2.14
    def query_induce(self, entity, assocName):
        """
        Find most common value for descendant assocName Association for a given entity
        It is used when we don't have info on that type of Association and we want to determin it by inference
        Using collections.Counter class, see https://docs.python.org/3/library/collections.html#collections.Counter
        """
        # Make query for descendant Associations on entity with name assocName 
        query = self.query_down(entity, assocName)

        if not query:
            return None

        # Start counter for association values (entity2)
        c = Counter([d.relation.entity2 for d in query])
        
        # Return the most common one        
        return c.most_common(1)[0][0]
            

    # 2.15. b)
    def query_local_assoc(self, entity, assocName):
        """
        This method allows queries for assocName Associations for a given entity
        Depending on the assoc type (Assotiation, AssocOne, AssocNum) it makes different processing
        """
        # Make local query for assoName Associations for entity
        localQueryAssoc = self.query_local(e1=entity, rel=assocName, rel_type=(Association, AssocOne, AssocNum))

        # Get values for entity
        values = [d.relation.entity2 for d in localQueryAssoc]

        if not localQueryAssoc:
            pass

        elif isinstance(localQueryAssoc[0].relation, AssocOne):
            # Get most common
            val, count = Counter(values).most_common(1)[0]
            # Return most frequent value and its frequency
            return (val, count/len(values))

        elif isinstance(localQueryAssoc[0].relation, AssocNum):
            # Find average value
            return sum(values)/len(values)

        elif isinstance(localQueryAssoc[0].relation, Association):
            # Get most common
            mc = Counter(values).most_common()
            # Return list of frequencies
            # Only return  values until frequency sum reaches 0.75
            frequencies = []
            frequency = 0
            for val, count in mc:
                frequencies.append((val, count/len(localQueryAssoc)))
                frequency += count/len(localQueryAssoc)
                if frequency >= 0.75:
                    return frequencies
        
        return None

    """ Teacher solution 
    def query_local_assoc(self, entity, assocName):
        local = self.query_local(e1=entity, rel=assocName)

        for l in local:
            if isinstance(l.relation, AssocOne):
                val, count = Counter([[d.relation.entity2 for d in local]]).most_common(1)[0]
                return val, count/len(local)
            if isinstance(l.relation, AssocNum):
                values = [d.relation.entity2 for d in local]
                return sum(values)/len(local)
            if isinstance(l.relation, Association):
                mc = []
                freq = 0
                for val, count in  Counter([[d.relation.entity2 for d in local]]).most_common():
                    mc.append((val, count/len(local)))
                    freq += count/len(local)
                    if freq > 0.75:
                        return mc
    """

    # 2.16.
    def query_assoc_value(self, entity, assocName):
        """
        This method helps determining the most accurate value for an Assocition assocName for an entity
        1. If the local Associations all have the same value, returns it
        2. If not, return the most common between the local and predecessor Associations
        """
        # Make local query for assocName Associations for entity
        localQueryAssoc = self.query_local(e1=entity, rel=assocName, rel_type=(Association, AssocOne, AssocNum))

        # Get values for entity
        lvalues = [d.relation.entity2 for d in localQueryAssoc]

        # a) If all local associations have the same value, return it
        if len(set(lvalues)) == 1:
            return lvalues[0]

        # b) Otherwise, ...
        # Get predecessor values
        predecessorsPlusLocal = self.query(entity=entity, rel=assocName)
        # Because it includes locals, remove them
        predecessors = [a for a in predecessorsPlusLocal if a not in localQueryAssoc]
        # Get values from relations (entity2)
        pvalues = [p.relation.entity2 for p in predecessors]

        # Define method to find the percentage of a value inside a list of values
        def perc(list, value):
            if list == []: return 0
            return len([l for l in list if l ==  value]) / len(list)
        
        # Return the most common value between local and predecessor relations 
        return max(lvalues + pvalues, key=lambda v: (perc(lvalues, v) + perc(pvalues, v)) / 2)




