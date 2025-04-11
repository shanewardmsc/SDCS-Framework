from colorama import init, Fore

# Console output colour configuration
splash_colour = Fore.YELLOW
title_colour = Fore.LIGHTBLUE_EX
query_colour = Fore.GREEN
fore_rst = Fore.RESET
aws_colour = Fore.YELLOW
alm_colour = Fore.RED
alm_rst = Fore.RESET
init(convert=True)


# -------------------------------------------------------#
#            Docker Application Splash Screen            #
# -------------------------------------------------------#
class SplashScreen:
    def __init__(self):
        self.splash_screen = splash_colour + \
                             " ----------------------------------------------------------------\n" \
                             "|                        Docker & Kubernetes                     |\n" \
                             "|                  Cloud Services Automation Tool                |\n" \
                             "|      To close this application at any time, enter: 'exit'      |\n" \
                             "|                                                                |\n" \
                             " ----------------------------------------------------------------\n\n" \
                             + fore_rst

    def load_splash_screen(self):
        print(self.splash_screen)
        return self.splash_screen


# -------------------------------------------------------#
#                 Main Login/Register Menu               #
# -------------------------------------------------------#
class MainPrompt:
    def __init__(self):
        pass

    def prompt(self):
        try:
            user_input = input("\n"
                               + title_colour +
                               "MAIN PROMPT:\n"
                               + fore_rst +
                               "For Docker, please enter 'D'              \n"
                               "For Kubernetes, please enter 'K'          \n"
                               "To close the Application, please enter 'exit': ")

            return user_input

        except ValueError as error:
            print(alm_colour + "Error: menu_utils() Invalid entry detected: " + str(error) + alm_rst)
            return
        except KeyboardInterrupt as error:
            print(alm_colour + "Error: menu_utils() Keyboard interrupt detected: " + str(error) + alm_rst)
            return
        except OSError as error:
            print(alm_colour + "Error: menu_utils() OS str(error) occurred: " + str(error) + alm_rst)
            return
        except Exception as error:
            print(alm_colour + "Error: menu_utils() General exception occurred: " + str(error) + alm_rst)
            return


# -------------------------------------------------------#
#               Docker Main Navigation Menu              #
# -------------------------------------------------------#
class MainMenu:
    def __init__(self):
        pass

    def docker_menu(self):
        try:
            menu_input = input("\n"
                               + aws_colour +
                               "        DOCKER MAIN MENU\n"
                               + fore_rst +
                               "        Select one of the below Docker Service options:\n"
                               "        - List all containers:                      enter '1'                 \n"
                               "        - List all stopped/exited containers:       enter '2'                 \n"
                               "        - Run container:                            enter '3'                 \n"
                               "        - Execute command on running container:     enter '4'                 \n"
                               "        - View port mappings for a container:       enter '5'                 \n"
                               "        - Stop and remove all containers:           enter '6'                 \n"
                               "        - Save an image to a tar file:              enter '7'                 \n"
                               "        - Create dockerfile and run a container:    enter '8'                 \n"
                               "        - Run pre-defined scenario:                 enter '9'                 \n"
                               "        - Back to Main Menu:                        enter 'b'                 \n"
                               "        - Exit Application:                         enter 'exit': ")

            return menu_input

        except ValueError as error:
            print(alm_colour + "Error: menu_utils() Invalid entry detected: " + str(error) + alm_rst)
            return
        except KeyboardInterrupt as error:
            print(alm_colour + "Error: menu_utils() Keyboard interrupt detected: " + str(error) + alm_rst)
            return
        except OSError as error:
            print(alm_colour + "Error: menu_utils() OS str(error) occurred: " + str(error) + alm_rst)
            return
        except Exception as error:
            print(alm_colour + "Error: menu_utils() General exception occurred: " + str(error) + alm_rst)
            return

    def kubernetes_menu(self):
        try:
            menu_input = input("\n"
                               + aws_colour +
                               "        KUBERNETES MAIN MENU\n"
                               + fore_rst +
                               "        Select one of the below Kubernetes Service options:\n"
                               "        - List all pods:                                   enter '1'                 \n"
                               "        - Describe a pod:                                  enter '2'                 \n"
                               "        - Create deployment with 2 pods:                   enter '3'                 \n"
                               "        - Scale number of pods from menu option 3:         enter '4'                 \n"
                               "        - Execute a command on pod:                        enter '5'                 \n"
                               "        - Perform a rolling update on deployment of pods:  enter '6'                 \n"
                               "        - Delete a deployment:                             enter '7'                 \n"
                               "        - Create a pod on every worker node:               enter '8'                 \n"
                               "        - Run pre-defined scenario:                        enter '9'                 \n"
                               "        - Back to Main Menu:                               enter 'b'                 \n"
                               "        - Exit Application:                                enter 'exit': ")

            return menu_input

        except ValueError as error:
            print(alm_colour + "Error: menu_utils() Invalid entry detected: " + str(error) + alm_rst)
            return
        except KeyboardInterrupt as error:
            print(alm_colour + "Error: menu_utils() Keyboard interrupt detected: " + str(error) + alm_rst)
            return
        except OSError as error:
            print(alm_colour + "Error: menu_utils() OS str(error) occurred: " + str(error) + alm_rst)
            return
        except Exception as error:
            print(alm_colour + "Error: menu_utils() General exception occurred: " + str(error) + alm_rst)
            return
