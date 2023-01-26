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

## Conda

- [Mambaforge](https://github.com/conda-forge/miniforge/releases)
  - [Mambaforge-22.9.0-2-Windows-x86_64.exe](https://github.com/conda-forge/miniforge/releases/download/22.9.0-2/Mambaforge-22.9.0-2-Windows-x86_64.exe)
  - [Mambaforge-22.9.0-2-Windows-x86_64.exe.sha256](https://github.com/conda-forge/miniforge/releases/download/22.9.0-2/Mambaforge-22.9.0-2-Windows-x86_64.exe.sha256)
  - SHA256 hash: `625ed0a94588dd7e38b108e907ed51c78bbaafdb7a50a699864033c963d47189`
  - `echo export PATH='"${PATH}:/opt/mambaforge/Scripts"' >> ~/.bashrc`

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
  - [Miniconda3-py310_22.11.1-1-Windows-x86_64.exe](https://repo.anaconda.com/miniconda/Miniconda3-py310_22.11.1-1-Windows-x86_64.exe)
  - SHA256 hash: `2e3086630fa3fae7636432a954be530c88d0705fce497120d56e0f5d865b0d51`
  - `echo export PATH='"${PATH}:/opt/miniconda3/Scripts"' >> ~/.bashrc`
  - Install [mamba](https://github.com/mamba-org/mamba) if not using Mambaforge (**[not recommended](https://mamba.readthedocs.io/en/latest/installation.html)**)
    - `conda install mamba -n base -c conda-forge`

- Configuration(s)

```bash
conda init cmd.exe
# conda init bash
conda config --append channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
conda config --set auto_activate_base false
conda config --show
```

- Create environment(s)

```bash
# conda activate base
mamba create -n ds jupyterlab nodejs openpyxl matplotlib seaborn scikit-learn  # python ipython numpy pandas
mamba create -n mne jupyterlab nodejs mne
mamba create -n pytorch jupyterlab nodejs pytorch
mamba create -n aio aiohttp aiodns brotli git sqlite uvloop
mamba create -n main git python screen sqlite
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


