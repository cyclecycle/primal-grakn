import re
from pprint import pprint
import grakn
from grakn.service.Session.Concept import Concept as GraknConcept
from grakn.service.Session.util.ResponseReader import ConceptMap as GraknConceptMap


MULTISPACE = re.compile(r'\s\s+')

'''
Perhaps the responses should be really be extensions of Grakn objects. With methods like .data() for getting the parsed structures.
'''


class ConceptDict(dict):

    def __init__(self, grakn_concept, *args, **kwargs):
        super(ConceptDict, self).__init__(*args, **kwargs)
        self.object = grakn_concept
        self.update(self.parse_concept(grakn_concept))
        # self.explanations = self.parse_explanation_tree()

    def parse_concept(self, concept, grakn_objs=False):
        d = {
            'id': concept.id,
            'base_type': concept.base_type.lower(),
            'type': concept.type().label()
        }
        if grakn_objs:
            d['obj'] = concept
        if hasattr(concept, 'label'):
            d['label'] = concept.label()
        if hasattr(concept, 'role_players'):
            d['relates'] = list(self.parse_role_players(concept.role_players_map()))
        if hasattr(concept, 'attributes'):
            d['attributes'] = list(self.parse_attributes(concept.attributes()))
        if hasattr(concept, 'value'):
            d['value'] = concept.value()
        d = remove_empty_keys(d)
        return d

    def parse_attributes(self, attributes):
        for attr in attributes:
            yield self.parse_attribute(attr)

    def parse_attribute(self, concept):
        d = {
            'id': concept.id,
            'label': concept.type().label(),
            'value': concept.value()
        }
        return d

    def parse_roles(self, concept, **kwargs):
        for role in concept:
            yield self.parse_role(role, **kwargs)

    def parse_role(self, concept, players=True):
        d = {
            'id': concept.id,
            'label': concept.label(),
        }
        if players:
            players = []
            for player in concept.players():
                players.append({
                    'id': player.id,
                    'label': player.label()
                })
            d['players'] = players
        return d

    def parse_role_players(self, concept):
        d = []
        for role, players in concept.items():
            role = self.parse_role(role, players=False)
            for player in players:
                player = self.parse_concept(player)
                d.append({
                    'role': role,
                    'player': player
                })
        # print(concept)
        return d


class ConceptMap(dict):

    def __init__(self, concept_map, *args, **kwargs):
        super(ConceptMap, self).__init__(*args, **kwargs)
        self.object = concept_map
        self.update(self.parse_concepts(concept_map))

    def parse_concepts(self, concept_map):
        data = {}
        for k, v in concept_map.map().items():
            v = ConceptDict(v)
            data[k] = v
        return data


class Graph():

    def __init__(self, uri='localhost:48555', keyspace=None, credentials={}, **kwargs):
        assert keyspace, 'Please provide keyspace'
        self.keyspace = keyspace
        self.uri = uri
        self.credentials = credentials

    ''' Context management '''

    def __enter__(self, **kwargs):
        if self.credentials:
            self.client = grakn.Grakn(uri=self.uri, credentials=self.credentials)
        else:
            self.client = grakn.Grakn(uri=self.uri)
        self.session = self.client.session(keyspace=self.keyspace, **kwargs)
        self.tx = self.session.transaction(grakn.TxType.BATCH)
        return self

    def __exit__(self, type, value, traceback):
        self.tx.close()
        self.session.close()

    ''' User functions '''

    def commit(self):
        self.tx.commit()

    def execute(self, query, from_file=False, **kwargs):
        if from_file:
            query = read_file(query)
        query = query.replace(';;', ';')  # Double semicolon can occur if user provides semicolon to match_or_insert
        query = query.replace('\n', ' ')
        query = MULTISPACE.sub(' ', query)
        answer_iterator = self.tx.query(query)
        concept_maps = []
        for concept_map in answer_iterator:
            concept_map = ConceptMap(concept_map)
            concept_maps.append(concept_map)
        return concept_maps
    # def parse_explanation_tree(self, concept_map, **kwargs):
    #     parsed = []
    #     for answer in concept_map.explanation().get_answers():
    #         for k, v in concept_map.map().items():
    #             v = self.parse_concept(v, **kwargs)
    #             print(k, v)
    #         # if v.is_inferred():
    #     raise


    # def get_explanation(self, concept_map, key=None):
    #     '''Get explanations for a given key. Goes one level deep at present.
    #     '''
    #     explanation = []
    #     for k, v in concept_map.map().items():
    #         if not k == key and not v.is_inferred():
    #             return []
    #         else:
    #             for answer in concept_map.explanation().get_answers():
    #                 for k1, v1 in answer.map().items():
    #                     if k1 == key:
    #                         # v1 is the relationship we want to explain
    #                         for answer2 in answer.explanation().get_answers():
    #                             for k2, v2 in answer2.map().items():
    #                                 v2 = self.parse_concept(v2)
    #                                 if v2['base_type'] == 'relationship':
    #                                     explanation.append({k2: v2})
    #     return explanation

    ''' Parsing functions '''

    # def parse_concept(self, concept, id_only=False, grakn_objs=False):
    #     if id_only:
    #         return {'id': concept.id}
    #     d = {
    #         'id': concept.id,
    #         'base_type': concept.base_type.lower(),
    #         'type': concept.type().label()
    #     }
    #     if grakn_objs:
    #         d['obj'] = concept
    #     if hasattr(concept, 'label'):
    #         d['label'] = concept.label()
    #     if hasattr(concept, 'role_players'):
    #         d['relates'] = list(self.parse_role_players(concept.role_players_map()))
    #     if hasattr(concept, 'attributes'):
    #         d['attributes'] = list(self.parse_attributes(concept.attributes()))
    #     if hasattr(concept, 'value'):
    #         d['value'] = concept.value()
    #     d = remove_empty_keys(d)
    #     return d

    ''' Convenience functions '''

    def match_or_insert(self, query):
        '''TODO handle any kind of match clause. Problem is you don't know you know what you're trying to insert to know whether it exists. Need to look in the insert clause and find out, then construct a match and get for it.
        '''
        q = 'match {}; get;'.format(query)
        response = self.execute(q)
        if not response:
            q = 'insert {};'.format(query)
            response = self.execute(q)
        return response


def remove_empty_keys(dict_):
    new_dict = {}
    for k, v in dict_.items():
        if v:
            new_dict[k] = v
    return new_dict


def read_file(path):
    with open(path, encoding='utf-8') as file:
        return file.read()