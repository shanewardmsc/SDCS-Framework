from colorama import init, Fore

# Alarm colour configuration
alm_colour = Fore.RED
alm_rst = Fore.RESET
init(convert=True)

# Create Dockerfile
def write_dockerfile(filename, string):
    try:
        with open(filename, "a") as f:
            write_string = ''.join(string)
            f.write(write_string)

        f.close()
    except IOError as error:
        print("Error: Cannot open file", str(error))
        return
    except Exception as error:
        print("Error: General exception occurred: ", str(error))
        return