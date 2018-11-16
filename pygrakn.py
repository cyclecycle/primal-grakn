import re
from pprint import pprint
import grakn


MULTISPACE = re.compile(r'\s\s+')


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

    def recurse_explanation(explanation):
        '''Get parsed explanations
        '''
        pass

    def get_explanation(self, concept_map, key=None):
        '''Get explanations for a given key. Goes one level deep at present
        '''
        explanation = []
        for k, v in concept_map.map().items():
            if not k == key and not v.is_inferred():
                return []
            else:
                for answer in concept_map.explanation().get_answers():
                    for k1, v1 in answer.map().items():
                        if k1 == key:
                            # v1 is the relationship we want to explain
                            for answer2 in answer.explanation().get_answers():
                                for k2, v2 in answer2.map().items():
                                    v2 = self.parse_concept(v2)
                                    if v2['base_type'] == 'relationship':
                                        explanation.append({k2: v2})
        return explanation

    def execute(self, query, from_file=False, **kwargs):
        if from_file:
            query = read_file(query)
        query = query.replace(';;', ';')  # Double semicolon can occur if user provides semicolon to match_or_insert
        query = query.replace('\n', ' ')
        query = MULTISPACE.sub(' ', query)
        answer_iterator = self.tx.query(query)
        data = []
        for concept_map in answer_iterator:
            for k, v in concept_map.map().items():
                explanation = self.get_explanation(concept_map, key=k)
                parsed = self.parse_concept(v, **kwargs)
                parsed['explanation'] = explanation
                data.append({k: parsed})
        return data

    ''' Parsing functions '''

    def parse_concept(self, concept, id_only=False, grakn_objs=False):
        if id_only:
            return {'id': concept.id}
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

    # def parse_entity(self, concept):
    #     d = {
    #         'id': concept.id,
    #         'type': concept.base_type.lower(),
    #         'isa': concept.type().label(),
    #         'attributes': list(self.parse_attributes(concept.attributes()))
    #     }
    #     return d

    # def parse_relationship(self, concept):
    #     d = {
    #         'id': concept.id,
    #         'type': concept.base_type.lower(),
    #         'isa': concept.type().label(),
    #         'roles': list(self.parse_roles(concept.role_players_map()))
    #     }
    #     return d

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

    ''' Convenience functions '''

    def match_or_insert(self, query):
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