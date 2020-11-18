
"""
The report module contains the details of formatting
and writing out nbuild_test_report.html.
As more reports are added their implementations
will be done here.
"""

import os
import datetime
import html
import json

from nbuild.test import Test

def write_reports_to(project, directory):
    """Write all project reports to a directory"""
    
    write_test_report(project, os.path.join(directory, 'nbuild_test_report.html'))
    write_risk_report(project, os.path.join(directory, 'nbuild_risk_report.html'))


# CSS styles are inlined into all reports
REPORT_CSS = """
html, body {
  background: #ffffff;
  color: #000000;
}
table {
  table-layout: auto;
  width: 100%;
  background-color: #ffffff;
}
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  padding: 4pt 8pt;
  text-align: left;
  width: auto;
}
tr {
  /*grid-template-columns: repeat(3, 1fr);*/
  grid-template-columns: 9ch 14ch 3fr;
  justify-content: flex-start;
  display: grid;
}
.passed {
  background-color: #90ee90; /* light green */
}
.failed {
  background-color: #ffcccb; /* light red */
}
pre {
  overflow-x: auto;
  white-space: pre-wrap;
  white-space: -moz-pre-wrap;
  white-space: -pre-wrap;
  white-space: -o-pre-wrap;
  word-wrap: break-word;
  padding: 2px 4px;
  border: 1px solid black;
  background: rgba(20, 20, 20, 0.05);
}
.expanded-row-content {
  border-top: none;
  display: grid;
  grid-column: 1/-1;
  justify-content: flex-start;
  /*color: #AEB1B3;*/
  font-size: 13px;
  background-color: #e0e0e0;
}
.hide-row {
  display: none;
}
.expanded-row-content > table {
  border: none;
}
details.shaded {
  border: 1px solid black;
  padding: 2pt 4pt;
  margin: 1pt 2pt;
  background: rgba(20, 20, 20, 0.05);
  background-clip: content-box;
}
details.shaded > summary {
  background: #ffffff;
}

/* specific to risk reports only */
#risk_matrix, #risk_matrix > div {
  width: 850pt !important; /* 25% larger b/c we only draw chart in 75% of stage */
  height: 480pt !important;
}
.anychart-credits { display: none; }

"""


