*** Settings ***
Library 	TestingSource.py

*** Test Cases ***
Invalid password
	Given that I have a username	foo
	  And that I have a password	test123
	 When I try to create a user
     Then I should get an error of invalid password

*** Keywords ***
That I have a username 
	[Arguments]		${username}
	set username 	${username}

That I have a password 
	[Arguments]		${password}
	Set password	${password}

I try to create a user
	Create user

I should get an error of invalid password
	Is invalid password
