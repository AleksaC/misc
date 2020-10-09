- Use -E or -r for extended regular expresions (using ?,[] etc.)
- Use -i to edit file in-place
- sed is meant to be used for line-based input (i.e. it reads a line stripping the newline and adds it to pattern space)
- Workaround allowing us to use regexes with newlines:
  - example for regex matching 

    ```yaml
      default_language_version:
        python: python3.8
    ```

    `':a;N;$!ba;s/default_language_version:\n[ \t]+python: \"?python3.8\"?\n\n?//g;'`
  - explanation
    - `:a;N;$!ba;` 
    - `:a` - create the label a
    - `N` - adds newline to pattern space and appends the next line 
    - `$!ba` - branch to the label a if we are before last line (we want to keep the last newline) -- this alows us to loop through the file concatenating the lines
    - `s/default_language_version:\n[ \t]+python: \"?python3.8\"?\n\n?//g` replaces the regex `default_language_version:\n[ \t]+python: \"?python3.8\"?\n\n?` with empty string (runs on previously concatenated pattern space)
    - Reference: https://stackoverflow.com/questions/1251999/how-can-i-replace-a-newline-n-using-sed
  - the pattern above probably only works for GNU sed
