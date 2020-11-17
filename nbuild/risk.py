
import html

class Mitigation:
    @staticmethod
    def Accept():
        return Mitigation(name='accept')

    @staticmethod
    def Avoid(how):
        return Mitigation(name='avoid', how=how)

    @staticmethod
    def Control(how):
        return Mitigation(name='control', how=how)

    @staticmethod
    def Transfer(to):
        return Mitigation(name='transfer', to=to)

    def __init__(self, name=None, **kwargs):
        if not name:
            raise Exception('Mitigation must have a name!')
        self.name = name
        self.kwargs = dict(kwargs)

    def get_report_desc(self):
        """
        Return a description of the mitigation
        """
        if self.name == 'accept':
          return 'Accept'

        elif self.name == 'avoid':
          return 'Avoid: {}'.format(html.escape(self.kwargs['how']))

        elif self.name == 'control':
          return 'Control: {}'.format(html.escape(self.kwargs['how']))

        elif self.name == 'transfer':
          return 'Transfer to {}'.format(html.escape(self.kwargs['to']))

        else:
            raise Exception('Unknown mitigation name = {}'.format())


class Risk:
    def __init__(self, name=None, if_=None, then=None, probability=5, impact=5, mitigation=Mitigation.Accept(), details=None):
        if not name:
            raise Exception('Risk must have a name!')
        
        if not if_:
            raise Exception('Risk must have an "if_" specified!')
        
        if not then:
            raise Exception('Risk must have a "then" specified!')
        
        if probability < 1 or probability > 5:
            raise Exception('probability must be between 1 and 5 inclusive, {} is outside this range.'.format(probability))

        if impact < 1 or impact > 5:
            raise Exception('impact must be between 1 and 5 inclusive, {} is outside this range.'.format(impact))

        if not mitigation or not isinstance(mitigation, Mitigation):
            raise Exception('mitigation must be of type Mitigation')

        self.name = name
        self.if_ = if_
        self.then = then
        self.probability = int(probability)
        self.impact = int(impact)
        self.mitigation = mitigation

    def get_report_desc(self):
        """
        Return a description of the risk, for use in creating lists.
        """
        return """
          <details class="shaded">
            <summary>{name}</summary>
            <p><b>IF: </b>{if_}</p>
            <p><b>THEN: </b>{then}</p>
            <p><b>Mitigation: </b>{mitigation}</p>
          </details>
        """.format(
            name=html.escape(self.name),
            if_=html.escape(self.if_),
            then=html.escape(self.then),
            mitigation =self.mitigation.get_report_desc(),
        ).strip()

