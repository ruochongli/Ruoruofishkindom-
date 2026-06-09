#!/bin/bash
# 为所有文件和文件夹生成 .meta 文件

cd "$(dirname "$0")"

generate_meta() {
    local path="$1"
    local guid=$(python3 -c "import uuid; print(str(uuid.uuid4()).replace('-',''))" 2>/dev/null || cat /proc/sys/kernel/random/uuid | tr -d '-' 2>/dev/null || openssl rand -hex 16)
    
    if [ -d "$path" ]; then
        cat > "$path.meta" <<METAFOLDER
fileFormatVersion: 2
guid: $guid
folderAsset: yes
DefaultImporter:
  externalObjects: {}
  userData: 
  assetBundleName: 
  assetBundleVariant: 
METAFOLDER
    else
        local ext="${path##*.}"
        case "$ext" in
            cs)
                cat > "$path.meta" <<METACS
fileFormatVersion: 2
guid: $guid
MonoImporter:
  externalObjects: {}
  serializedVersion: 2
  defaultReferences: []
  executionOrder: 0
  icon: {instanceID: 0}
  userData: 
  assetBundleName: 
  assetBundleVariant: 
METACS
                ;;
            unity|prefab|asset|mat|anim|controller|mask|playable|renderTexture|physicMaterial|guiskin|flare|font|ttf|otf|png|jpg|jpeg|bmp|tga|psd|wav|mp3|ogg|mp4|avi|mov|fbx|obj|dll|json|xml|txt|csv|yaml|yml|shader|cginc|hlsl|compute|cs.meta|asmdef|asmref|rsp)
                cat > "$path.meta" <<METADEFAULT
fileFormatVersion: 2
guid: $guid
NativeFormatImporter:
  externalObjects: {}
  mainObjectFileID: 0
  userData: 
  assetBundleName: 
  assetBundleVariant: 
METADEFAULT
                ;;
            *)
                cat > "$path.meta" <<METADEFAULT2
fileFormatVersion: 2
guid: $guid
DefaultImporter:
  externalObjects: {}
  userData: 
  assetBundleName: 
  assetBundleVariant: 
METADEFAULT2
                ;;
        esac
    fi
}

# 递归处理所有文件和文件夹（排除 .git, .meta, Packages, ProjectSettings）
find . -not -path './.git/*' -not -path './Packages/*' -not -path './ProjectSettings/*' -not -path './generate_meta.sh' -not -name '*.meta' | while read -r item; do
    if [ ! -f "$item.meta" ] && [ ! -d "$item.meta" ]; then
        generate_meta "$item"
    fi
done

echo "Done generating .meta files"
