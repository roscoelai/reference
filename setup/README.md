# Setup Working Environment

> _On a Windows machine_

- 2 choices:
  - PortableGit (+MSYS2)
  - Git for Windows SDK
- Choose PortableGit for this round
  - PortableGit is lighter, but has no package manager
  - Programs that do not come bundled will have to be obtained manually (or with MSYS2)
  - Top on the list are: `rclone`, `rsync`
  - Others might include: `Python`, `Poppler`, `pngquant`, `ImageMagick`, `FFmpeg`, `GitHub CLI`

## PortableGit

Where you choose to put things, and how you manage user environment variables, is up to you.

- https://git-scm.com/download/win
- [PortableGit-2.40.0-64-bit.7z.exe](https://github.com/git-for-windows/git/releases/download/v2.40.0.windows.1/PortableGit-2.40.0-64-bit.7z.exe)

### File hash in PowerShell

```powershell
Get-Help Get-FileHash
Get-FileHash .\path\to\file.ext -Algorithm MD5
```

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

### Git config

- https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration

```bash
git config --system core.autocrlf false
git config --global user.email user@email.com
git config --global user.name "First Last"
```

---

## Git for Windows SDK

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

- Set some configs for git

```bash
git config --global user.email user@email.com
git config --global user.name "First Last"
```

- If there are error messages on welcome, have a look at `/etc/profile.d/git-sdk.sh`

---

## Conda

- [Miniforge](https://github.com/conda-forge/miniforge/releases)
  - As of `23.3.1-0`, identical to Mambaforge
  - Mambaforge discouraged as of September 2023
  - Add `path/to/miniforge3/condabin` to user `PATH`

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
  - Remove `defaults` channel: `conda config --remove channels defaults`
  - Add `conda-forge` channel: `conda config --add channels conda-forge`
  - Install `mamba`: `conda install mamba -n base`

- Other configurations

```bash
conda init cmd.exe  # (or bash)
conda config --append channels bioconda
conda config --set channel_priority strict
conda config --set auto_activate_base false
```

- Create environment(s)

```bash
# Examples:
mamba create -n main git pydicom python screen sqlite
mamba create -n ds jupyterlab pandas polars seaborn scikit-learn
mamba create -n aio aiohttp
mamba create -n mne jupyterlab mne
mamba create -n pytorch jupyterlab pytorch
mamba create -n r-h2o r-dbi r-h2o r-mice r-optparse r-sqlite
```

---

## R

- [CRAN](https://cran.r-project.org)
  - [R-4.2.2-win.exe](https://cran.r-project.org/bin/windows/base/R-4.2.2-win.exe)
  - [md5sum.R-4.2.2.txt](https://cran.r-project.org/bin/windows/base/md5sum.R-4.2.2.txt)
  - MD5 hash: `eaa06020ec663918c580050038f1d1d5`
  - `echo export PATH='"${PATH}:/opt/R-4.2.2/bin/x64"' >> ~/.bashrc`

- [RStudio](https://posit.co/download/rstudio-desktop)
  - [RStudio-2022.12.0-353.zip](https://download1.rstudio.org/electron/windows/RStudio-2022.12.0-353.zip)
  - SHA256 hash: `8c351ee495736d5d6352b437f329d5ce99daa3f7a112dd96a838a49073d72bc8`
  - `echo export PATH='"${PATH}:/opt/RStudio-2022.12.0-353"' >> ~/.bashrc`

- (Optional) [Rtools42 for Windows](https://cran.r-project.org/bin/windows/Rtools/rtools42/rtools.html)
  - [rtools42-5355-5357.exe](https://cran.r-project.org/bin/windows/Rtools/rtools42/files/rtools42-5355-5357.exe)

- [Using RStudio Projects](https://support.rstudio.com/hc/en-us/articles/200526207-Using-Projects)

---

## Java

- [Java JDK](https://jdk.java.net)
  - [openjdk-19.0.1_windows-x64_bin.zip](https://download.java.net/java/GA/jdk19.0.1/afdd2e245b014143b62ccb916125e3ce/10/GPL/openjdk-19.0.1_windows-x64_bin.zip)
  - [openjdk-19.0.1_windows-x64_bin.zip.sha256](https://download.java.net/java/GA/jdk19.0.1/afdd2e245b014143b62ccb916125e3ce/10/GPL/openjdk-19.0.1_windows-x64_bin.zip.sha256)
  - SHA256 hash: `adb1a33c07b45c39b926bdeeadf800f701be9c3d04e0deb543069e5f09856185`
  - `echo export PATH='"/opt/openjdk-19.0.1/bin:${PATH}"' >> ~/.bashrc`

---

## SSH

- If you forgot everything about SSH, start from here: https://calmcode.io/ssh/introduction.html
- https://docs.github.com/en/authentication/connecting-to-github-with-ssh

```bash
man ssh
man ssh_config
```

---


