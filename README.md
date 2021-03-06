<h1 align="center">timew distribution 📈</h1>

<p align="center">
    <img src='https://github.com/tom-doerr/bins/raw/main/timew_distribution/td1.gif'>
    <p align="center">
    </p>
</p>

This plugin plots the time you spent on a tag as a histogram.
The location of the last item you tracked is marked with a red square in the plot.

Instead of typing `timew distribution ...` you can also type `timew dist ...` or `timew dis ...`.


## Installation
Install the `termplotlib` library using
```
pip3 install termplotlib
```

Then you just need to copy the file `distribution.py` into your timewarrior extension folder.
```bash
git clone git@github.com:tom-doerr/timew_distribution.git
cp timew_distribution/distribution.py ~/.timewarrior/extensions/
```

## Plotting for the current tags
To plot the distribution for the currently tracked tags, you can run
```
timew dist $(timew | awk 'NR==1 {$1=""; print $0}')
```
## Plot when done tracking
Plot every time the timewarrior data is modified:
```
while inotifywait -e modify ~/.timewarrior/data; do
        timew dist $(timew | awk 'NR==1 {$1=""; print $0}')
done
```
