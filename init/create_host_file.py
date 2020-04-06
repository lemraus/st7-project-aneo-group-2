import os

OUTPUT_DIR = os.environ.get("AZ_BATCH_NODE_SHARED_DIR")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "hostfile")

if __name__ == "__main__":
    with open(OUTPUT_FILE, "w") as hostfile:
        content = "\n".join(os.environ.get("AZ_BATCH_HOST_LIST").split(","))
        hostfile.write(content)
