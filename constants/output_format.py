# JSON_FORMAT = """
# {
#   "test_cases": [
#     {
#       "ID": "CXXXX[numeric]",
#       "Title": "User wants to enter information on Supporting Information so that it can be submitted for review/approval.",
#       "Preconditions": "Functional Area: Allows users to submit complete and accurate Supporting Information as part of their online application, reducing RTP applications, and time spent by staff processing to correct applications.\nPre-Condition:\n1. The provider user has PMM portal Access based on the Role Based Access Control (RBAC).\n2. The User is the Admin/Owner of New Enrolment Application.\n3. The user is logged in to PMM Portal and on License and Certifications > Supporting Information > Provider Type 57.",
#       "Steps": "1. The user successfully logs into the PMM portal and navigates to the License and Certifications > Supporting Information screen.",
#       "Expected Results": "1. User is able to log in successfully.\n2. User is able to view the License and Certifications > Supporting Information screen.\n3. User is able to view Page Heading: Supporting Information.",
#       "Priority": "Medium"  // Based on the criticality of the test scenario.
#     }
#   ],
#   "selenium_scripts": {test_case_id: "CXXXX[numeric]",// Link this script to its matching test case.
#     "script": [Java Selenium test code string here] // Java code block.
#   },
# }
# """
# JSON_FORMAT = """
# {
#   "test_cases": [
#     {
#       "ID": "CXXXX[numeric]",
#       "Title": "Short title of the scenario",
#       "Type": "positive | negative | edge",
#       "Preconditions": "System and user state before running test",
#       "Steps": "Step-by-step actions to execute",
#       "Expected Results": "Expected system behavior after execution",
#       "Priority": "Low | Medium | High",
#       "TestData": {
#         "Inputs": {"field1": "value", "field2": "value"},
#         "API_Payload": {"json_key": "value"},
#         "DB_Mock": {"table": "value"}
#       }
#     }
#   ],
#   "selenium_scripts": {test_case_id: "CXXXX[numeric]",// Link this script to its matching test case.
#     "script": "Java Selenium test code string here" // Java code block.
#     }
#   }
# }
# """

JSON_FORMAT = """
{
  "test_cases": [
    {
      "ID": "CXXXX[numeric]",
      "Title": "Short title of the scenario",
      "Type": "positive | negative | edge",
      "Preconditions": "System and user state before running test",
      "Steps": "Step-by-step actions to execute",
      "Expected Results": "Expected system behavior after execution",
      "Priority": "Low | Medium | High",
      "TestData": {
        "Inputs": {"field1": "value", "field2": "value"},
        "API_Payload": {"json_key": "value"},
        "DB_Mock": {"table": "value"}
      }
    }
  ],
  "automation_scripts": {
    "CXXXX[numeric]": {
      "framework": "java_selenium | js_testcomplete | python_selenium | js_playwright",
      "script": ["code line 1", "code line 2", "..."]
    }
  }
}
"""
