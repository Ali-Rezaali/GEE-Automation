import warnings

# [1] SUPPRESS DEPRECATION & EOL WARNINGS (Python 3.9 EOL / google-auth warnings)

warnings.filterwarnings("ignore", category=FutureWarning)

import ee

ee.Initialize()

# [2] PATH & CONFIGURATION

BasePath = "projects/your-project/assets/Path/To/Models/"

ModelSuffixes = ["T2M", "WS", "SM"]

# [3] DEFINE TARGET LABELS BY YEAR (4 SEASONS PER LINE)

# Uncomment the whole yearly row (or specific items) to remove

SiteOneLabels = [
    "S1-2020", "S2-2020", "S3-2020", "S4-2020",
    "S1-2021", "S2-2021", "S3-2021", "S4-2021",
    "S1-2022", "S2-2022", "S3-2022", "S4-2022",
    "S1-2023", "S2-2023", "S3-2023", "S4-2023",
    "S1-2024", "S2-2024", "S3-2024", "S4-2024",
    "S1-2025", "S2-2025", "S3-2025", "S4-2025",
]

SiteTwoLabels = [
    "S1-2020", "S2-2020", "S3-2020", "S4-2020",
    "S1-2021", "S2-2021", "S3-2021", "S4-2021",
    "S1-2022", "S2-2022", "S3-2022", "S4-2022",
    "S1-2023", "S2-2023", "S3-2023", "S4-2023",
    "S1-2024", "S2-2024", "S3-2024", "S4-2024",
    "S1-2025", "S2-2025", "S3-2025", "S4-2025",
]


# [4] GENERATE TARGET ASSET PATHS

def GenerateAssetPaths():
  
    TargetPaths = []

    # SiteOne Model Assets
  
    for Label in SiteOneLabels:
      
        for Suffix in ModelSuffixes:
          
            TargetPaths.append(f"{BasePath}SiteOne-{Label}-Model-{Suffix}")

    # SiteTwo Model Assets
  
    for Label in SiteTwoLabels:
      
        for Suffix in ModelSuffixes:
          
            TargetPaths.append(f"{BasePath}SiteTwo-{Label}-Model-{Suffix}")

    return TargetPaths


# [5] BATCH DELETE OPERATOR

def DeleteTargetedAssets():
 
  Targets = GenerateAssetPaths()

    if not Targets:
     
      print("[!] No active labels selected. Aborting.")
     
      return

    print("--- TARGETED ASSETS FOR PURGE ---")
    for Path in Targets:
        print(f" -> {Path}")
    print("---------------------------------")

    Confirm = input(f"Are you sure you want to PERMANENTLY delete these {len(Targets)} assets? Type 'YES': ")

    if Confirm.strip() == "YES":
        for Path in Targets:
            try:
                ee.data.deleteAsset(Path)
                print(f"[SUCCESS] Deleted: {Path}")
            except Exception as Err:
                print(f"[FAILED] Could not delete {Path}: {Err}")
    else:
        print("[ABORTED] Deletion canceled. No assets were touched.")


# [6] EXECUTE

if __name__ == "__main__":
  
    DeleteTargetedAssets()
