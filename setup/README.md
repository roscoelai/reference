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
  - `mkdir -p '/opt' "/home/${USERNAME}"`

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

- Remove/Add some packages:
  - `pacman -Rs $(pacman -Qqs i686)`
  - `pacman -Rs mingw-w64-x86_64-xpdf-tools`
  - `pacman -S mingw-w64-x86_64-github-cli mingw-w64-x86_64-imagemagick mingw-w64-x86_64-poppler tree`

- Set some configs for git
  - `git config --global user.email user@email.com`
  - `git config --global user.name "First Last"`

- If there are error messages on welcome, have a look at `/etc/profile.d/git-sdk.sh`

---

## Miniconda

- [What is Conda?](https://conda.io/projects/conda/en/latest/index.html)

- Download [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
  - [[Miniconda3-latest-Windows-x86_64.exe](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe)]
  - [[Miniconda3-py39_4.10.3-Windows-x86_64.exe](https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Windows-x86_64.exe)]

- Extract somewhere (_e.g._ `/opt/Miniconda3`)

- Add the following to `~/.bashrc`

```bash
conda() {
    local miniconda3="${EXEPATH}/opt/Miniconda3"
    local activate="${miniconda3}/Scripts/activate.bat"
    start cmd //k "${activate}" "${miniconda3}"
}
```

- Set some configs for conda
  - `conda config --add channels conda-forge`
  - `conda config --set channel_priority strict`

- Install [mamba](https://github.com/mamba-org/mamba)
  - `conda install mamba -n base -c conda-forge`

- [Managing environments manual](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

- Create some environments
  - [MNE](https://mne.tools/stable/install/index.html)
    - `mamba create --name=mne --channel=conda-forge mne`
  - [PsychoPy](https://www.psychopy.org/download.html)
    - Environment file [psychopy-env.yml](https://raw.githubusercontent.com/psychopy/psychopy/master/conda/psychopy-env.yml)
    - `mamba env create -n psychopy -f psychopy-env.yml`

---

## R, RStudio, Rtools40

- Visit [CRAN](https://cran.r-project.org/index.html)
  - [[R-4.1.1-win.exe](https://cran.r-project.org/bin/windows/base/R-4.1.1-win.exe)]
  - Extract somewhere (_e.g._ `/opt/R-4.1.1`)
  - Add the following to `~/.bashrc`
    - `export PATH="${PATH}:/opt/R-4.1.1/bin/x64"`

- Get [RStudio](https://www.rstudio.com/products/rstudio/download/)
  - [[RStudio-2021.09.0-351.zip](https://download1.rstudio.org/desktop/windows/RStudio-2021.09.0-351.zip)]
  - Extract somewhere (_e.g._ `/opt/RStudio-2021.09.0-351`)
  - Add the following to `~/.bashrc`
    - `export PATH="${PATH}:/opt/RStudio-2021.09.0-351/bin"`

- (Optional) Get [Rtools40](https://cran.r-project.org/bin/windows/Rtools/)
  - [[rtools40v2-x86_64.exe](https://cran.r-project.org/bin/windows/Rtools/rtools40v2-x86_64.exe)]

- [Using RStudio Projects](https://support.rstudio.com/hc/en-us/articles/200526207-Using-Projects)
  - Very useful for organizing work
  - Especially for collaboration

---

## Others

- Rust
  - `pacman -S mingw-w64-x86_64-rust`
  - 😊
  - Have a look at [rustup](https://rustup.rs/)
- Go
  - `pacman -S mingw-w64-x86_64-go`
  - 😊
- [Java JDK](https://jdk.java.net/)
  - [[openjdk-17.0.1_windows-x64_bin.zip](https://download.java.net/java/GA/jdk17.0.1/2a2082e5a09d4267845be086888add4f/12/GPL/openjdk-17.0.1_windows-x64_bin.zip)]
  - Extract somewhere (_e.g._ `/opt/openjdk-17.0.1`)
  - Add the following to `~/.bashrc`
    - `export PATH="/opt/jdk-17.0.1/bin:${PATH}"`


