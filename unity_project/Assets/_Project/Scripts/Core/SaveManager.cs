using UnityEngine;
using System;
using System.IO;

namespace BurstFishingKingdom.Core
{
    /// <summary>
    /// 存档管理器 - JSON存档系统
    /// </summary>
    public class SaveManager : MonoBehaviour
    {
        private string SavePath => Path.Combine(Application.persistentDataPath, "save.json");
        private string BackupPath => Path.Combine(Application.persistentDataPath, $"save_{DateTime.Now:yyyyMMdd_HHmmss}.bak");

        /// <summary>
        /// 保存游戏
        /// </summary>
        public void SaveGame()
        {
            var data = GameManager.Instance.PlayerData?.ToSaveData();
            if (data == null) return;

            // 备份旧存档
            if (File.Exists(SavePath))
            {
                File.Copy(SavePath, BackupPath, overwrite: true);
            }

            string json = JsonUtility.ToJson(data, prettyPrint: true);
            File.WriteAllText(SavePath, json);
            
            Debug.Log($"[SaveManager] 游戏已保存: {SavePath}");
        }

        /// <summary>
        /// 尝试加载游戏
        /// </summary>
        public bool TryLoadGame()
        {
            if (!File.Exists(SavePath))
            {
                Debug.Log("[SaveManager] 没有找到存档，创建新游戏");
                return false;
            }

            try
            {
                string json = File.ReadAllText(SavePath);
                var data = JsonUtility.FromJson<PlayerSaveData>(json);
                GameManager.Instance.PlayerData?.LoadFromSaveData(data);
                
                // 计算离线收益
                GameManager.Instance.OfflineReward?.CalculateAndShow(data.LastSaveTime);
                
                Debug.Log("[SaveManager] 存档加载成功");
                return true;
            }
            catch (Exception e)
            {
                Debug.LogError($"[SaveManager] 加载存档失败: {e.Message}");
                return false;
            }
        }
    }

    /// <summary>
    /// 存档数据结构
    /// </summary>
    [Serializable]
    public class PlayerSaveData
    {
        public string PlayerName;
        public string PlayerGender;
        public int Level;
        public int Exp;
        public int Gold;
        public int Shame;
        
        // 外观
        public int SkinToneIndex;
        public int HairStyleIndex;
        public int HairColorIndex;
        public int EyeColorIndex;
        
        // 装备
        public string EquippedUnderwearId;
        public string EquippedSocksId;
        public string EquippedBottomId;
        public string EquippedTopId;
        public string EquippedAccessoryId;
        public string EquippedWeaponId;
        
        // 背包
        public InventorySlotSaveData[] InventorySlots;
        
        // NPC关系
        public NPCRelationSaveData[] NPCRelations;
        
        // 婚姻
        public string SpouseId;
        public int MarriageDays;
        public string ActiveCrewId;
        
        // 天赋
        public TalentSaveData[] Talents;
        
        // 时间
        public string LastSaveTime;
        public int CurrentGameHour;
        public int TotalPlayDays;
        
        // 船只/房屋
        public int CurrentShipLevel;
        public string CurrentCityId;
    }

    [Serializable]
    public class InventorySlotSaveData
    {
        public string ItemId;
        public int Count;
        public int Quality;
    }

    [Serializable]
    public class NPCRelationSaveData
    {
        public string NPCId;
        public int Favor;
        public int Stage;
        public string CurrentOutfit;
    }

    [Serializable]
    public class TalentSaveData
    {
        public string TalentId;
        public int Level;
    }
}
