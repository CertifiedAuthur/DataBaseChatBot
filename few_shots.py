few_shots = [
    {
        'Question': "What is the total number of test cases executed on Sunday?",
        'SQLQuery': "SELECT COUNT(*) FROM cleaned_data WHERE weekday = 'Sunday'",
        'SQLResult': "Result of the SQL query",
        'Answer': "311"
    },
    {
        'Question': "How many test cases have the precondition set to 'NONE'?",
        'SQLQuery': "SELECT COUNT(*) FROM cleaned_data WHERE Precondition = 'NONE'",
        'SQLResult': "Result of the SQL query",
        'Answer': "2106"
    },
   
    {
        'Question': "How many test cases were executed in the year 2024?",
        'SQLQuery': "SELECT COUNT(*) FROM cleaned_data WHERE year = '2024'",
        'SQLResult': "Result of the SQL query",
        'Answer': '451'
    },
    {
        'Question': "What is the average execution time for test cases in March?",
        'SQLQuery': "SELECT AVG(CAST(executionTimestamp AS INTEGER)) FROM cleaned_data WHERE month = 'March'",
        'SQLResult': "Result of the SQL query",
        'Answer': 'None'
    },
    {
        'Question': "Which test suites were executed on Wednesday?",
        'SQLQuery': "SELECT DISTINCT testSuiteName FROM cleaned_data WHERE weekday = 'Wednesday'",
        'SQLResult': "Result of the SQL query",
        'Answer': "'ProjectA', 'ProjectF', 'ProjectD', 'ProjectH', 'ProjectB', 'ProjectG', 'ProjectC', 'ProjectE', 'DemoCase_ecuSleepTest'"
    },
    {
        'Question': "How many test cases failed due to errors?",
        'SQLQuery': "SELECT COUNT(*) FROM cleaned_data WHERE failed_step_ERROR IS NOT NULL",
        'SQLResult': "Result of the SQL query",
        'Answer': '2429'  
    },
    {
        'Question': "How many test cases were executed with a setup verdict of 'PASS'?",
        'SQLQuery': "SELECT COUNT(*) FROM cleaned_data WHERE test_steps_setup_verdict = 'PASSED'",
        'SQLResult': "Result of the SQL query",
        'Answer': "0"
    },
    {
        'Question': "What is the distribution of test case verdicts?",
        'SQLQuery': "SELECT verdict, COUNT(*) FROM cleaned_data GROUP BY verdict",
        'SQLResult': "Result of the SQL query",
        'Answer': "('ERROR', 345), ('FAILED', 373), ('INCONCLUSIVE', 112), ('NONE', 40), ('PASSED', 1559)"}
]