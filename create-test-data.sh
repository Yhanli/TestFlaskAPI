#  create user
curl --location --request POST 'http://127.0.0.1:5000/create_user' --form 'username="test1"' --form 'customer="testCust"'
curl --location --request POST 'http://127.0.0.1:5000/create_user' --form 'username="test2"' --form 'customer="testCust"'
curl --location --request POST 'http://127.0.0.1:5000/create_user' --form 'username="test3"' --form 'customer="otherTestCust"'

#  upload file
curl --location --request PUT 'http://127.0.0.1:5000/upload' --form '=@"API/fakeFiles/testfile1.txt"' --form 'username="test1"'
curl --location --request PUT 'http://127.0.0.1:5000/upload' --form '=@"API/fakeFiles/testfile2.txt"' --form 'username="test2"'
curl --location --request PUT 'http://127.0.0.1:5000/upload' --form '=@"API/fakeFiles/testfile3.txt"' --form 'username="test3"'
