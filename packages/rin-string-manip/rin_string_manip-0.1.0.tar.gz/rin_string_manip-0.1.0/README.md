Perform string manipulation operations using a single command.<br>
<h1>Usage</h1>
run the following command

```bash
ring-string-manip --OPTIONS
```
OPTIONS that can be provided are:

```commandline
config-path: path/to/config.yaml
file-path: path/to/file.txt
```
<hr>
<h2>Config file format</h2>
Ensure your config/yaml file follows the following format:

```yaml
pipline:
  - func1
  - func2
  - func3 
```
Default sequence is (if no path is provided)
```yaml
pipeline:
  - remove_stop_words
  - coalesce_spaces
  - stair_case
  - append_date
  - prepend_number
```
Refer below for available functions.
<hr>
<h1>Functions available</h1>
<h3>remove_stop_words</h3>
Removes stop_words from given string. Default stop_words are

```yaml
stopwords:
  - A
  - The
  - An
  - Is
  - For
  - It
  - Our
  - We
  - They
  - Their
```
<h3>coalesce_spaces</h3>
Converts multiple spaces into one space
<br>

<h3>stair_case</h3>
Converts first letter upper, second lower, third upper and so on.
<br>

<h3>prepend_number</h3>
Adds numbers to the lines. Here, the line number is prepended.
<br>

<h3>append_date</h3>
Appends the date+time at the end of the string.