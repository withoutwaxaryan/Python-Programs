import time
import webbrowser

total_breaks=3
break_count=0

print("This Program Started on " + time.ctime())

while(break_count < total_breaks):
    time.sleep(2)
    webbrowser.open("https://youtu.be/QXcI6sycTnQ")
    break_count=break_count+1
    
