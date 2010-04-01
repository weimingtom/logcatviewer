  !include "MUI.nsh"
  !include "x64.nsh"

;--------------------------------

SetOverwrite on
;--------------------------------

!macro MoveFileToDetails file

  Push $0
  Push $1
  Push $2
  Push $3

  StrCpy $0 "${file}"

  FileOpen $1 $0 r
  IfErrors +9

    FileRead $1 $2
    IfErrors +7

    StrCpy $3 $2 2 -2
    StrCmp $3 "$\r$\n" 0 +2
      StrCpy $2 $2 -2

    StrCmp $2 "" +2
      DetailPrint $2

    Goto -7

  FileClose $1
  Delete $0

  Pop $3
  Pop $2
  Pop $1
  Pop $0

!macroend

;--------------------------------

; The name of the installer
Name "$%VENDOR% $%PRODUCT%"

; The file to write
OutFile "..\$%VENDOR%_$%PRODUCT%_$%VERSION%-setup.exe"

; The default installation directory
InstallDir $PROGRAMFILES\$%VENDOR%\$%PRODUCT%

; Registry key to check for directory (so if you install again, it will
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\$%VENDOR%\$%PRODUCT%" "Install_Dir"

;Vista redirects $SMPROGRAMS to all users without this
RequestExecutionLevel admin

ShowInstDetails show
ShowUninstDetails show

;--------------------------------
; Pages

  !define MUI_WELCOMEPAGE_TITLE_3LINES
  !define MUI_FINISHPAGE_TITLE_3LINES

  !define MUI_FINISHPAGE_SHOWREADME ChangeLog.txt
  !define MUI_FINISHPAGE_SHOWREADME_NOTCHECKED

  !define MUI_FINISHPAGE_LINK "Visit $%VENDOR% homepage"
  !define MUI_FINISHPAGE_LINK_LOCATION http://www.$%VENDOR%.com/

  !define MUI_FINISHPAGE_NOAUTOCLOSE

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH

  !define MUI_WELCOMEPAGE_TITLE_3LINES
  !define MUI_FINISHPAGE_TITLE_3LINES
  !define MUI_UNFINISHPAGE_NOAUTOCLOSE

  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

;--------------------------------
; Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------

Section "$%VENDOR%" sec_$%VENDOR%

  SectionIn RO

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR

  ; Put files there
  File /r "..\dist\*.*"
  File /r "..\filter.ini" 
  File /r "..\ChangeLog.txt"

  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\$%VENDOR%\$%PRODUCT% "Install_Dir" "$INSTDIR"

  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$%PRODUCT%" "DisplayName" "$%VENDOR% $%PRODUCT%"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$%PRODUCT%" "HelpLink" "http://www.$%VENDOR%.com"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$%PRODUCT%" "URLUpdateInfo" "http://www.$%VENDOR%.com"

  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$%PRODUCT%" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$%PRODUCT%" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$%PRODUCT%" "NoRepair" 1

  WriteUninstaller "uninstall.exe"

SectionEnd

;--------------------------------

Section "Start Menu Shortcuts" sec_shortcuts
  SetOutPath $INSTDIR

  CreateDirectory "$SMPROGRAMS\$%VENDOR%\$%PRODUCT%"
  CreateShortCut "$SMPROGRAMS\$%VENDOR%\$%PRODUCT%\$%PRODUCT%.V.$%VERSION%.lnk" "$INSTDIR\$%PRODUCT%.exe"
  CreateShortCut "$SMPROGRAMS\$%VENDOR%\$%PRODUCT%\ChangeLog.lnk" "$INSTDIR\ChangeLog.txt"
  CreateShortCut "$SMPROGRAMS\$%VENDOR%\$%PRODUCT%\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$QUICKLAUNCH\$%PRODUCT%V.$%VERSION%.lnk" "$INSTDIR\$%PRODUCT%.exe"
  CreateShortCut "$DESKTOP\$%PRODUCT%V.$%VERSION%.lnk" "$INSTDIR\$%PRODUCT%.exe"

SectionEnd


;--------------------------------

; Uninstaller

Section "Uninstall"

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR


  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$%PRODUCT%"
  DeleteRegKey HKLM SOFTWARE\$%VENDOR%\$%PRODUCT%
  
  ; Remove files and uninstaller

  Delete "$INSTDIR\*.*"


  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\$%VENDOR%\$%PRODUCT%\*.*"
  Delete "$DESKTOP\$%PRODUCT%V.$%VERSION%.lnk"
  Delete "$QUICKLAUNCH\$%PRODUCT%V.$%VERSION%.lnk"

  ; Remove directories used
  RMDir "$SMPROGRAMS\$%VENDOR%\$%PRODUCT%"

  RMDir /r "$INSTDIR"

SectionEnd

;--------------------------------

  ;Language strings
  LangString DESC_sec_$%VENDOR% ${LANG_ENGLISH} "Install $%VENDOR% $%PRODUCT% files."
  LangString DESC_sec_shortcuts ${LANG_ENGLISH} "Add shortcuts to the Start Menu."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${sec_$%VENDOR%} $(DESC_sec_$%VENDOR%)
    !insertmacro MUI_DESCRIPTION_TEXT ${sec_shortcuts} $(DESC_sec_shortcuts)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------

Function .onInit
var /GLOBAL unPath

StrCpy $unPath "c:\Program Files\$%VENDOR%\$%PRODUCT%\uninstall.exe" 

IfFileExists "c:\Program Files\$%VENDOR%\$%PRODUCT%\uninstall.exe" uninstall

ReadRegStr $unPath HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$%VENDOR%" "UninstallString"
IfErrors 0 uninstall
goto End

quit:
    Quit
uninstall:
    MessageBox MB_YESNO|MB_ICONQUESTION \
               "$%VENDOR% $%PRODUCT% already installed at$\n$\n    $unPath, $\n$\nClick Yes to uninstall it, No to quit installation." \
               IDYES doUninstall \
               IDNO quit
doUninstall:
    ExecWait $unPath

End:


FunctionEnd
