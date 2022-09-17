# Setup Working Environment

> _On a Windows machine_

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

## Miniconda

- [What is Conda?](https://conda.io/projects/conda/en/latest/index.html)

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
  - [[Miniconda3-py39_4.12.0-Windows-x86_64.exe](https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Windows-x86_64.exe)]
  - Extract somewhere (_e.g._ `/opt/Miniconda3`)
  - Add the following to `~/.bashrc`
    - `export PATH="${PATH}:/opt/Miniconda3/Scripts"`

```bash
# conda init bash
conda config --set auto_activate_base false
conda config --add channels conda-forge
conda config --set channel_priority strict
```

- Install [mamba](https://github.com/mamba-org/mamba)
  - `conda install mamba -n base -c conda-forge`

- [Managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

- Create environment(s)
  - [MNE](https://mne.tools/stable/install/index.html)
    - `mamba create --override-channels --channel=conda-forge --name=mne mne`
    - `mamba create -n mne python=3.9 jupyterlab mne nodejs openpyxl pytorch`

---

## R, RStudio, (optional) RTools

- R from [CRAN](https://cran.r-project.org/index.html)
  - [[R-4.2.1-win.exe](https://cran.r-project.org/bin/windows/base/R-4.2.1-win.exe)]
  - Extract somewhere (_e.g._ `/opt/R-4.2.1`)
  - Add the following to `~/.bashrc`
    - `export PATH="${PATH}:/opt/R-4.2.1/bin"`

- [RStudio](https://www.rstudio.com/products/rstudio/download/)
  - [[RStudio-2022.07.1-554.zip](https://download1.rstudio.org/desktop/windows/RStudio-2022.07.1-554.zip)]
  - Extract somewhere (_e.g._ `/opt/RStudio-2022.07.1-554`)
  - Add the following to `~/.bashrc`
    - `export PATH="${PATH}:/opt/RStudio-2022.07.1-554/bin"`

- (Optional) [RTools](https://cran.r-project.org/bin/windows/Rtools/)
  - [[rtools42-5253-5107-signed.exe](https://cran.r-project.org/bin/windows/Rtools/rtools42/files/rtools42-5253-5107-signed.exe)]

- [Using RStudio Projects](https://support.rstudio.com/hc/en-us/articles/200526207-Using-Projects)
  - Very useful for organizing work, especially for collaboration (relative paths, ...)

---

## Java

- [Java JDK](https://jdk.java.net/)
  - [[openjdk-18.0.2.1_windows-x64_bin.zip](https://download.java.net/java/GA/jdk18.0.2.1/db379da656dc47308e138f21b33976fa/1/GPL/openjdk-18.0.2.1_windows-x64_bin.zip)]
  - Extract somewhere (_e.g._ `/opt/openjdk-18.0.2.1`)
  - Add the following to `~/.bashrc`
    - `export PATH="/opt/openjdk-18.0.2.1/bin:${PATH}"`

---

## SSH

- If you forgot everything about SSH, start from here: https://calmcode.io/ssh/introduction.html
- https://docs.github.com/en/authentication/connecting-to-github-with-ssh

```bash
man ssh
man ssh_config
```

---


