using UnityEngine;
using System;
using System.Collections.Generic;
using System.Linq;

namespace BurstFishingKingdom.Core
{
    /// <summary>
    /// 每日商店系统
    /// 每天自动刷新6-8个商品，支持手动刷新
    /// </summary>
    public class DailyShopSystem : MonoBehaviour
    {
        public static DailyShopSystem Instance { get; private set; }

        [Header("商品池")]
        public List<ShopItemPool> ItemPools = new();

        [Header("当前商品")]
        public List<ShopItemEntry> CurrentItems = new();
        public int MaxItems = 8;
        public int MinItems = 6;

        [Header("刷新配置")]
        public int BaseRefreshCost = 100;
        public int MaxRefreshTimes = 10;
        public int TodayRefreshCount = 0;

        [Header("概率分布")]
        public QualityWeight[] QualityWeights =
        {
            new QualityWeight { Quality = Equipment.ItemQuality.Common, Weight = 400 },
            new QualityWeight { Quality = Equipment.ItemQuality.Uncommon, Weight = 300 },
            new QualityWeight { Quality = Equipment.ItemQuality.Rare, Weight = 180 },
            new QualityWeight { Quality = Equipment.ItemQuality.Epic, Weight = 80 },
            new QualityWeight { Quality = Equipment.ItemQuality.Legendary, Weight = 30 },
            new QualityWeight { Quality = Equipment.ItemQuality.Mythic, Weight = 10 },
        };

        public event Action OnShopRefreshed;
        public event Action<int> OnRefreshCostChanged;

        private int _lastRefreshDay = -1;

        private void Awake()
        {
            if (Instance != null && Instance != this) { Destroy(gameObject); return; }
            Instance = this;
        }

        private void Start()
        {
            var timeManager = FindObjectOfType<TimeManager>();
            if (timeManager != null)
            {
                timeManager.OnDayChanged += OnDayChanged;
            }

            // 初始刷新
            if (CurrentItems.Count == 0)
            {
                RefreshShop();
            }
        }

        private void OnDayChanged(int day)
        {
            if (day != _lastRefreshDay)
            {
                _lastRefreshDay = day;
                TodayRefreshCount = 0;
                RefreshShop();
            }
        }

        /// <summary>
        /// 自动刷新商店（每天）
        /// </summary>
        public void RefreshShop()
        {
            CurrentItems.Clear();
            int itemCount = UnityEngine.Random.Range(MinItems, MaxItems + 1);

            for (int i = 0; i < itemCount; i++)
            {
                var entry = GenerateRandomItem();
                if (entry != null)
                    CurrentItems.Add(entry);
            }

            OnShopRefreshed?.Invoke();
            Debug.Log($"[DailyShop] 商店已刷新，共 {CurrentItems.Count} 件商品");
        }

        /// <summary>
        /// 手动刷新（消耗金币）
        /// </summary>
        public bool ManualRefresh()
        {
            if (TodayRefreshCount >= MaxRefreshTimes)
            {
                Debug.Log("[DailyShop] 今日刷新次数已用完");
                return false;
            }

            int cost = GetCurrentRefreshCost();
            var playerData = GameManager.Instance.PlayerData;
            if (playerData.Gold < cost)
            {
                Debug.Log("[DailyShop] 金币不足");
                return false;
            }

            playerData.AddGold(-cost);
            TodayRefreshCount++;
            RefreshShop();
            OnRefreshCostChanged?.Invoke(GetCurrentRefreshCost());
            return true;
        }

        /// <summary>
        /// 购买商品
        /// </summary>
        public bool BuyItem(int index)
        {
            if (index < 0 || index >= CurrentItems.Count) return false;
            var entry = CurrentItems[index];
            if (entry.SoldOut) return false;

            var playerData = GameManager.Instance.PlayerData;
            if (playerData.Gold < entry.Price) return false;

            playerData.AddGold(-entry.Price);

            // 添加到背包
            var inventory = playerData.Inventory;
            if (entry.IsClothing && entry.ClothingItem != null)
            {
                // 衣服直接装备或放入背包
                inventory.AddItem(CreateItemSOFromClothing(entry.ClothingItem), 1, entry.Quality);
            }
            else if (entry.MaterialItem != null)
            {
                inventory.AddItem(entry.MaterialItem, entry.Count, entry.Quality);
            }

            entry.SoldOut = true;
            Debug.Log($"[DailyShop] 购买 {entry.DisplayName} x{entry.Count}");
            return true;
        }

        private ShopItemEntry GenerateRandomItem()
        {
            var quality = RollQuality();
            var pool = ItemPools.Find(p => p.TargetQuality == quality);
            if (pool == null || pool.Items.Count == 0) return null;

            var item = pool.Items[UnityEngine.Random.Range(0, pool.Items.Count)];
            int price = CalculatePrice(item, quality);
            int count = UnityEngine.Random.Range(1, 4);

            return new ShopItemEntry
            {
                DisplayName = item.ItemName,
                Price = price,
                Count = count,
                Quality = quality,
                IsClothing = item is Equipment.ClothingItemSO,
                ClothingItem = item as Equipment.ClothingItemSO,
                MaterialItem = item as Inventory.ItemSO,
                SoldOut = false
            };
        }

        private Equipment.ItemQuality RollQuality()
        {
            int totalWeight = QualityWeights.Sum(w => w.Weight);
            int roll = UnityEngine.Random.Range(0, totalWeight);
            int cumulative = 0;

            foreach (var qw in QualityWeights)
            {
                cumulative += qw.Weight;
                if (roll < cumulative)
                    return qw.Quality;
            }
            return Equipment.ItemQuality.Common;
        }

        private int CalculatePrice(Inventory.ItemSO item, Equipment.ItemQuality quality)
        {
            float multiplier = quality switch
            {
                Equipment.ItemQuality.Common => 1f,
                Equipment.ItemQuality.Uncommon => 1.5f,
                Equipment.ItemQuality.Rare => 2.5f,
                Equipment.ItemQuality.Epic => 5f,
                Equipment.ItemQuality.Legendary => 10f,
                Equipment.ItemQuality.Mythic => 25f,
                _ => 1f
            };
            return Mathf.FloorToInt((item?.SellPrice ?? 10) * multiplier);
        }

        public int GetCurrentRefreshCost()
        {
            return Mathf.FloorToInt(BaseRefreshCost * Mathf.Pow(2, TodayRefreshCount));
        }

        private Inventory.ItemSO CreateItemSOFromClothing(Equipment.ClothingItemSO clothing)
        {
            // 创建对应的物品SO（简化：直接引用或使用通用物品）
            // 实际项目中可以有一个 ClothingToItem 的映射
            return null;
        }
    }

    [Serializable]
    public class ShopItemPool
    {
        public Equipment.ItemQuality TargetQuality;
        public List<Inventory.ItemSO> Items = new();
    }

    [Serializable]
    public class ShopItemEntry
    {
        public string DisplayName;
        public int Price;
        public int Count;
        public Equipment.ItemQuality Quality;
        public bool IsClothing;
        public Equipment.ClothingItemSO ClothingItem;
        public Inventory.ItemSO MaterialItem;
        public bool SoldOut;
    }

    [Serializable]
    public class QualityWeight
    {
        public Equipment.ItemQuality Quality;
        public int Weight;
    }
}
