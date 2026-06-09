namespace BurstFishingKingdom.Equipment
{
    /// <summary>
    /// 装备部位枚举
    /// 从内衣到外套的分层结构，支持爆衣系统的逐层剥离
    /// </summary>
    public enum EquipmentSlot
    {
        Underwear,   // 内衣 - 最内层，最后才损坏
        Socks,       // 袜子/长筒袜
        Bottom,      // 裙子/裤子/下装
        Top,         // 上衣/外套
        Accessory,   // 饰品（头饰、项链、戒指等）
        Weapon       // 鱼竿/战斗武器
    }

    /// <summary>
    /// 装备品质枚举
    /// </summary>
    public enum ItemQuality
    {
        Common = 0,      // 普通 - 白色
        Uncommon = 1,    // 优质 - 绿色
        Rare = 2,        // 稀有 - 蓝色
        Epic = 3,        // 史诗 - 紫色
        Legendary = 4,   // 传说 - 橙色
        Mythic = 5       // 神话 - 金色
    }

    /// <summary>
    /// 衣服的破损阶段
    /// </summary>
    public enum DurabilityStage
    {
        Full,       // 完整
        Damaged,    // 轻微破损
        Broken,     // 严重破损
        Destroyed   // 完全损坏
    }
}
