using UnityEngine;

namespace BurstFishingKingdom.Inventory
{
    /// <summary>
    /// 物品基类 ScriptableObject
    /// </summary>
    [CreateAssetMenu(fileName = "NewItem", menuName = "若若的钓鱼王国/物品")]
    public class ItemSO : ScriptableObject
    {
        public string ItemId;
        public string ItemName;
        [TextArea(2, 4)] public string Description;
        public Sprite Icon;
        public Equipment.ItemQuality Quality = Equipment.ItemQuality.Common;
        public int MaxStack = 99;
        public ItemCategory Category;
        public bool IsSellable = true;
        public int SellPrice = 10;
    }

    public enum ItemCategory
    {
        Material,    // 材料（布料、丝线等）
        Dye,         // 染料
        Fish,        // 鱼
        Food,        // 食物
        Tool,        // 工具
        Quest,       // 任务物品
        Currency     // 货币
    }
}
