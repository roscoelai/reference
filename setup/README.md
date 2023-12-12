# Setup Working Environment

This is primarily about managing tools for work on a Windows machine. Ideally a package manager will be able to handle this, but it might be necessary to combine a few, and still handle some tools manually. Phasing out [PortableGit](https://git-scm.com/download/win#:~:text=64%2Dbit%20Git%20for%20Windows%20Portable) from the discussion here, but it might still be useful if the bundled tools are adequate for the task.

### Package managers
- `winget` (check it out, but it may not solve all problems)
- `pacman` (from MSYS2)
  - <sup><sub>or [Git for Windows SDK](https://gitforwindows.org/#:~:text=Git%20for%20Windows%20SDK), avoid for now</sub></sup>
- `conda`/`mamba` (from Miniforge3)
- MSYS2 and Miniforge3 may be managed by `winget`

Some tools that may be needed:
```
Rclone
Rsync
Python
Git
GitHub CLI
Poppler
pngquant
Ghostscript
ImageMagick
FFmpeg
```

---

## Conda

- [Miniforge3](https://github.com/conda-forge/miniforge#:~:text=Windows,x86_64)
  - Use `winget` if possible
  - Add `C:\...\path\to\miniforge3\condabin` to `PATH`
- <sup><sub>[Miniconda](https://docs.conda.io/projects/miniconda/en/latest), avoid for now</sub></sup>

Config:

```
conda config --set auto_activate_base false
```

Channel management:

```
conda config --append channels bioconda
conda config --set channel_priority strict
```

Create environment(s):

```
mamba create -n main git pydicom python screen sqlite
mamba create -n ds jupyterlab pandas polars seaborn scikit-learn
mamba create -n ds jupyterlab pandas polars pyarrow pyreadstat scikit-learn seaborn xlsx2csv xlsxwriter pytorch torchvision torchaudio cpuonly -c pytorch
mamba create -n aio aiohttp
mamba create -n mne jupyterlab mne
mamba create -n r-h2o r-dbi r-h2o r-mice r-optparse r-sqlite
```

---

## R

- [R](https://cran.r-project.org/bin/windows/base/)
  - Use `winget` if possible
- [RStudio](https://posit.co/download/rstudio-desktop/#:~:text=Zip/Tarballs)
  - `winget` might not be possible
  - Might need to edit `%USERPROFILE%\AppData\Roaming\RStudio\config.json`
    - Under `platform > windows > rExecutablePath`
    - Set `C:/.../R-x.x.x/bin/x64/Rterm.exe` (can use forward slashes, or double back slashes)
- <sup><sub>[Rtools](https://cran.r-project.org/bin/windows/Rtools), avoid for now</sub></sup>

Learn to use [RStudio Projects](https://support.rstudio.com/hc/en-us/articles/200526207-Using-Projects) to avoid headaches due to working directory/path issues (but it will not solve all problems).

---

## Java

Might be necessary for H2O (only Java versions 8-17 are supported).

- [Java JDK](https://jdk.java.net)
- [OpenJDK Archive](https://jdk.java.net/archive)
- Add `C:\...\jdk-x.x.x\bin` to `PATH`

---

## SSH

- If you forget everything, start from here: https://calmcode.io/ssh/introduction.html
- https://docs.github.com/en/authentication/connecting-to-github-with-ssh

```bash
man ssh
man ssh_config
```

---

## Out of place

### How to calculate file hash in PowerShell

```powershell
Get-FileHash [-Path] -Algorithm MD5
```

### Git config

- https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration

```bash
git config --system core.autocrlf false
git config --global user.email user@email.com
git config --global user.name "First Last"
```

---

## Legacy

### Rsync

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

### Git for Windows SDK

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


