using UnityEngine;

namespace BurstFishingKingdom.Equipment
{
    /// <summary>
    /// 衣服物品 ScriptableObject
    /// 每件衣服包含3个耐久阶段的Sprite
    /// </summary>
    [CreateAssetMenu(fileName = "NewClothing", menuName = "若若的钓鱼王国/衣服")]
    public class ClothingItemSO : ScriptableObject
    {
        [Header("基础信息")]
        public string ItemId;
        public string ItemName;
        [TextArea(2, 4)] public string Description;
        public EquipmentSlot Slot;
        public ItemQuality Quality = ItemQuality.Common;

        [Header("属性")]
        public int MaxDurability = 100;
        public int Defense = 0;
        public int Attack = 0;
        public int Charm = 0;

        [Header("Sprite (按破损阶段)")]
        [Tooltip("完整状态")] public Sprite NormalSprite;
        [Tooltip("轻微破损")] public Sprite DamagedSprite;
        [Tooltip("严重破损")] public Sprite BrokenSprite;

        [Header("制衣信息")]
        [Tooltip("AI生成的原料列表")]
        public CraftingMaterial[] Materials;
        [Tooltip("需要的制衣等级")]
        public int RequiredCraftingLevel = 1;

        [Header("外观颜色")]
        public Color PrimaryColor = Color.white;
        public Color SecondaryColor = Color.white;

        /// <summary>
        /// 获取品质颜色
        /// </summary>
        public Color GetQualityColor()
        {
            return Quality switch
            {
                ItemQuality.Common => new Color(0.89f, 0.91f, 0.94f),      // #e2e8f0
                ItemQuality.Uncommon => new Color(0.51f, 0.87f, 0.51f),    // #4ade80
                ItemQuality.Rare => new Color(0.23f, 0.51f, 0.96f),        // #3b82f6
                ItemQuality.Epic => new Color(0.66f, 0.33f, 0.97f),        // #a855f7
                ItemQuality.Legendary => new Color(0.98f, 0.45f, 0.09f),   // #f97316
                ItemQuality.Mythic => new Color(0.98f, 0.80f, 0.08f),      // #facc15
                _ => Color.white
            };
        }

        /// <summary>
        /// 获取品质名称
        /// </summary>
        public string GetQualityName()
        {
            return Quality switch
            {
                ItemQuality.Common => "普通",
                ItemQuality.Uncommon => "优质",
                ItemQuality.Rare => "稀有",
                ItemQuality.Epic => "史诗",
                ItemQuality.Legendary => "传说",
                ItemQuality.Mythic => "神话",
                _ => "未知"
            };
        }
    }

    [System.Serializable]
    public class CraftingMaterial
    {
        public string MaterialId;
        public string MaterialName;
        public int RequiredAmount;
        public ItemQuality MinQuality;
        public string ObtainHint;
    }
}
