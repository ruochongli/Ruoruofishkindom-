using UnityEngine;
using System;
using System.Collections.Generic;

namespace BurstFishingKingdom.Core
{
    /// <summary>
    /// 城市系统
    /// 管理城市列表、解锁条件、NPC位置
    /// </summary>
    public class CitySystem : MonoBehaviour
    {
        public static CitySystem Instance { get; private set; }

        [Header("城市列表")]
        public List<CityData> Cities = new();

        [Header("当前城市")]
        public string CurrentCityId = "breeze_harbor";

        public event Action<string> OnCityChanged;
        public event Action<string> OnCityUnlocked;

        private void Awake()
        {
            if (Instance != null && Instance != this) { Destroy(gameObject); return; }
            Instance = this;
            InitializeCities();
        }

        private void InitializeCities()
        {
            Cities = new List<CityData>
            {
                new CityData
                {
                    CityId = "breeze_harbor",
                    CityName = "宁静港湾村",
                    Description = "新手渔村，温暖而宁静。",
                    Climate = ClimateType.Temperate,
                    IsUnlocked = true,
                    AvailableNPCs = new List<string> { "lily", "hein" },
                    ShopLevel = 1
                },
                new CityData
                {
                    CityId = "magma_port",
                    CityName = "熔岩港",
                    Description = "火山脚下的港口，盛产火属性材料。",
                    Climate = ClimateType.Volcanic,
                    IsUnlocked = false,
                    UnlockCondition = "击败溪流鲤鱼王",
                    AvailableNPCs = new List<string>(),
                    ShopLevel = 2
                },
                new CityData
                {
                    CityId = "crystal_town",
                    CityName = "冰晶镇",
                    Description = "寒带小镇，可以看到极光。",
                    Climate = ClimateType.Arctic,
                    IsUnlocked = false,
                    UnlockCondition = "拥有2级船只",
                    AvailableNPCs = new List<string>(),
                    ShopLevel = 2
                },
                new CityData
                {
                    CityId = "emerald_city",
                    CityName = "翡翠城",
                    Description = "雨林深处的城市，珍稀花卉的产地。",
                    Climate = ClimateType.Tropical,
                    IsUnlocked = false,
                    UnlockCondition = "完成莉莉任务线",
                    AvailableNPCs = new List<string>(),
                    ShopLevel = 3
                },
                new CityData
                {
                    CityId = "pearl_bay",
                    CityName = "珍珠湾",
                    Description = "深海港口，史诗BOSS的栖息地。",
                    Climate = ClimateType.DeepSea,
                    IsUnlocked = false,
                    UnlockCondition = "拥有3级船只",
                    AvailableNPCs = new List<string>(),
                    ShopLevel = 4
                }
            };
        }

        /// <summary>
        /// 切换到指定城市
        /// </summary>
        public void TravelToCity(string cityId)
        {
            var city = Cities.Find(c => c.CityId == cityId);
            if (city == null || !city.IsUnlocked)
            {
                Debug.Log($"[CitySystem] 城市 {cityId} 未解锁");
                return;
            }

            CurrentCityId = cityId;
            GameManager.Instance.PlayerData.CurrentCityId = cityId;
            OnCityChanged?.Invoke(cityId);
            Debug.Log($"[CitySystem] 抵达 {city.CityName}");
        }

        /// <summary>
        /// 检查并解锁城市
        /// </summary>
        public void CheckUnlockConditions()
        {
            var player = GameManager.Instance.PlayerData;
            foreach (var city in Cities)
            {
                if (city.IsUnlocked) continue;

                bool canUnlock = false;
                switch (city.CityId)
                {
                    case "crystal_town":
                        canUnlock = player.CurrentShipLevel >= 2;
                        break;
                    case "pearl_bay":
                        canUnlock = player.CurrentShipLevel >= 3;
                        break;
                }

                if (canUnlock)
                {
                    city.IsUnlocked = true;
                    OnCityUnlocked?.Invoke(city.CityId);
                    Debug.Log($"[CitySystem] 解锁新城市: {city.CityName}");
                }
            }
        }

        public CityData GetCurrentCity()
        {
            return Cities.Find(c => c.CityId == CurrentCityId);
        }
    }

    [Serializable]
    public class CityData
    {
        public string CityId;
        public string CityName;
        public string Description;
        public ClimateType Climate;
        public bool IsUnlocked;
        public string UnlockCondition;
        public List<string> AvailableNPCs;
        public int ShopLevel;
    }

    public enum ClimateType
    {
        Temperate,  // 温带
        Volcanic,   // 火山
        Arctic,     // 寒带
        Tropical,   // 雨林
        DeepSea     // 深海
    }
}
