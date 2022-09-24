
# download file 
curl -o /dev/null -s -w "%{http_code}\n" --location --request GET 'http://127.0.0.1:5000/download/testfile1.txt' --form 'username="test1"' 
curl -o /dev/null -s -w "%{http_code}\n" --location --request GET 'http://127.0.0.1:5000/download/testfile2.txt' --form 'username="test1"'
curl -o /dev/null -s -w "%{http_code}\n" --location --request GET 'http://127.0.0.1:5000/download/testfile3.txt' --form 'username="test1"'

# delete file
curl --location --request DELETE 'http://127.0.0.1:5000/delete/testfile1.txt' --form 'username="test1"'
curl --location --request DELETE 'http://127.0.0.1:5000/delete/testfile2.txt' --form 'username="test1"'
curl --location --request DELETE 'http://127.0.0.1:5000/delete/testfile3.txt' --form 'username="test1"'