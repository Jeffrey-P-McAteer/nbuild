
"""
The risk module holds a Mitigation class
and the Risk class.
"""

import html

class Mitigation:
    """
    The Mitigation class should only be constructed using the following static methods:
      - Mitigation.Accept()
      - Mitigation.Avoid('Description of how the risk is avoided; eg by dropping the feature if it cannot be built safely')
      - Mitigation.Control('Description of how the risk is controlled; eg by building 2x features to perform 1x task')
      - Mitigation.Transfer('To whom? Bob in dept X will handle risk Y because his task is relevant to Y')
    """
    @staticmethod
    def Accept(): # pylint: disable=missing-function-docstring
        return Mitigation(name='accept')

    @staticmethod
    def Avoid(how): # pylint: disable=missing-function-docstring
        return Mitigation(name='avoid', how=how)

    @staticmethod
    def Control(how): # pylint: disable=missing-function-docstring
        return Mitigation(name='control', how=how)

    @staticmethod
    def Transfer(to): # pylint: disable=missing-function-docstring
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
            raise Exception('Unknown mitigation name = {}'.format(self.name))


class Risk:
    """
    Describes a risk, it's probability, impact, and mitigation strategy.
    Default mitigation is to accept risks.
    """
    def __init__(self,
                 name=None,
                 if_=None,
                 then=None,
                 probability=5,
                 impact=5,
                 mitigation=Mitigation.Accept()):
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

        # print warnings that should be adressed but cannot stop the Risk from being constructed
        # These are also added to project.warnings when we are given the project object.
        self.warnings = []
        if not 'cost' in then.lower():
            w = 'WARNING: cost not mentioned in Risk "{}" "then" section (then={})'.format(name, then)
            self.warnings.append(w)
            print(w)
        if not 'schedule' in then.lower():
            w = 'WARNING: schedule not mentioned in Risk "{}" "then" section (then={})'.format(name, then)
            self.warnings.append(w)
            print(w)
        

        self.project = None
        self.name = name
        self.if_ = if_
        self.then = then
        self.probability = int(probability)
        self.impact = int(impact)
        self.mitigation = mitigation

        # These are derived information computed early for reporing purposes
        self.is_issue = self.probability >= 5
        self.is_watch_item = self.impact > 3 and mitigation.name.lower() == 'accept'

    def set_project(self, project):
        """Stores a reference to the project and adds warnings to project.warnings"""
        self.project = project
        self.project.warnings += self.warnings

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

