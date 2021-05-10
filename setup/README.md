# Setup Working Environment

> _On a Windows machine_

## 1. Git for Windows SDK

1. Download [Git for Windows SDK](https://github.com/git-for-windows/build-extra/releases) - [[git-sdk-installer-1.0.8-64.7z.exe](https://github.com/git-for-windows/build-extra/releases/download/git-sdk-1.0.8/git-sdk-installer-1.0.8-64.7z.exe)]

2. Extract to a directory, determined by preference and privilege (_e.g._ `C:\git-sdk-64`), while following [installation instructions](https://github.com/git-for-windows/git/wiki/Technical-overview#installing-the-sdk)

```bash
sdk init git
```

3. Run and pin `git-bash.exe` to taskbar

4. Update packages (learn about [pacman](https://archlinux.org/pacman/pacman.8.html))

```bash
pacman -Syu
```

5. Create some directories:

```bash
mkdir -p '/opt'
mkdir -p "/home/${USERNAME}"
```

6. Create/Edit some config files:

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

7. Remove some packages

```bash
pacman -Rs $(pacman -Qqs i686)
pacman -Rs mingw-w64-x86_64-xpdf-tools
```

8. Set some global configs for git

```bash
git config --global core.askPass ""
git config --global credential.helper ""
git config --global user.name "John Doe"
git config --global user.email johndoe@example.com
```

9. There might be some error messages on welcome, which may require editing `/etc/profile.d/git-sdk.sh`

## 2. Miniconda

1. Download [Miniconda](https://docs.conda.io/en/latest/miniconda.html) - [[Miniconda3-latest-Windows-x86_64.exe](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe)]

2. Extract to a directory in `/opt` (_e.g._ `/opt/Miniconda3`)

3. Add the following to `~/.bashrc` (to access conda command prompt using `conda`)

```bash
export DLFLD="${USERPROFILE}/Downloads"
conda() {
    local miniconda3="${EXEPATH}\\opt\\Miniconda3"
    local activate="${miniconda3}\\Scripts\\activate.bat"
    start //d "${DLFLD//\//\\}" cmd //k "${activate}" "${miniconda3}"
}
```

4. Learn about [conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)

5. Open conda command prompt and install [mamba](https://github.com/mamba-org/mamba)

```
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install mamba -n base -c conda-forge
```

6. Learn about [managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

7. Create a new environment using a `environment.yaml` file (_e.g._ [environment.yml](https://raw.githubusercontent.com/mne-tools/mne-python/main/environment.yml))

```
mamba env update --file environment.yml
```

8. Or create a new envrionment manually

```
mamba create -n env1 python ipython jupyterlab matplotlib numpy openpyxl pandas scikit-learn scipy spyder statsmodels
```

## 3. R/RStudio/Rtools40

1. Download R from [The Comprehensive R Archive Network](https://cran.r-project.org/) - [[R-4.0.5-win.exe](https://cran.r-project.org/bin/windows/base/R-4.0.5-win.exe)]

2. Download [RStudio Desktop](https://rstudio.com/products/rstudio/download/) - [[RStudio-1.4.1106.zip](https://download1.rstudio.org/desktop/windows/RStudio-1.4.1106.zip)]

3. Extract to directories in `/opt` (_e.g._ `/opt/R-4.0.5` and `/opt/RStudio-1.4.1106`)

4. Add the following to `~/.bashrc` (to access RStudio using `rstudio`)

```bash
export PATH="${PATH}:/opt/R-4.0.5/bin:/opt/R-4.0.5/bin/x64:/opt/RStudio-1.4.1106/bin"
export DLFLD="${USERPROFILE}/Downloads"
alias rstudio='start //d "${DLFLD//\//\\}" rstudio'
```

5. Learn more about [using projects](https://support.rstudio.com/hc/en-us/articles/200526207-Using-Projects)

6. (Optional) Download [Rtools40](https://cran.r-project.org/bin/windows/Rtools/) - [[rtools40v2-x86_64.exe](https://cran.r-project.org/bin/windows/Rtools/rtools40v2-x86_64.exe)] and follow the installation instructions

## 4. Julia

1. Download [Julia](https://julialang.org/downloads/) - [[julia-1.6.1-win64.zip](https://julialang-s3.julialang.org/bin/winnt/x64/1.6/julia-1.6.1-win64.zip)]

2. Extract to a directory in `/opt` (_e.g._ `julia-1.6.1`)

3. Add packages

```julia
julia> ]
(@v1.6) pkg> add CSV DataFrames Plots Pluto
```

4. Launch Pluto notebook

```julia
julia> import Pluto
julia> Pluto.run(launch_browser = true)
```
