# Setup Working Environment

Take advantage of package managers to keep tools organized and up to date. Unfortunately, some combination might be necessary, and it might not be possible for some tools.

This page will focus on Windows environments.

## Package managers

- WinGet
  - Can be temperamental, use for what works
    - VS Code
- [MSYS2](https://www.msys2.org/)
  - UNIX/Bash
    - Vim
    - Rclone
    - Rsync
    - Git
    - GitHub CLI
    - Micromamba
    - Others:
      - Poppler
      - pngquant
      - Ghostscript
      - ImageMagick
      - FFmpeg
- Manual
  - R
  - RStudio

---

### MSYS2

- Edit `/etc/pacman.conf`:
  - Comment out all repositories except `[ucrt64]` and `[msys]`
- Add to `PATH`:
  - `...\msys64\ucrt64\bin`
  - `...\msys64\usr\bin`

```bash
pacman -Syu

# Minimalist
pacman -S git vim

# More 1
pacman -S make git mingw-w64-ucrt-x86_64-github-cli mingw-w64-ucrt-x86_64-rclone rsync vim

# More 2
pacman -S make git mingw-w64-ucrt-x86_64-github-cli mingw-w64-ucrt-x86_64-rclone mingw-w64-ucrt-x86_64-imagemagick mingw-w64-ucrt-x86_64-pngquant mingw-w64-ucrt-x86_64-poppler rsync tree vim
```

---

### Git config

- https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration

```bash
git config --system core.autocrlf false
git config --global user.email user@email.com
git config --global user.name "First Last"
```

---

### Micromamba

Channels:

```
micromamba config append channels conda-forge
micromamba config append channels nodefaults
micromamba config set channel_priority strict
```

Environments:

```
micromamba create -n main git pydicom python screen sqlite
micromamba create -n aio aiohttp
micromamba create -n ds fastexcel jupyterlab pandas polars scikit-learn seaborn xlsxwriter
micromamba create -n ds2 -c h2oai -c pytorch fastexcel jupyterlab pandas polars pyarrow pyreadstat scikit-learn seaborn xlsxwriter h2o pytorch torchvision torchaudio cpuonly
```

---

### R

- [R](https://cran.r-project.org/bin/windows/base/)
- [RStudio](https://posit.co/download/rstudio-desktop/#:~:text=Zip/Tarballs)
  - Might need to edit `%USERPROFILE%\AppData\Roaming\RStudio\config.json`
    - Under `platform > windows > rExecutablePath`
    - Set `C:/.../R-x.x.x/bin/x64/Rterm.exe` (use forward slashes, or double back slashes)
- [Rtools](https://cran.r-project.org/bin/windows/Rtools) (optional)

Learn to use [RStudio Projects](https://support.rstudio.com/hc/en-us/articles/200526207-Using-Projects) to avoid headaches due to working directory/path issues (but it will not solve all problems).

---

### SSH

- If you forget everything, start from here: https://calmcode.io/ssh/introduction.html
- https://docs.github.com/en/authentication/connecting-to-github-with-ssh

```bash
man ssh
man ssh_config
```

---

### File hash in PowerShell

```powershell
Get-FileHash [-Path] -Algorithm MD5
```

---

### Legacy

#### Rsync

- [Zstandard](https://github.com/facebook/zstd/releases)
  - Symantec might not recognize the lastest one, so go for something older
- https://packages.msys2.org/package/rsync
  - [rsync-3.2.7-2-x86_64.pkg.tar.zst](https://mirror.msys2.org/msys/x86_64/rsync-3.2.7-2-x86_64.pkg.tar.zst)
    - SHA256: `786233bb7f3e8011182997330d74c21226c4085783d474eb448b39dec7ec566e`
- https://packages.msys2.org/package/libxxhash
  - [libxxhash-0.8.1-1-x86_64.pkg.tar.zst](https://mirror.msys2.org/msys/x86_64/libxxhash-0.8.1-1-x86_64.pkg.tar.zst)
    - SHA256: `9c8e2cb592bd78e8d10d6c896357d672999cab7c459e2b13220f572446105aef`
- https://packages.msys2.org/package/libopenssl
  - [libopenssl-3.1.0-1-x86_64.pkg.tar.zst](https://mirror.msys2.org/msys/x86_64/libopenssl-3.1.0-1-x86_64.pkg.tar.zst)
    - SHA256: `fa76246190fec6850623e73a69660d8394646b671ea9117748820a5fe937687e`
- Copy `rsync` executable to `/usr/bin`
- Try to run rsync first and let it complain about missing DLL(s)
- Copy missing DLL(s) to `/usr/bin` one-by-one until `rsync` works

#### Git for Windows SDK

- Read the ["Installing the SDK" section of the technical overview](https://github.com/git-for-windows/git/wiki/Technical-overview#installing-the-sdk)
  - [Git for Windows SDK](https://github.com/git-for-windows/build-extra/releases)
    - [[git-sdk-installer-1.0.8-64.7z.exe](https://github.com/git-for-windows/build-extra/releases/download/git-sdk-1.0.8/git-sdk-installer-1.0.8-64.7z.exe)]
  - Extract somewhere (_e.g._ `C:\git-sdk-64`)
  - Run `git-bash.exe` (and pin to taskbar)
  - `sdk init git`
  - `pacman -Syu`
    - [pacman manual](https://archlinux.org/pacman/pacman.8.html)

- Create some directories

```bash
mkdir -p '/opt' "/home/${USERNAME}"
```

- Create/Edit some config files

```bash
printf "Transparency=medium\nWindow=full" > /etc/minttyrc

if [ -f /etc/profile-original ]; then
	cp /etc/profile-original /etc/profile
else
	cp /etc/profile /etc/profile-original
fi

h="/home/${USERNAME}"
sed -i "28i \
HOME='${h}'\n\
HOMEDRIVE='${h}'\n\
HOMEPATH='${h}'\n\
HISTFILE='${h}/.bash_history'\n" /etc/profile
```

- Remove/Add some packages

```bash
pacman -Rs $(pacman -Qqs i686)
pacman -Rs mingw-w64-x86_64-xpdf-tools
# pacman -S mingw-w64-x86_64-github-cli mingw-w64-x86_64-ffmpeg mingw-w64-x86_64-imagemagick mingw-w64-x86_64-pngquant mingw-w64-x86_64-poppler tree
# ffmpeg segfaulted, get compiled executables instead
pacman -S mingw-w64-x86_64-github-cli mingw-w64-x86_64-imagemagick mingw-w64-x86_64-pngquant mingw-w64-x86_64-poppler tree
```

- If there are error messages on welcome, have a look at `/etc/profile.d/git-sdk.sh`

---

### Java

Might be necessary for H2O (only Java versions 8-17 are supported).

- [Java JDK](https://jdk.java.net)
- [OpenJDK Archive](https://jdk.java.net/archive)
- Add `C:\...\jdk-x.x.x\bin` to `PATH`

---


