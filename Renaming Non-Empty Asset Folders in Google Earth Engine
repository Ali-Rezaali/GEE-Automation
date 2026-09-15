import warnings

# [1] SUPPRESS DEPRECATION WARNINGS

warnings.filterwarnings("ignore", category=FutureWarning)

import ee

ee.Initialize()

# [2] PATH CONFIGURATION

OldFolderPath = "projects/your-project/assets/Path/To/OldName"

NewFolderPath = "projects/your-project/assets/Path/To/NewName"


# [3] RECURSIVE FOLDER MOVE OPERATOR

def MoveAssetRecursive(SourcePath: str, DestinationPath: str):
    """Recursively moves assets, handling Folders and ImageCollections properly."""
    try:
        SourceInfo = ee.data.getAsset(SourcePath)
        AssetType = SourceInfo.get("type", "UNKNOWN")
    except Exception as Error:
        print(f"[ERROR] Source asset not found ({SourcePath}): {Error}")
        return

    # If it's a container (FOLDER or IMAGE_COLLECTION), migrate contents
    if AssetType in ["FOLDER", "IMAGE_COLLECTION"]:
        # Ensure destination container exists
        try:
            ee.data.getAsset(DestinationPath)
            print(f"[EXISTS] Container already at destination: {DestinationPath}")
        except Exception:
            ee.data.createAsset({"type": AssetType}, DestinationPath)
            print(f"[CREATED] {AssetType}: {DestinationPath}")

        # List all children inside the container
        Children = (
            ee.data.listAssets({"parent": SourcePath}).get("assets", [])
        )

        for Child in Children:
            ChildSource = Child["name"]
            ChildName = ChildSource.split("/")[-1]
            ChildDestination = f"{DestinationPath}/{ChildName}"

            # Recursively move child
            MoveAssetRecursive(ChildSource, ChildDestination)

        # Once all children are moved, delete the empty source container
        try:
            ee.data.deleteAsset(SourcePath)
            print(f"[CLEANUP] Deleted empty source container: {SourcePath}")
        except Exception as Error:
            print(
                f"[WARNING] Could not delete source container {SourcePath}: {Error}"
            )

    else:
        # Standard leaf asset (Image, FeatureCollection, Table, etc.)
        try:
            ee.data.renameAsset(SourcePath, DestinationPath)
            AssetName = SourcePath.split("/")[-1]
            print(f" [MOVED] {AssetName} -> {DestinationPath}")
        except Exception as Error:
            print(f" [FAILED] Could not move {SourcePath}: {Error}")


def RenameFolderWorkflow():
    print("--- AUTOMATED GEE FOLDER MIGRATION ---")
    print(f" Source:      {OldFolderPath}")
    print(f" Destination: {NewFolderPath}")
    print("--------------------------------------")

    Confirmation = input(
        f"This will move all children from '{OldFolderPath}' to '{NewFolderPath}'. Type 'YES' to proceed: "
    )

    if Confirmation.strip() == "YES":
        MoveAssetRecursive(OldFolderPath, NewFolderPath)
        print("\n[COMPLETE] Migration finished!")
    else:
        print("[ABORTED] No assets were modified.")


# [4] EXECUTE

if __name__ == "__main__":
    RenameFolderWorkflow()
