using UnityEngine;
using System;

namespace BurstFishingKingdom.Core
{
    /// <summary>
    /// 船舱系统
    /// 管理船舱格子：床（休息）、衣橱（换装）、AI制衣台、空位
    /// </summary>
    public class ShipCabinSystem : MonoBehaviour
    {
        public static ShipCabinSystem Instance { get; private set; }

        [Header("船舱等级")]
        public int CabinLevel = 1;
        public int MaxFurnitureSlots = 4;

        [Header("家具状态")]
        public bool HasBed = true;
        public bool HasWardrobe = true;
        public bool HasCraftingTable = true;
        public int EmptySlots = 1;

        [Header("休息配置")]
        public float RestHourCost = 4f;
        public int RestHpRecovery = 50;
        public int RestShameReduction = 20;

        public event Action OnFurnitureChanged;
        public event Action OnRestComplete;

        private void Awake()
        {
            if (Instance != null && Instance != this) { Destroy(gameObject); return; }
            Instance = this;
        }

        /// <summary>
        /// 休息 - 推进时间，恢复状态
        /// </summary>
        public void Rest()
        {
            var timeManager = FindObjectOfType<TimeManager>();
            var playerData = GameManager.Instance.PlayerData;

            // 推进时间
            timeManager?.AdvanceHour(Mathf.FloorToInt(RestHourCost));

            // 恢复状态
            playerData.SetShame(Mathf.Max(0, playerData.Shame - RestShameReduction));

            OnRestComplete?.Invoke();
            Debug.Log("[ShipCabin] 休息完毕，羞耻值下降，精神焕发！");
        }

        /// <summary>
        /// 升级船舱
        /// </summary>
        public bool UpgradeCabin()
        {
            int cost = GetUpgradeCost();
            var playerData = GameManager.Instance.PlayerData;
            if (playerData.Gold < cost) return false;

            playerData.AddGold(-cost);
            CabinLevel++;
            MaxFurnitureSlots += 2;
            EmptySlots += 2;

            OnFurnitureChanged?.Invoke();
            Debug.Log($"[ShipCabin] 船舱升级到 Lv.{CabinLevel}");
            return true;
        }

        /// <summary>
        /// 添加家具
        /// </summary>
        public bool AddFurniture(string furnitureId)
        {
            if (EmptySlots <= 0) return false;

            switch (furnitureId)
            {
                case "bed":
                    if (HasBed) return false;
                    HasBed = true;
                    break;
                case "wardrobe":
                    if (HasWardrobe) return false;
                    HasWardrobe = true;
                    break;
                case "crafting_table":
                    if (HasCraftingTable) return false;
                    HasCraftingTable = true;
                    break;
                default:
                    return false;
            }

            EmptySlots--;
            OnFurnitureChanged?.Invoke();
            return true;
        }

        public int GetUpgradeCost()
        {
            return CabinLevel * 1000;
        }
    }
}
