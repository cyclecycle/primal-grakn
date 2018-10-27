import re
from pprint import pprint
import grakn


MULTISPACE = re.compile(r'\s\s+')


class Graph():

    def __init__(self, keyspace, **kwargs):
        self.keyspace = keyspace

    def __enter__(self, uri='localhost:48555', **kwargs):
        self.client = grakn.Grakn(uri=uri)
        self.session = self.client.session(keyspace=self.keyspace, **kwargs)
        self.tx = self.session.transaction(grakn.TxType.BATCH)
        return self

    def commit(self):
        self.tx.commit()

    def execute(self, query, **kwargs):
        query = query.replace('\n', ' ')
        query = MULTISPACE.sub(' ', query)
        print(query)
        answer_iterator = self.tx.query(query)
        data = []
        try:
            answer = answer_iterator.collect_concepts()
        except:
            return []
        for concept in answer:
            parsed = self.parse_concept(concept, **kwargs)
            data.append(parsed)
        return data

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
        # print(dir(concept))
        if hasattr(concept, 'label'):
            d['label'] = concept.label()
        # if hasattr(concept, 'roles'):
        #     d['roles'] = list(self.parse_roles(concept.roles(), players=False))
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

    def __exit__(self, type, value, traceback):
        self.tx.close()
        self.session.close()


def remove_empty_keys(dict_):
    new_dict = {}
    for k, v in dict_.items():
        if v:
            new_dict[k] = v
    return new_dict