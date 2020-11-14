
"""
The report module contains the details of formatting
and writing out nbuild_test_report.html.
As more reports are added their implementations
will be done here.
"""

import os

from nbuild.test import Test

def write_reports_to(project, directory):
    """Write all project reports to a directory"""
    test_rep_path = os.path.join(directory, 'nbuild_test_report.html')
    with open(test_rep_path, 'w') as test_rep:
        # test_table is a bunch of <tr> rows with <td> columns
        test_table = create_task_table(project.tests)

        closing_remarks = ""
        
        test_rep.write("""<DOCTYPE html>
<html lang="en">
  <head>
    <title>{name} Test Report</title>
    <style>
table {{
  table-layout: auto;
  width: 100%;
  background-color: #ffffff;
}}
table, th, td {{
  border: 1px solid black;
  border-collapse: collapse;
}}
th, td {{
  padding: 4pt 8pt;
  text-align: left;
  width: auto;
}}
tr {{
  /*grid-template-columns: repeat(3, 1fr);*/
  grid-template-columns: 9ch 14ch 3fr;
  justify-content: flex-start;
  display: grid;
}}
.passed {{
  background-color: #90ee90; /* light green */
}}
.failed {{
  background-color: #ffcccb; /* light red */
}}
pre {{
  overflow-x: auto;
  white-space: pre-wrap;
  white-space: -moz-pre-wrap;
  white-space: -pre-wrap;
  white-space: -o-pre-wrap;
  word-wrap: break-word;
}}
.expanded-row-content {{
  border-top: none;
  display: grid;
  grid-column: 1/-1;
  justify-content: flex-start;
  color: #AEB1B3;
  font-size: 13px;
  background-color: #e0e0e0;
}}
.hide-row {{
  display: none;
}}
.expanded-row-content > table {{
  border: none;
}}

    </style>
  </head>
  <body>
    <h1>{name} Test Report</h1>
    <details><summary>Deliverables</summary>
      {deliverable}
    </details>
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
    {closing_remarks}
    <script>
    function toggleRow(event, element) {{
      if (event.target == element || event.target.parentNode == element) {{
        element.getElementsByClassName('expanded-row-content')[0].classList.toggle('hide-row');
      }}
    }}
    </script>
  </body>
</html>
""".format(
        name=project.name,
        deliverable=project.deliverable.get_report_desc(),
        test_table=test_table,
        closing_remarks=closing_remarks
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
