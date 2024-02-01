# Windows
## Dirs..
- Zip : C:\Program Files\7-Zip\7z.exe
- Process : D:\pal-world
- steamcmd : D:\SteamCMD\steamcmd.exe

## Features
- memory monitoring and auto restart (16GB excess)
- 5 min auto backup
- 2 hour update check and update (auto restart on update)
- auto install steamcmd

## How to start?
[KO]
[7-Zip 설치](https://www.7-zip.org/)

/pal-world/windows/update-scripts/PalworldUpdate.bat 실행
(자동으로 steamcmd 를 설치함)

/pal-world/windows/WindowsScriptExecutor.bat 실행 후 서버 종료
(설정 전부 기본으로 할거면 서버 종료는 안해도 됨)

!!설정 할 사람만!!<br/>
/pal-world/SteamCMD/steamapps/common/PalServer/DefaultPalWorldSettings.ini 내용 복사

/pal-world/SteamCMD/steamapps/common/PalServer/Pal/Saved/Config/WindowsServer/PalWorldSettings.ini 생성 후 복사한 내용 붙여넣기

/pal-world/windows/WindowsScriptExecutor.bat 실행

[EN]
[Install 7-Zip](https://www.7-zip.org/)

execute /pal-world/windows/update-scripts/PalworldUpdate.bat
(auto install steamcmd)

execute /pal-world/windows/WindowsScriptExecutor.bat and shut down the server
(if you want to keep default settings, shutting down the server is not necessary)

!!Only for those who want to configure!!<br/>
Copy the contents of /pal-world/SteamCMD/steamapps/common/PalServer/DefaultPalWorldSettings.ini

Create /pal-world/SteamCMD/steamapps/common/PalServer/Pal/Saved/Config/WindowsServer/PalWorldSettings.ini and paste the copied contents

Run /pal-world/windows/WindowsScriptExecutor.bat
