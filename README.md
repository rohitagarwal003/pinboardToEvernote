Pinboard To Evernote
====================
About
-----
Archive the content of your pinboard bookmarks as notes in your evernote account.

Motivation
----------
I really love Pinboard. It is very fast and gets out of the way quickly. But if you don't pay for an annual archival account, then search is rather hit-or-miss. If you don't remember part of the title or the url, then good luck finding the bookmark you are looking for. So, I created this utility which stores the content of your pinboard bookmarks in your evernote account. Consider this a poor man's version of Pinboard archival account.

Prerequisites
-------------
* Install [PyTidyLib](http://countergram.com/open-source/pytidylib/docs/index.html) `sudo easy_install pytidylib`
* Fill the `credentials.py` file:
  * You can find your Pinboard API token on your https://pinboard.in/settings/password page
  * You can get a free Diffbot Developer Token from http://www.diffbot.com/plans/free
  * You can get a developer token that allows you to access your own Evernote account from:
      * https://sandbox.evernote.com/api/DeveloperToken.action (if you want to store notes in a test account at https://sandbox.evernote.com You will need to create a test account first.)
      * https://www.evernote.com/api/DeveloperToken.action (if you want to store notes in your main account at https://www.evernote.com)

Tested on Python 2.7

Usage
-----
```
main.py [-h] [-s] [-n NOTEBOOK]

optional arguments:
  -h, --help            show this help message and exit
  -s, --sandbox         Store notes in a test account at sandbox.evernote.com
                        instead of your main account at www.evernote.com. Use
                        this option when you are testing the utility.
  -n NOTEBOOK, --notebook-name NOTEBOOK
                        Store the bookmarks in the notebook named NOTEBOOK. If
                        no notebook is specified then bookmarks are stored in
                        the default notebook. If NOTEBOOK doesn't exist, then
                        bookmarks are stored in the default notebook.
```

Comments
--------
* If you want to test the utility:
  * Create a test account at https://sandbox.evernote.com
  * Fill the `credentials.py` file.
  * Create a file named `lastUpdate.txt` in the project directory and enter a recent date and time like this `2012-10-20T10:20:30Z`.
  * Run `main.py -s`
  * This will store the content of your Pinboard bookmarks created after `2012-10-20T10:20:30Z` in your test account at https://sandbox.evernote.com
* If you are satisfied with the results:
  * Delete the `lastUpdate.txt` file you created earlier.
  * Change your EvernoteDeveloperToken to the one for your main account at https://www.evernote.com
  * Create a new notebook in your evernote account (if you don't do this the bookmarks will be stored in your default notebook)
  * Run `main.py -n Pinboard` (if the notebook you created was named 'Pinboard')
  * Sit back and relax. The first run may take a lot of time depending on the number of bookmarks you have in your Pinboard account.
  * Either set up a cron job which executes `main.py -n Pinboard` daily. Or execute the script manually after regular intervals.
