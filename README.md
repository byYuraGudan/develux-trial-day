# develux-trial-day

# Install script requirements 
```
pip install -r req/requirements.prod.txt
```
# Install tests requirements
```
pip install -r req/requirements.dev.txt
```
# Make `src` Source directory
# Make `tests` Tests directory 

# To run this script you need the next parameters:
    1. package name
    2. package version
    3. bitbucket workspace
    4. bitbucket repository
    5. access token to bitbucket repository (link: https://bitbucket.org/<workspace>/<repository>/admin/access-tokens)

# Note 

Make sure you have package.json in root directory in the repository.

# Run script from the console
```
python src/update_package_script.py <package-name> <package-version> <bitbucket-workspace> <bitbucket-repository> <bitbucket-token>
```
Example:
```
python src/update_package_script.py package 0.2.1 yuriihudan npm-package <TOKEN>
```
