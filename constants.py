msg = [
            {
            "role": "user",
            "content": "Respond only with a valid command prompt commands. Do not include the prompt symbol (e.g. >, $, etc.) or preamble. Only the command."
            },
            {
                "role": "user",
                "content": "example: create a new file called example.txt with content 'This is the content of the file.' responds with 'echo. This is the content of the file. > example.txt'"
            },
            {
                "role": "user",
                "content": "example: Retrieves the IP configuration details for all network interfaces and then pings the 'google.com' website to check network connectivity. ipconfig /all && ping google.com"
            },
            {
                "role": "user",
                "content": "Lists all files and directories within the 'C:\Windows' directory and its subdirectories and saves the output to a file named 'files.txt'. dir C:\Windows /s /b > files.txt "
            },
            {
                "role": "user",
                "content": "Retrieves a list of all running processes (tasklist) and filters the output to only display the processes containing the text 'chrome.exe', typically showing running instances of Google Chrome. tasklist | findstr 'chrome.exe'"
            },
            {
                "role": "user",
                "content": """ Here are some more examples
                    1. Command: `ls`
                    Error: `'ls' is not recognized as an internal or external command, operable program or batch file.`
                    Correct Version: `dir`

                    2. Command: `mv file.txt /new_directory`
                    Error: `'mv' is not recognized as an internal or external command, operable program or batch file.`
                    Correct Version: `move file.txt /new_directory`

                    3. Command: `cp file.txt /new_directory`
                    Error: `'cp' is not recognized as an internal or external command, operable program or batch file.`
                    Correct Version: `copy file.txt /new_directory`

                    4. Command: `cd..`
                    Error: `The system cannot find the path specified.`
                    Correct Version: `cd ..` (space between `cd` and `..`)

                    5. Command: `rd directory`
                    Error: `The directory is not empty.`
                    Correct Version: `rmdir directory /s` (removes the directory and its contents)

                    6. Command: `cat file.txt`
                    Error: `'cat' is not recognized as an internal or external command, operable program or batch file.`
                    Correct Version: `type file.txt`

                    7. Command: `grep "pattern" file.txt`
                    Error: `'grep' is not recognized as an internal or external command, operable program or batch file.`
                    Correct Version: `findstr "pattern" file.txt`

                    8. Command: `ping google.com`
                    Error: `'ping' is not recognized as an internal or external command, operable program or batch file.`
                    Correct Version: `ping www.google.com`

                    9. Command: `chmod +x script.sh`
                    Error: `'chmod' is not recognized as an internal or external command, operable program or batch file.`
                    Correct Version: No equivalent in Windows Command Prompt (use PowerShell instead)

                    10. Command: `ls -l`
                        Error: `'ls' is not recognized as an internal or external command, operable program or batch file.`
                        Correct Version: `dir /b` (lists files and directories in bare format)
                    """
            },
            {
                "role": "user",
                "content": "Only respond with valid window command prompt commands."
            }
        ]