***************************************
reddit_view, gets links from subreddits
***************************************

# this will out put a list of links to the slideshow file

.. code-block:: bash

    # where list_of_subreddits is a file with a list of subreddits
    $reddit_view -s `cat ~/list_of_subreddits | tr "\n" ","` &> ~/slideshow
    $reddit_view -s `cat ~/bin/list_of_subreddits | tr "\n" ","` -o hot &> ~/slideshow
    $reddit_view -i r -s funny,science,machineporn -o hot,top -p 1 &> ~/slideshow
    
    # to view
    $cat ~/slideshow | xargs feh -D 5 --auto-zoom -g 800x800 -B black
    $cat ~/slideshow | shuf | awk '{ sub(/gifv$/, "gif"); print }' | mplayer -vo xv -playlist -

for more see the programs -h help option