def write_risk_report(project, risk_rep_path):
    """
    Given a project, extract risk data and write it to an HTML document
    at risk_rep_path
    """
    with open(risk_rep_path, 'w') as risk_rep:

        risk_list = create_risk_list(project.risks)
        issue_list = create_risk_list([r for r in project.risks if r.is_issue])
        watch_items_list = create_risk_list([r for r in project.risks if r.is_watch_item])

        anychart_init_script = r"""
anychart.onDocumentReady(function () {
  var chart = anychart.heatMap(window.risk_data);

  chart.width = '680pt';
  chart.height = '480pt';


  chart.stroke('#fff');
  chart
    .hovered()
    .stroke('6 #fff')
    .fill('#545f69')
    .labels({ fontColor: '#fff' });

  chart.bounds(0, 0, "75%", "100%");

  chart.interactivity().selectionMode('none');

  chart
    .title()
    .enabled(false)
    .text('Risk Matrix')
    .padding([0, 0, 20, 0]);

  chart
    .labels()
    .enabled(true)
    .minFontSize(14)
    .format(function () {
      var c = JSON.parse(this.heat)["risk_count"];
      if (c) {
        return c;
      }
      return '';
    });

  chart.yAxis().stroke(null);
  chart.yAxis().labels().padding([0, 15, 0, 0]);
  chart.yAxis().ticks(false);
  chart.yScale().inverted(false);
  chart.yAxis().orientation("left");
  chart.yAxis().title().enabled(true);
  chart.yAxis().title().useHtml(true);
  chart.yAxis().title().text(
    '<span style="font-size:1.6em;">Likelihood</span> <em>(1-rare, 5-guaranteed to occur)</em>'
  );
  
  chart.xAxis().stroke(null);
  chart.xAxis().ticks(false);
  chart.xScale().inverted(false);
  chart.xAxis().orientation("bottom");
  chart.xAxis().title().enabled(true);
  chart.xAxis().title().useHtml(true);
  chart.xAxis().title().text(
    '<span style="font-size:1.6em;">Consequence</span> <em>(1-small impact, 5-project will fail)</em>'
  );

  chart.tooltip().allowLeaveChart(true);
  //chart.tooltip().allowLeaveScreen(true);
  //chart.tooltip().allowLeaveStage(true); // causes scrolling bug
  chart.tooltip().fontColor("#ffffff");
  chart.tooltip().background().fill("#000000");
  chart.tooltip().separator(true);
  chart.tooltip().title().useHtml(true);
  chart
    .tooltip()
    .useHtml(true)
    .titleFormat(function () {
      var c = JSON.parse(this.heat)["risk_count"];
      if (c) {
        return c + ' risks';
      }
      return 'no risks';
    })
    .format(function () {
      risk_html = JSON.parse(this.heat)["risk_html"];
      return (
        ''+risk_html+'<br>'+
        '<span style="color: #CECECE">Probability/Likelihood: </span>' +
        this.y +
        '<br/>' +
        '<span style="color: #CECECE">Impact/Consequence: </span>' +
        this.x
      );
    });

  chart.container('risk_matrix');
  chart.draw();

  window.chart = chart; // for debugging in browsers
});

"""

        risk_rep.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <title>{name} Risk Report</title>

    <!-- TODO we should inline these resources, possibly using Google's closure compiler to remove unreached JS branches -->

    <script src="https://cdn.anychart.com/releases/v8/js/anychart-base.min.js"></script>
    <script src="https://cdn.anychart.com/releases/v8/js/anychart-ui.min.js"></script>
    <script src="https://cdn.anychart.com/releases/v8/js/anychart-exports.min.js"></script>
    <script src="https://cdn.anychart.com/releases/v8/js/anychart-heatmap.min.js"></script>
    <link href="https://cdn.anychart.com/releases/v8/css/anychart-ui.min.css" type="text/css" rel="stylesheet">
    <link href="https://cdn.anychart.com/releases/v8/fonts/css/anychart-font.min.css" type="text/css" rel="stylesheet">
    
    <style>{REPORT_CSS}</style>
  </head>
  <body>
    <h1>{name} Risk Report</h1>
    <p>Point of Contact: <code>{poc}</code></p>
    <details class="shaded"><summary>Deliverables</summary>
      {deliverable}
    </details>
    <br>
    
    <h2>All Risks</h2>
    {risk_list}

    <h2>Risk Matrix</h2>
    <div id="risk_matrix"></div>
    <script>window.risk_data = {risk_data};</script>
    <script>{anychart_init_script}</script>

    <h3>Issues <em>(risks with likelihood of 5)</em></h3>
    {issue_list}

    <h3>Watch Items <em>(risks with impact > 3 and mitigation of "Accept")</em></h3>
    {watch_items_list}

    <h2>Warnings</h2>
    <em>These are minor issues detected when saving the project description</em>
    <pre>{warnings}</pre>

  </body>
</html>
""".format(
        REPORT_CSS=REPORT_CSS,
        name=html.escape(project.name),
        poc=html.escape(project.poc),
        deliverable=project.deliverable.get_report_desc(),
        risk_list=risk_list,
        issue_list=issue_list,
        watch_items_list=watch_items_list,
        risk_data=create_risk_anychart_matrix_data(project.risks),
        anychart_init_script=anychart_init_script,
        warnings=project.get_warning_lines(),
      ))

    project.reports.append(risk_rep_path)

def write_test_report(project, test_rep_path):
    """
    Given a project that has been evaluated (.evaluate()),
    extract test data and write it to an HTML document at risk_rep_path
    """
    with open(test_rep_path, 'w') as test_rep:
        # test_table is a bunch of <tr> rows with <td> columns
        test_table = create_task_table(project.tests)

        test_rep.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <title>{name} Test Report</title>
    <style>{REPORT_CSS}</style>
  </head>
  <body>
    <h1>{name} Test Report</h1>
    <p>Point of Contact: <code>{poc}</code></p>
    <details class="shaded"><summary>Deliverables</summary>
      {deliverable}
    </details>
    <br>
    <p>Test duration: <code>{eval_duration}</code> (hours:minutes:seconds)</p>
    <br>
    <table>
      <tr>
        <th>Tests</th>
        <th>Status</th>
        <th>Description</th>
      </tr>
      {test_table}
    </table>
    <br>

    <script>
    function toggleRow(event, element) {{
      if (event.target == element || event.target.parentNode == element) {{
        element.getElementsByClassName('expanded-row-content')[0].classList.toggle('hide-row');
      }}
    }}
    </script>

    <h2>Warnings</h2>
    <em>These are minor issues detected when saving the project description</em>
    <pre>{warnings}</pre>

  </body>
</html>
""".format(
        REPORT_CSS=REPORT_CSS,
        name=html.escape(project.name),
        poc=html.escape(project.poc),
        deliverable=project.deliverable.get_report_desc(),
        eval_duration=datetime.timedelta(seconds=project.evaluation_duration_s),
        test_table=test_table,
        warnings=project.get_warning_lines(),
      ))

    project.reports.append(test_rep_path)

