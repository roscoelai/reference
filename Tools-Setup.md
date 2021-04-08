# Tools Setup

## For Windows

### R/RStudio/Rtools40

- [The Comprehensive R Archive Network](https://cran.r-project.org/) - [[R-4.0.4-win.exe](https://cran.r-project.org/bin/windows/base/R-4.0.4-win.exe)]
- [RStudio Desktop](https://rstudio.com/products/rstudio/download/) - [[RStudio-1.4.1106.zip](https://download1.rstudio.org/desktop/windows/RStudio-1.4.1106.zip)]
- [Rtools40](https://cran.r-project.org/bin/windows/Rtools/) - [[rtools40-x86_64.exe](https://cran.r-project.org/bin/windows/Rtools/rtools40-x86_64.exe)] (optional)

Learn more about [using projects](https://support.rstudio.com/hc/en-us/articles/200526207-Using-Projects)

### Miniconda

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) - [[Miniconda3-latest-Windows-x86_64.exe](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe)]

Create a new environment (`env1` might not be the best name for an environment)

```
conda create -n env1 python ipython jupyterlab matplotlib numpy openpyxl pandas scikit-learn scipy seaborn spyder statsmodels tqdm

conda activate env1

conda update --all
```

Learn more about [managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

Or use the base environment (Not recommended)

```
conda install python ipython jupyterlab matplotlib numpy openpyxl pandas scikit-learn scipy seaborn spyder statsmodels tqdm

conda update --all
```

### Git for Windows SDK

- [Git for Windows SDK 1.0.8](https://github.com/git-for-windows/build-extra/releases) - [[git-sdk-installer-1.0.8-64.7z.exe](https://github.com/git-for-windows/build-extra/releases/download/git-sdk-1.0.8/git-sdk-installer-1.0.8-64.7z.exe)]

### Julia

- [Julia](https://julialang.org/downloads/) - [[julia-1.6.0-win64.zip](https://julialang-s3.julialang.org/bin/winnt/x64/1.6/julia-1.6.0-win64.zip)]

```julia
julia> ]
(@v1.6) pkg> add CSV DataFrames Plots Pluto
julia> import Pluto
julia> Pluto.run(launch_browser = false)
```
