import tkinter as tk
import subprocess
import os
import gpt
from colorama import init, Fore
import constants
username = os.getenv('USERNAME')

chat_history = constants.msg
last_10_commands = []
full_chat_history = []

def is_valid_command(command):
    process = subprocess.run(command + " /?", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.stdout.decode().lower()
    error = process.stderr.decode().lower()

    # Check for common error messages
    if "is not recognized as an internal or external command" in error:
        return False
    elif "syntax of the command is incorrect" in error:
        return False
    else:
        return True
    
def trim_object_length(obj, max_length=800):
    if len(obj) == 0:
        return obj
    
    total_length = sum(len(str(item)) for item in obj)
    
    while total_length > max_length:
        item = obj.pop(0)  # Remove the first element from the object
        total_length -= len(str(item))
        print('popped top element from object')
    
    return obj

def display_file_structure(path='C:\\'):
    full_file_structure = ''
    for root, directories, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * level
        full_file_structure += indent + os.path.basename(root) + ', '
        print(f"{indent}[{os.path.basename(root)}]")
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            full_file_structure += sub_indent + file + ', '
            print(f"{sub_indent}{file}")

# Provide the desired root directory

# Display the file structure starting from the root directory
# display_file_structure()
    
def execute_command():
    global full_chat_history

    base = str(os.getcwd()) + ': '
    command = input_text.get("1.0", tk.END).strip()
    if command:
        # Record all user input
        full_chat_history.append({"role": "user", "content": command})
        full_chat_history = trim_object_length(full_chat_history)
        try:
            # Special handling for 'cd' commands
            if command.startswith("cd "):
                new_dir = command[3:].strip()  # Extract the directory path from the command
                os.chdir(new_dir)  # Change the current directory
                base = str(os.getcwd()) + ': '
            
            if command.startswith("explain"):
                status_code, ex_response = gpt.generate_response(full_chat_history)
                if status_code != 200:
                    output_text.insert(tk.END, ex_response + "\n")
                    input_text.delete("1.0", tk.END)
                    return
                  # Record gpt response
                output_text.config(state="normal") 
                output_text.insert(tk.END, ex_response + "\n")

            # No more than 10 last commands
            if len(last_10_commands) >= 10:
                last_10_commands.pop(0)

            last_10_commands.append({"role": "user", "content": command})
            # Validate if it is a valid command
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_text.config(state="normal")  # Enable editing of the output text
            output_text.insert(tk.END, base, "base")  # Display 'base' with custom tag
            output_text.insert(tk.END, command + "\n")  # Display command in command history
            output, error = process.communicate()

            if len(error) > 0:
                last_10_commands.append({
                    "role": "user",
                    "content": command
                })
                last_10_commands.append({
                    "role": "user",
                    "content": "Only respond with valid window command prompt commands."
                })
                gpt_history = chat_history + last_10_commands
                status_code, response = gpt.generate_response(gpt_history)
                if status_code != 200:
                    output_text.insert(tk.END, response + "\n")
                    input_text.delete("1.0", tk.END)
                    return
                full_chat_history.append({"role": "assistant", "content": response})
                # Extract the first word from the response
                first_word = response.split(' ')[0]
                # Validate the command
                if is_valid_command(first_word):
                    if response.startswith("cd "):
                        new_dir = response[3:].strip()  # Extract the directory path from the command
                        os.chdir(new_dir)  # Change the current directory
                        base = str(os.getcwd()) + ': '

                    last_10_commands.append({"role": "assistant", "content": response})
                    output_text.insert(tk.END, "Corrected: " + response + "\n")
                    try:
                        # Run the command and capture the output
                        process = subprocess.Popen(response, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        output, error = process.communicate()
                        output_text.insert(tk.END, output.decode() + error.decode() + "\n")
                        input_text.delete("1.0", tk.END)
                        full_chat_history.append({"role": "system", "content": output.decode() + error.decode()})

                    except subprocess.CalledProcessError as e:
                        # Error occurred, display error message
                        output_text.insert(tk.END, f"Error: {e.output.decode()}\n")
                        input_text.delete("1.0", tk.END)
                        full_chat_history.append({"role": "system", "content": e.output.decode()})
                else:
                    output_text.insert(tk.END, "Could not find a valid command for this, I came up with: \n" + response + "\n However this is incorrect. \n")
                    input_text.delete("1.0", tk.END)
                    full_chat_history.append({"role": "system", "content": "Could not find a valid command for this, I came up with: \n" + response + "\n However this is incorrect. \n"})
            else:
                output_text.insert(tk.END, output.decode() + error.decode() + "\n")
                input_text.delete("1.0", tk.END)  # Clear the input text
                full_chat_history.append({"role": "system", "content": output.decode() + error.decode()})

            
        except subprocess.CalledProcessError as e:
            output_text.insert(tk.END, f"Error: {e.output.decode()}\n")
            full_chat_history.append({"role": "system", "content": e.output.decode()})

            
        finally:
            output_text.config(state="disabled")  # Disable editing of the output text
        
        output_text.insert(tk.END, "\n")
        output_text.see(tk.END)  # Scroll to the end of the output text


root = tk.Tk()
root.title("Copilot Command")
root.configure(bg="#333333")  # Set background color

# Create output text widget
output_text = tk.Text(root, height=20, width=80, bg="#222222", fg="#FFFFFF", font=("Arial", 12))  # Set background, foreground, and font
output_text.pack(fill=tk.BOTH, expand=True)  # Fill and expand to fit the window

output_text.tag_configure("welcome", foreground="#FFD700", font=("Arial", 12, "bold"))
output_text.tag_configure("username", foreground="#00FF00", font=("Arial", 12, "bold"))
output_text.tag_configure("instructions", foreground="#FFFFFF", font=("Arial", 12))

welcome_msg = f"Welcome {username}, to your Copilot Command Station! \nExplain or enter your commands and I'll do the rest!\n\n"
output_text.insert(tk.END, welcome_msg)
output_text.tag_add("welcome", "1.0", "1.7")
output_text.tag_add("username", f"1.8", f"1.{8+len(username)}")
output_text.tag_add("instructions", f"1.{9+len(username)}", "3.0")

output_text.config(state="disabled")  # Set the initial state to disabled
output_text.tag_configure("base", font=("Arial", 12, "bold"), foreground="#FFD700")  # Configure 'base' tag
output_text.tag_configure("suggested", foreground="#00FF00")  # Configure 'suggested' tag with green color

# Create input text widget
input_text = tk.Text(root, height=1, width=80, bg="#444444", fg="#FFFFFF", font=("Arial", 12))  # Set background, foreground, and font
input_text.pack(fill=tk.X)  # Fill horizontally

# Bind the Enter key to execute_command
root.bind('<Return>', lambda event: execute_command())

root.mainloop()