def create_task_table(tests):
    """A recursive function that makes <tr> elements, possibly with a <table> element containing sub-task tables"""
    table = ""
    if isinstance(tests, list):
        for t in tests:
            table += create_task_table(t)
    elif isinstance(tests, Test):
        t = tests
        if tests.tests:
            # Write child tests to sub-table
            table = ('<tr onclick="toggleRow(event, this)"><td>{tests}</td><td class="{_class}">{passed}</td><td>{description}</td>'+
                    '<td class="expanded-row-content hide-row">'+
                    '<table><tr><th>Tests</th><th>Status</th><th>Description</th></tr>{child_test_table}</table>'+
                    '</td></tr>').format(
                _class='passed' if t.passed else 'failed',
                passed='Passed' if t.passed else 'Failed',
                description=t.get_report_desc(),
                tests=len(tests.tests),
                child_test_table=create_task_table(tests.tests)
            )
        else:
            # Create a simple row
            table = '<tr><td>0</td><td class="{_class}">{passed}</td><td>{description}</td></tr>'.format(
                _class='passed' if t.passed else 'failed',
                passed='Passed' if t.passed else 'Failed',
                description=t.get_report_desc()
            )
    else:
        raise Exception('Unknown data sent to create_task_table: {}'.format(tests))
    return table


def create_risk_list(risks, simple=False):
    """
    Turns a risk objects into HTML. if simple=True this becomes a <ul>,
    otherwise it becomes a list of <details> which may be expanded for details.
    """
    if simple:
        table = "<ul>"
        for r in risks:
            table += "<li>{} ({})</li>".format( html.escape(r.name), r.mitigation.name )
        table += "</ul>"
        return table
    else:
        table = "<p>"
        for r in risks:
            table += r.get_report_desc()
        table += '<p>'
        return table


def create_risk_anychart_matrix_data(risks):
    """
    Turns risk objects into JSON suitable for use in an anychart heatmap.
    The 'heat' value is a JSON string containing an HTML risk list and a
    count of the risks in the given impact + probability square.
    """
    risk_dicts = []
    for impact in range(1, 6):
        for probability in range(1, 6):
            filtered_risks = filter_risks(risks, impact, probability)
            risk_dicts += [{
                'x': impact,
                'y': probability,
                'heat': json.dumps({ # javascript parses the ['heat'] variable attached to points for details
                    'risk_html': create_risk_list(filtered_risks, simple=True),
                    'risk_count': len(filtered_risks),
                }),
                'fill': risk_color_for(probability, impact, len(filtered_risks) )
            }]

    return json.dumps(risk_dicts, separators=(',', ':'))

def risk_color_for(probability, impact, num_risks): # pylint: disable=too-many-return-statements
    """
    Given a probability + impact, color a square.
    If there are no risks the square will be light grey (#f0f0f0).
    """
    # See https://www.colourlovers.com/palette/56122/Sweet_Lolly
    colors = ["#00C176", "#88C100", "#FABE28", "#FF8A00", "#FF003C", "#f0f0f0"]
    
    if num_risks > 0: # we have some risks, color them

        # Colors taken directly off an internal slide
        if probability <= 5 and impact <= 1: # green
            return colors[0]
        
        if probability <= 3 and impact <= 2: # green
            return colors[0]
        if probability <= 5 and impact <= 2: # yellow
            return colors[2]

        if probability <= 2 and impact <= 3: # green
            return colors[0]
        if probability <= 4 and impact <= 3: # yellow
            return colors[2]
        if probability <= 5 and impact <= 3: # red
            return colors[4]

        if probability <= 1 and impact <= 4: # green
            return colors[0]
        if probability <= 3 and impact <= 4: # yellow
            return colors[2]
        if probability <= 5 and impact <= 4: # red
            return colors[4]

        if probability <= 2 and impact <= 5: # yellow
            return colors[2]
        if probability <= 5 and impact <= 5: # red
            return colors[4]

    # Nothing else matched, use grey
    return colors[5]


def filter_risks(risks, impact_eq, probability_eq):
    """Returns only risks which match the given impact and probability numbers"""
    return [r for r in risks if r.impact == impact_eq and r.probability == probability_eq]

