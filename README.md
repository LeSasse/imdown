# imdown

imdown (pronouce "I'm down") can be used to collect images from a directory
tree and put them into a markdown file for markdown to compile to another format
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


# use

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

You can then manually adjust the markdown file and compile via pandoc.
If you do not need to adjust it and just want the pdf, you can also skip the intermediate markdown file
and pipe it straight into pandoc (of course for this you need pandoc installed!):

```
imdown figures -f pdf | pandoc -o output_pdfs/piped.pdf
```
and see the result in [output_pdfs/piped.pdf](example/output_pdfs/piped.pdf).
