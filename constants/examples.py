examples = {
  "test_cases": [
    {
      "ID": "C1001",
      "Title": "Verify Provider Name Field - Valid Input",
      "Type": "positive",
      "Preconditions": "User is logged in and on the 'Supporting Information' page.",
      "Steps": "1. Enter 'Acme Healthcare Inc.' in the 'Provider Name' field.\n2. Submit the form.",
      "Expected Results": "The 'Provider Name' field accepts the input and displays it correctly.",
      "Priority": "High",
      "TestData": {
        "Inputs": { "Provider Name": "Acme Healthcare Inc." },
        "API_Payload": {},
        "DB_Mock": {}
      }
    }
  ],
  "automation_scripts": {
    "C1001": {
      "framework": "java_selenium",
      "script": [
        "// Java Selenium test code for C1001",
        "WebDriver driver = new ChromeDriver();",
        "driver.get(\"https://example.com/supporting-information\");",
        "WebElement providerNameField = driver.findElement(By.id(\"providerName\"));",
        "providerNameField.sendKeys(\"Acme Healthcare Inc.\");",
        "WebElement submitButton = driver.findElement(By.id(\"submitButton\"));",
        "submitButton.click();",
        "WebElement displayedName = driver.findElement(By.id(\"providerName\"));",
        "Assert.assertEquals(displayedName.getAttribute(\"value\"), \"Acme Healthcare Inc.\");",
        "driver.quit();"
      ]
    }
  }
}
