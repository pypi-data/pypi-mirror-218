#! /usr/bin/python
import os
import json
import sys
import colorama
colorama.init()

from .lib.Argument import Argument
Argument=Argument(sys.argv)

def help():
    print("<FileInfo> [Options].. ")

def main():
    try:
        if Argument.hasOptionValue('-file'):
            if Argument.getoptionvalue('--type') and Argument.getoptionvalue('--option'):
                file_content = json.loads(os.popen('mediainfo --Output=JSON '+Argument.getoptionvalue('-file')).read())
                try:
                    if file_content["media"]["track"]:
                        for track in file_content["media"]["track"]:
                            if(track['@type'] == Argument.getoptionvalue('--type')):
                                option = Argument.getoptionvalue('--option')
                                for i in track.keys():
                                    if option == i:
                                        output = colorama.Fore.GREEN + option + colorama.Fore.BLUE + "  -->  " + colorama.Fore.RED + track[i]
                                        print(output)
                    else:
                        raise Exception( colorama.Fore.RED +  "Unable to fetch the Tracks of your Source file")
                except ValueError as e:
                    print(e)
                    
            elif Argument.getoptionvalue('--type') and (Argument.hasOption(['--list_All_keys']) or Argument.hasOption(['-l'])):
                file_content = json.loads(os.popen('mediainfo --Output=JSON '+Argument.getoptionvalue('-file')).read())
                try:
                    if file_content["media"]["track"]:
                        for track in file_content["media"]["track"]:
                            if(track['@type'] == Argument.getoptionvalue('--type')):
                                for i in track.items():
                                    output = colorama.Fore.GREEN + str(i[0]) + "  -->  " + colorama.Fore.RED + str(i[1])
                                    print(output)
                    else:
                        raise Exception(colorama.Fore.RED +  "Unable to fetch the Tracks of your Source file")
                except ValueError as e:
                    print(e)
                                
            elif Argument.hasOption(['--type']) and (Argument.hasOption(['--help']) or Argument.hasOption(['-h'])):
                file_content = json.loads(os.popen('mediainfo --Output=JSON '+Argument.getoptionvalue('-file')).read())
                try:
                    if file_content["media"]["track"]:
                        for track in file_content["media"]["track"]:
                            tracks = track['@type']
                            if tracks =="General":
                                print(colorama.Fore.GREEN + f"{tracks}" + colorama.Fore.RED +  " ==> "+ colorama.Fore.BLUE +" Show's the Files " +colorama.Fore.GREEN + "General "+ colorama.Fore.BLUE + "properties" )
                            if tracks =="Video":
                                print(colorama.Fore.GREEN + f"{tracks}" + colorama.Fore.RED +  " ==> "+ colorama.Fore.BLUE +" Show's the Files " +colorama.Fore.GREEN + " Video "+ colorama.Fore.BLUE + "properties" )
                            if tracks =="Audio":
                                print(colorama.Fore.GREEN + f"{tracks}" + colorama.Fore.RED +  " ==> "+ colorama.Fore.BLUE +" Show's the Files " +colorama.Fore.GREEN + " Audio "+ colorama.Fore.BLUE + "properties" )
                    else:
                        raise Exception(colorama.Fore.RED +  "Unable to fetch the Tracks of your Source file")
                except ValueError as e:
                    print(e)
                        
                        
            elif Argument.getoptionvalue('--type') and  Argument.hasOption(['--options']):
                file_content = json.loads(os.popen('mediainfo --Output=JSON '+Argument.getoptionvalue('-file')).read())
                try:
                    if file_content["media"]["track"]:
                        for track in file_content["media"]["track"]:
                            if(track['@type'] == Argument.getoptionvalue('--type')):
                                heading = colorama.Fore.BLUE + "Options"
                                heading_def = colorama.Fore.BLUE + "Help Definitions"
                                arrow = " --> " + colorama.Fore.BLUE
                                print(f"{heading : <45}{arrow : ^20}{heading_def :>20}")
                                for i in track:
                                    options = colorama.Fore.GREEN + i
                                    options_help = colorama.Fore.RED + i
                                    arrow = " --> " + colorama.Fore.BLUE
                                    print(f"{options : <45}{arrow : ^20}{options_help :>10} of the Source File")

                    else:
                        raise Exception(colorama.Fore.RED +  "Unable to fetch the Tracks of your Source file")
                except ValueError as e:
                    print(e)

            else:
                print(colorama.Fore.RED + "Please Enter the Type of the Video File...")
                print(colorama.Fore.RED + "or Check your Commands properly...")
        
        else:
            help()
    except:
        help()
            
if __name__ == "__main__":
    main()

        

                            

            
                    
                


            


