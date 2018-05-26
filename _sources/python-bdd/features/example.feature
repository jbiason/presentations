Feature: Testing passwords

	Scenario: Invalid password
		Given that I have a username foo
		  And that I have a password test123
		 When I try to create an user
		 Then I should get an error of invalid password
