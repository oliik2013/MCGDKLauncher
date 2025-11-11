import os
import platform
import distro
import time
from pathlib import Path

print("MCGDKLauncher 1.0")
distro = distro.id()
print(f"Detected Linux distribution: {distro}")
mainfolder = Path(os.path.expanduser("~/.mcgdklauncher"))
if mainfolder.exists():
    print("What you want to do?")
    print("1. Launch Minecraft GDK")
    print("2. Update WineGDK")
    print("3. Exit")
    choice = input("Enter your choice (1/2/3): ")
    if choice == "1":
        contentfolder = Path(os.path.expanduser("~/.mcgdklauncher/Minecraft/Content"))
        if contentfolder.exists():
            os.system("bash -c \"VKD3D_CONFIG=dxr11,dxr WINEPREFIX=~/.mcgdklauncher/prefix DXVK_ENABLE_NVAPI=1 ~/.mcgdklauncher/WineGDK/build/wine ~/.mcgdklauncher/Minecraft/Content/Minecraft.Windowss.exe\"")
            exit(0)
        else:
            print("Minecraft game files not found in ~/.mcgdklauncher/Minecraft/Content. Please place them there and try again.")
            time.sleep(3)
            exit(1)
    elif choice == "2":
        print("Updating WineGDK...")
        os.system("cd ~/.mcgdklauncher/WineGDK && git fetch && git merge origin/main")
        os.system("cd ~/.mcgdklauncher/build && make -j$(nproc)")
        print("WineGDK updated successfully!")
        time.sleep(2)
        exit(0)
    elif choice == "3":
        print("Exiting...")
        time.sleep(1)
        exit(0)
    else:
        print("Invalid choice, exiting...")
        time.sleep(1)
        exit(1)
else:
    print("First time setup")
    input("Press Enter to start setup...")
    os.system("mkdir ~/.mcgdklauncher")
    print("Downloading and compiling WineGDK and dependencies...")
    time.sleep(2)
    if distro == "arch":
        print("Warning: You probbaly need to enable multilib repository in /etc/pacman.conf and run 'sudo pacman -Syu' before proceeding.")
        time.sleep(3)
        os.system("sudo pacman -S mingw-w64-gcc base-devel git gcc multilib-devel winetricks wine vulkan-icd-loader lib32-vulkan-icd-loader libx11 lib32-libx11 freetype2 lib32-freetype2 mesa lib32-mesa glu lib32-glu alsa-lib lib32-alsa-lib libxrandr lib32-libxrandr libxi lib32-libxi libxext lib32-libxext libxrender lib32-libxrender libxcursor lib32-libxcursor libxinerama lib32-libxinerama libxcomposite lib32-libxcomposite libxfixes lib32-libxfixes libpng lib32-libpng libjpeg-turbo lib32-libjpeg-turbo libtiff lib32-libtiff openal lib32-openal mpg123 lib32-mpg123 sdl2 lib32-sdl2 libxml2 lib32-libxml2 libldap lib32-libldap vulkan-headers cups")
    else:
        print("Warning: Automatic dependency installation is only on Arch. Procedding without installing dependencies.")
        time.sleep(3)

    print("Cloning WineGDK repository...")
    os.system("git clone https://github.com/Weather-OS/WineGDK.git ~/.mcgdklauncher/WineGDK")
    os.system("mkdir ~/.mcgdklauncher/build")
    print("Compiling WineGDK (this may take a while)...")
    time.sleep(2)
    os.system("cd ~/.mcgdklauncher/build && ../WineGDK/configure --enable-win64 && make -j$(nproc)")
    print("Compiled WineGDK successfully!")
    os.system("mkdir ~/.mcgdklauncher/prefix")
    print("Installing Winetricks dependencies (vkd3d, dxvk, nvapi)...")
    time.sleep(2)
    os.system("bash -c \"WINEPREFIX=~/.mcgdklauncher/prefix winetricks vkd3d dxvk dxvk_nvapi0061\"")
    os.system("mkdir ~/.mcgdklauncher/Minecraft")
    print("Please place your unencrypted game files in ~/.mcgdklauncher/Minecraft (place the Content folder there.) IMPORTANT: The main executable must have extra \"s\" at the end of its name")
    print("Waiting for user to place game files...")
    time.sleep(10)
    if os.path.exists("~/.mcgdklauncher/Minecraft/Content"):
        print("Game files detected, setup complete! Please restart the launcher.")
        time.sleep(5)
        exit(0)
    else:
        print("Still waiting")
        time.sleep(30)
        if os.path.exists("~/.mcgdklauncher/Minecraft/Content"):
            print("Game files detected, setup complete! Please restart the launcher.")
            time.sleep(5)
            exit(0)
        else:
            print("Game files not found. Please place them in ~/.mcgdklauncher/Minecraft and restart the launcher.")
            time.sleep(5)
            exit(1)
