---
title: Using Excel with Apache NiFi to make user data exchanges easier
---

It's very common in many situations for data engineers and others working with an organization's data to run into one or more situations where the data is delivered by people who just load it up in a spreadsheet and send it over. In most cases, they don't know better and also don't have any tools that make the process better for them either. They're just doing the best they can with what they know and are given.

Fortunately, NiFi is more than capable of handling these users and use cases thanks to the `ConvertExcelToCsv` processor. It can even maintain the formatting of Excel cells to a degree, such as converting the internal representation of a date to whatever string format was specified for its formatting.

If you find yourself in a situation like this, these are some things to explain to the users that will make it much easier for them to work with you.

### Use Descriptive, Non-Duplicated Headers

The first line of a good Excel document that can be easily adapted should be a header line with no gaps between the fields, and each column header should be a good and descriptive name. There's no need to abbreviate. "First Name" and "FirstName" are fine for a person's first name, no need to keep it short like "fname."

It's important to also let them know that if they duplicate a header name, you won't be able to easily make it work for them. What you'll have to do is intercept the CSV output from `ConvertExcelToCsv` and rewrite the header line. This is one of the reasons why descriptive headers are better; descriptive headers are less likely to be duplicated.

### Do Not Explain The Data

Explanatory notes about the data should never be in the document, be it in a cell or a column header. If explanation is needed, just communicate it separately. Tell them that you appreciate them trying to clarify things, but the notes will just be confused for bad records.

### When In Doubt, Leave It Blank

If a field is nullable in your schema or has a good default value, encourage users to just leave the field blank when they are manually building or converting the data. It's better for them to not type anything at all in such cases, especially when they might get the value wrong (ex. typing `NA` instead of `N/A` when `N/A` is the required value for that situation).

The ultimate goal is to encourage them to give you a data set that can be easily converted into a CSV file, which can in turn be used by the Record API.

Excel, done right, can be a great format for receiving data from less technically-skilled teams and organizations. It's really not that difficult to educate such users on how to build a simple data set that lets them just fire an email and walk away. Often it's just copying and pasting data in a tool they already know. It can even be an effective way for organizations to bypass uncooperative IT departments that might scoff at NiFi reaching into departmental databases, setting up message queues, etc. 