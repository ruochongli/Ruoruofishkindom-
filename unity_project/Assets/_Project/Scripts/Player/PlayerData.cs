using UnityEngine;
using System;

namespace BurstFishingKingdom.Player
{
    /// <summary>
    /// 玩家数据 - 所有玩家状态的中心存储
    /// </summary>
    public class PlayerData : MonoBehaviour
    {
        [Header("基础信息")]
        public string PlayerName = "冒险者";
        public Gender PlayerGender = Gender.Female;
        
        [Header("等级与资源")]
        public int Level = 1;
        public int CurrentExp = 0;
        public int ExpToNextLevel = 100;
        public int Gold = 500;
        
        [Header("外观")]
        public PlayerAppearance Appearance;
        
        [Header("装备")]
        public Equipment.EquipmentManager EquipmentManager;
        
        [Header("背包")]
        public Inventory.InventoryGrid Inventory;
        
        [Header("婚姻")]
        public string SpouseNPCId = "";
        public int MarriageDays = 0;
        public string ActiveCrewId = "";
        
        [Header("船只")]
        public int CurrentShipLevel = 1;
        public string CurrentCityId = "breeze_harbor";
        
        [Header("统计")]
        public int TotalFishCaught = 0;
        public int TotalBattlesWon = 0;
        public int TotalPlayTimeSeconds = 0;

        public event Action<int> OnGoldChanged;
        public event Action<int, int> OnExpChanged;
        public event Action<int> OnLevelUp;

        private void Awake()
        {
            Appearance = GetComponent<PlayerAppearance>();
            EquipmentManager = GetComponent<Equipment.EquipmentManager>();
        }

        private void Update()
        {
            TotalPlayTimeSeconds += Mathf.FloorToInt(Time.deltaTime);
        }

        public void AddGold(int amount)
        {
            Gold = Mathf.Max(0, Gold + amount);
            OnGoldChanged?.Invoke(Gold);
        }

        public void AddExp(int amount)
        {
            CurrentExp += amount;
            OnExpChanged?.Invoke(CurrentExp, ExpToNextLevel);
            
            while (CurrentExp >= ExpToNextLevel)
            {
                LevelUp();
            }
        }

        private void LevelUp()
        {
            CurrentExp -= ExpToNextLevel;
            Level++;
            ExpToNextLevel = Mathf.FloorToInt(ExpToNextLevel * 1.5f);
            OnLevelUp?.Invoke(Level);
            Debug.Log($"[PlayerData] 升级！当前等级: {Level}");
        }

        /// <summary>
        /// 导出存档数据
        /// </summary>
        public Core.PlayerSaveData ToSaveData()
        {
            return new Core.PlayerSaveData
            {
                PlayerName = PlayerName,
                PlayerGender = PlayerGender.ToString(),
                Level = Level,
                Exp = CurrentExp,
                Gold = Gold,
                SkinToneIndex = Appearance?.SkinToneIndex ?? 0,
                HairStyleIndex = Appearance?.HairStyleIndex ?? 0,
                HairColorIndex = Appearance?.HairColorIndex ?? 0,
                EyeColorIndex = Appearance?.EyeColorIndex ?? 0,
                EquippedUnderwearId = EquipmentManager?.GetEquippedId(Equipment.EquipmentSlot.Underwear),
                EquippedSocksId = EquipmentManager?.GetEquippedId(Equipment.EquipmentSlot.Socks),
                EquippedBottomId = EquipmentManager?.GetEquippedId(Equipment.EquipmentSlot.Bottom),
                EquippedTopId = EquipmentManager?.GetEquippedId(Equipment.EquipmentSlot.Top),
                EquippedAccessoryId = EquipmentManager?.GetEquippedId(Equipment.EquipmentSlot.Accessory),
                EquippedWeaponId = EquipmentManager?.GetEquippedId(Equipment.EquipmentSlot.Weapon),
                SpouseId = SpouseNPCId,
                MarriageDays = MarriageDays,
                ActiveCrewId = ActiveCrewId,
                LastSaveTime = DateTime.Now.ToString("O"),
                CurrentGameHour = FindObjectOfType<Core.TimeManager>()?.CurrentHour ?? 8,
                TotalPlayDays = FindObjectOfType<Core.TimeManager>()?.CurrentDay ?? 1,
                CurrentShipLevel = CurrentShipLevel,
                CurrentCityId = CurrentCityId,
            };
        }

        /// <summary>
        /// 从存档数据加载
        /// </summary>
        public void LoadFromSaveData(Core.PlayerSaveData data)
        {
            PlayerName = data.PlayerName;
            PlayerGender = (Gender)Enum.Parse(typeof(Gender), data.PlayerGender);
            Level = data.Level;
            CurrentExp = data.Exp;
            Gold = data.Gold;
            SpouseNPCId = data.SpouseId;
            MarriageDays = data.MarriageDays;
            ActiveCrewId = data.ActiveCrewId;
            CurrentShipLevel = data.CurrentShipLevel;
            CurrentCityId = data.CurrentCityId;
            
            if (Appearance != null)
            {
                Appearance.SkinToneIndex = data.SkinToneIndex;
                Appearance.HairStyleIndex = data.HairStyleIndex;
                Appearance.HairColorIndex = data.HairColorIndex;
                Appearance.EyeColorIndex = data.EyeColorIndex;
            }
        }
    }

    public enum Gender { Female, Male }
}
