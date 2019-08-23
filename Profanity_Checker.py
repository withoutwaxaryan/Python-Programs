import urllib.request
from urllib.parse import quote_plus
    

def read_text():
    #Add the location of the file in the line below to check for 'Cuss' Words
    quotes = open("/home/aryan/movie_quotes.txt")
    contents_of_file=quotes.read()
    print(contents_of_file)
    quotes.close()
    check_profanity(contents_of_file)

def check_profanity(contents_of_file):

     encoded_contents_of_file = quote_plus(contents_of_file)
     #Below Site is what do you like by Google -> Checks Curse words!!
     url = "http://www.wdylike.appspot.com/?q=" + encoded_contents_of_file
     connection = urllib.request.urlopen(url)
     output = connection.read()
     #print(output)
     connection.close()
     if b"true" in output:
         print("Profanity Alert!!")
     elif b"false" in output:
         print("No curse words")
     else :
         print("Could not scan the document properly")
    

read_text()
