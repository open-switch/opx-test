<%
import java.text.DateFormat
import java.text.SimpleDateFormat
%>
<STYLE>
BODY, TABLE, TD, TH, P {
  font-family:Verdana,Helvetica,sans serif;
  font-size:11px;
  color:black;
}
h1 { color:black; }
h2 { color:black; }
h3 { color:black; }
TD.bg1 { color:white; background-color:#0000C0; font-size:120% }
TD.bg2 { color:white; background-color:#4040FF; font-size:110% }
TD.bg3 { color:white; background-color:#8080FF; }
TD.test_passed { color:blue; }
TD.test_failed { color:red; }
TD.console { font-family:Courier New; }
</STYLE>
<BODY>

<TABLE>
  <TR><TD align="right"><IMG SRC="${rooturl}<%= build.result == hudson.model.Result.SUCCESS  ? "static/10dc1983/images/24x24/blue.png" : "static/e59dfe28/images/32x32/red.gif" %>" />
  </TD><TD valign="center"><B style="font-size: 150%;"><%= build.result == hudson.model.Result.SUCCESS ? "ALL TESTS PASSED" : "SOME TESTS FAILED OR THE JOB ENCOUNTERED A PROBLEM" %></B></TD></TR>
  <TR><TD>Build URL:</TD><TD><A href="${rooturl}${build.url}">${rooturl}${build.url}</A></TD></TR>
  <TR><TD>Project URL:</TD><TD><A href="${rooturl}${project.url}">${rooturl}${project.url}</A></TD></TR>
  <TR><TD>Build Name:</TD><TD>${build.displayName}</TD></TR>
  <TR><TD>Date of job:</TD><TD>${it.timestampString}</TD></TR>
  <TR><TD>Job duration:</TD><TD>${build.durationString}</TD></TR>
</TABLE>
<BR/>

<!-- Robot Framework Results -->
<%
def robotResults = false
def actions = build.actions // List<hudson.model.Action>
actions.each() { action ->
  if( action.class.simpleName.equals("RobotBuildAction") ) { // hudson.plugins.robot.RobotBuildAction
    robotResults = true %>
<p><h4>Robot Framework Results</h4></p>
<p><b>To view the Detailed Report in chrome, download Disable-Content-Security-Policy Extension and Disable it<b></p>
<p><a href="${rooturl}${build.url}robot/report/report.html">Detailed Report</a></p>
<p>Pass Percentage: <%= action.overallPassPercentage %>%</p>
<table cellspacing="0" cellpadding="4" border="1" align="center">
<thead>
<tr bgcolor="#F3F3F3">
  <td><b>Test Name</b></td>
  <td><b>Status</b></td>
  <td><b>Execution Datetime</b></td>
</tr>
</thead>
<tbody>
<%  def suites = action.result.allSuites
    suites.each() { suite -> 
      def currSuite = suite
      def suiteName = currSuite.displayName
      // ignore top 2 elements in the structure as they are placeholders
      while (currSuite.parent != null && currSuite.parent.parent != null) {
        currSuite = currSuite.parent
        suiteName = currSuite.displayName + "." + suiteName
      } %>
<tr><td colspan="3"><b><%= suiteName %></b></td></tr>
<%    DateFormat format = new SimpleDateFormat("yyyyMMdd HH:mm:ss.SS")
      def execDateTcPairs = []
      suite.caseResults.each() { tc ->
        Date execDate = format.parse(tc.starttime)
        execDateTcPairs << [execDate, tc]
      }
      // primary sort execDate, secondary displayName
      execDateTcPairs = execDateTcPairs.sort{ a,b -> a[1].displayName <=> b[1].displayName }
      execDateTcPairs = execDateTcPairs.sort{ a,b -> a[0] <=> b[0] }
      execDateTcPairs.each() {
        def execDate = it[0]
        def tc = it[1]  %>
<tr>
  <td><%= tc.displayName %></td>
  <td style="color: <%= tc.isPassed() ? "#66CC00" : "#FF3333" %>"><%= tc.isPassed() ? "PASS" : "FAIL" %></td>
  <td><%= execDate %></td>
</tr>
<%    } // tests
    } // suites %>
</tbody></table><%
  } // robot results
}
if (!robotResults) { %>
<p>See the <a href="${rooturl}${build.url}console">Ansible console output logs</a></p>
<%
} %>

<br />

<!-- CONSOLE OUTPUT -->
<% if(build.result==hudson.model.Result.FAILURE) { %>
<p>See the <a href="${rooturl}${build.url}console">console output</a></p>
<br />
<% } %>

</BODY>
