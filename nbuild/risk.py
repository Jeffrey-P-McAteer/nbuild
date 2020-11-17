
import html

class Risk:
    def __init__(self, name=None, if_=None, then=None, probability=5, impact=5):
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

        self.name = name
        self.if_ = if_
        self.then = then
        self.probability = int(probability)
        self.impact = int(impact)


    def get_report_desc(self):
        """
        Return a description of the risk, for use in creating lists.
        """
        return """
          <details class="shaded">
            <summary>{name}</summary>
            <p><b>IF:</b>{if_}</p>
            <p><b>THEN:</b>{then}</p>
          </details>
        """.format(
            name=html.escape(self.name),
            if_=html.escape(self.if_),
            then=html.escape(self.then)
        ).strip()

