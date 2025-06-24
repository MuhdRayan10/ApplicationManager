import os
import requests
import zipfile

# country codes
country_codes = [
    "us","cn","in","ru","gb","fr","de","br","it","jp",
    "ca","au","kr","za","mx","sa","ng","tr","ar","es",
    "nl","se","ch","be","pl","no","dk","fi","id","th",
    "eg","pk","vn","ph","cl","co","pe","ua","my","nz"
]

os.makedirs("flags", exist_ok=True)

for code in country_codes:
    url = f"https://flagcdn.com/w160/{code}.png"
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(f"flags/{code}.png", "wb") as f:
            f.write(resp.content)
    else:
        print(f"Failed: {code}")

# zipping 
zipf = zipfile.ZipFile("flags.zip", "w")
for code in country_codes:
    path = f"flags/{code}.png"
    if os.path.exists(path):
        zipf.write(path, arcname=f"{code}.png")
zipf.close()

print("Created country_flags_40.zip")
