packagesNeedingInstallation <- function(package) 
{
  available <- suppressMessages(suppressWarnings(sapply(package, require, quietly = TRUE, character.only = TRUE, warn.conflicts = FALSE)))
  missing <- package[!available]
  if (length(missing) > 0) return(missing)
  return(character())
}

isCRANChoosen <- function()
{
  return(getOption("repos")["CRAN"] != "@CRAN@")
}

installNeededPackages <- function(requiredPackages, defaultCRANmirror = "https://cran.rstudio.com/") 
{
  packagesNeedInstall<-packagesNeedingInstallation(requiredPackages)
  if(length(packagesNeedInstall)>0)
  {
    if(!isCRANChoosen())
    {       
      #chooseCRANmirror()
      options(repos=structure(c(CRAN="http://cran.rstudio.com/")))
      if(!isCRANChoosen())
      {
        options(repos = c(CRAN = defaultCRANmirror))
      }
    }
    
    suppressMessages(suppressWarnings(install.packages(packagesNeedInstall)))
    packagesNeedInstall<-packagesNeedingInstallation(requiredPackages)
    if(length(packagesNeedInstall)==0) print("All required packages were successfully installed")
    else sprintf('The following package(s) were not installed: $s', paste(packagesNeedInstall,collapse = ','))
  }
}