# imdown

imdown (pronounce "I'm down") can be used to collect images from a directory
tree and put them into a markdown file for markdown to compile to another format
using [pandoc](https://pandoc.org/)
(although I typically use pdf's so its targeted at that mainly.)

# install

Install from PyPI:
```
pip install imdown
```
or from GitHub:
```
pip install git+https://github.com/LeSasse/imdown.git
```


# Write new files

## Try out the example

You can try it out on the example provided in this repository. Go to the `example`
directory:

```
git clone https://github.com/LeSasse/imdown.git
cd imdown/example
```

Collect all images from the `figures` directory and put them into a markdown file:

```
imdown figures -o markdown_files/all_filetypes.md
```
and see the result in [markdown_files/all_filetypes.md](example/markdown_files/all_filetypes.md).
Or filter out a specific filetype only i.e. pdf's:

```
imdown figures -f pdf -o markdown_files/only_pdfs.md
```

You can then manually adjust the markdown file and compile via [pandoc](https://pandoc.org/).
If you do not need to adjust it and just want the pdf, you can also skip the intermediate markdown file
and pipe it straight into pandoc (of course for this you need [pandoc](https://pandoc.org/) installed!):

```
imdown figures -f pdf | pandoc -o output_pdfs/piped.pdf
```
and see the result in [output_pdfs/piped.pdf](example/output_pdfs/piped.pdf).

## Adjust the paths written in the markdown output

By default `imdown` will write all the paths relative to the directory
in which the markdown file will be written (or from current directory if the
markdown is just printed to stdout). However, you may not always like to build
your final output format from the same directory as the markdown file, so you
can specifiy `-b, --build_directory`, so that all paths will be written relative
from this directory:

```
imdown figures -b . -o markdown_files/build_directory_specified.md
```

Check the result in [markdown_files/build_directory_specified.md](example/markdown_files/build_directory_specified.md)
and you can see that the paths are relative not from the md file but from the
directory you specified (i.e. the current directory). Note that of course the
example in the repository is therefore not able to show the pictures in that
particular md file. Alternatively, you can also simply use the `-a, --absolute`
flag to write all paths as absolute paths.

## Ignore paths or filenames based on a string

You can pass a string to the `-i, --ignore` flag. If any of the paths/filenames
of the images include this string, it will be ignored.
For example:
```
imdown figures -i analysis1
```
will result in:

```
![figures/analysis2/fig5.pdf](figures/analysis2/fig5.pdf)

![figures/analysis2/fig4.pdf](figures/analysis2/fig4.pdf)

![figures/analysis2/fig5.png](figures/analysis2/fig5.png)

![figures/analysis3/fig7.pdf](figures/analysis3/fig7.pdf)

![figures/analysis3/fig6.png](figures/analysis3/fig6.png)

![figures/analysis3/fig9.pdf](figures/analysis3/fig9.pdf)

![figures/analysis3/fig8.pdf](figures/analysis3/fig8.pdf)

![figures/analysis3/fig10.pdf](figures/analysis3/fig10.pdf)
```

You can also ignore multiple strings, i.e.
```
imdown figures -f pdf png -i analysis1 analysis2
```
will result in:

```
![figures/analysis3/fig7.pdf](figures/analysis3/fig7.pdf)

![figures/analysis3/fig6.png](figures/analysis3/fig6.png)

![figures/analysis3/fig9.pdf](figures/analysis3/fig9.pdf)

![figures/analysis3/fig8.pdf](figures/analysis3/fig8.pdf)

![figures/analysis3/fig10.pdf](figures/analysis3/fig10.pdf)
```

## Walk only to a certain depth

You can specify how many levels the program should walk the directory tree.
If None (default) the program will walk all the way. Specify 0 to only consider
files in the initial directory. For each level deeper add +1.
For example:

```
imdown figures -f pdf png -d 0
```
will output nothing, as there are no files in the initial directory.
However, specifiying one level will be enough to give the same output as the default
in this case, as the program will go one level deeper (but there are no levels beyond
this in the example).
```
imdown figures -f pdf png -d 1
```

# Update manually adjusted markdowns

Now imagine that you manually adjusted captions or text in one of the markdown files.
But you also added new plots to your directory and want to add them to you markdown or you want to include filetypes
that you did not include previously.

For example consider [markdown_files/manually_adjusted.md](example/markdown_files/manually_adjusted.md).
This is the markdown that I created only using pdf plots. I now also want to add all
png's. I have adjusted the captions and added some text and of course I do not want to lose that text when
adding new plots. In order to do this I can provide the adjusted file as a reference file as an 
additional argument and add only the new plots. For example I can test it and print the
updated version to stdout:

```
imdown figures -f pdf png -r markdown_files/manually_adjusted.md
```

which should output:

```markdown
![This is a new caption](figures/analysis1/fig2.pdf)

I have also added some text.

![figures/analysis2/fig5.pdf](figures/analysis2/fig5.pdf)

![figures/analysis2/fig4.pdf](figures/analysis2/fig4.pdf)

![figures/analysis3/fig7.pdf](figures/analysis3/fig7.pdf)

![figures/analysis3/fig9.pdf](figures/analysis3/fig9.pdf)

![figures/analysis3/fig8.pdf](figures/analysis3/fig8.pdf)

![figures/analysis3/fig10.pdf](figures/analysis3/fig10.pdf)

![figures/analysis1/fig3.png](figures/analysis1/fig3.png)

![figures/analysis1/fig1.png](figures/analysis1/fig1.png)

![figures/analysis2/fig5.png](figures/analysis2/fig5.png)

![figures/analysis3/fig6.png](figures/analysis3/fig6.png)

```

Note that this outputs all paths as relative to the current directory, since
you are printing to stdout. The advantage is that the old paths aren't just valid
from the reference file, but you can also write it to a new file, in which case
paths will be written relative from that file:

```
imdown figures -f pdf png -o markdown_files/manually_adjusted_and_updated.md -r markdown_files/manually_adjusted.md
```
for which you can find the result in [markdown_files/manually_adjusted_and_updated.md](example/markdown_files/manually_adjusted_and_updated).

Of course you can also overwrite the reference file, but do that at your own risk.
Another advantage of this is, that you can take the reference file, update it with the 
new plots, and pipe it straight into pandoc again, if you like:

```
imdown figures -f pdf png -r markdown_files/manually_adjusted.md | pandoc -o output_pdfs/piped_from_reference.pdf
```
You can see the result at [output_pdfs/piped_from_reference.pdf](example/output_pdfs/piped_from_reference.pdf)
