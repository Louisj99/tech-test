# Midnite Jr Engineer Take Home Test

## Introduction
 As a base I pull the skeleton from the repo given in the instructions <br>
 This test was a decent challenge for me as I've never really gone indepth with APIs in python before due to me only having professional experience with golang <br>
 but once I got going I realised it's the exact same process as go just with a different language.

## How to run
I have included a requirements.txt file to make it easier to install the required packages <br>

```bash
pip install -r requirements.txt
```
Then to run the program you can use the following command
```bash
make run
```

And finally to run the tests you can use the following command
```bash 
make test
```
additionally you can run the tests with coverage using the following command
```bash
 coverage run -m pytest && coverage report -m
```
There is an explanation of the testing that i did within the api_test.py file <br>
It also has a comment with the result of the coverage when I ran it

## Challenges
My main challenge was that I wrote this API as I would write a go API in terms of logic. <br>
This is why I have used data classes for the request and return to simulate structs in go. I'm not entirely sure if this is the correct or most practical way to do this in python but for me, it made the most sense. <br>
Additionally I also moved most of the logic out of the main API function into their own functions. normally I would have moved them all into their own file but due to the size of the task I decided it would be easier for whoever reviews it, that it all be in the same file. <br>
The other challenge I faced was actually getting python to work in terms of imports. Most of my googling time was spent on how to upgrade my version from 3.10 and how to set up a virtual environment so that pycharm would use the same instance of python that was running in terminal. <br>
lastly I was somewhat confused by the final alert and the timings. I took it that the time int was the time as seconds but if I was to do this as a real production level piece I would have used real time and then use the seconds from that.
## Conclusions 
I found the logic quite easy to understand and I learnt the syntax quite quickly and overall quite enjoyed the task.<br>
I was able to learn quite a bit, and it really made me realise that once you know how to do something in one language it easily transfers over with a bit of googling for the syntax.<br>
I also really enjoyed the testing in python, it is probably the easiest and cleanest testing suite that I have used It was just very simple and nice to write.