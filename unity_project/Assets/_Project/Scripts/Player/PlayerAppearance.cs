using UnityEngine;

namespace BurstFishingKingdom.Player
{
    /// <summary>
    /// 玩家外观管理器
    /// 管理角色捏脸参数和换装渲染
    /// </summary>
    public class PlayerAppearance : MonoBehaviour
    {
        [Header("捏脸参数")]
        public int SkinToneIndex = 2;
        public int HairStyleIndex = 0;
        public int HairColorIndex = 0;
        public int EyeColorIndex = 0;
        public int FaceShapeIndex = 0;
        public int EyebrowStyleIndex = 0;
        public int MouthStyleIndex = 0;

        [Header("颜色预设")]
        public Color[] SkinTones = new Color[]
        {
            new Color(0.96f, 0.81f, 0.77f),
            new Color(0.91f, 0.71f, 0.63f),
            new Color(0.83f, 0.64f, 0.45f),
            new Color(0.78f, 0.53f, 0.26f),
            new Color(0.55f, 0.33f, 0.14f),
            new Color(0.24f, 0.14f, 0.08f),
        };
        public Color[] HairColors = new Color[]
        {
            new Color(0.36f, 0.23f, 0.13f),  // 棕
            new Color(0.18f, 0.18f, 0.18f),  // 黑
            new Color(0.83f, 0.63f, 0.09f),  // 金
            new Color(0.75f, 0.22f, 0.17f),  // 红
            new Color(0.56f, 0.27f, 0.68f),  // 紫
            new Color(0.16f, 0.50f, 0.72f),  // 蓝
            new Color(0.15f, 0.68f, 0.38f),  // 绿
            new Color(0.93f, 0.94f, 0.95f),  // 白/银
            new Color(0.91f, 0.12f, 0.39f),  // 粉
            new Color(1.00f, 0.60f, 0.00f),  // 橙
        };
        public Color[] EyeColors = new Color[]
        {
            new Color(0.23f, 0.51f, 0.96f),  // 蓝
            new Color(0.13f, 0.77f, 0.37f),  // 绿
            new Color(0.66f, 0.33f, 0.97f),  // 紫
            new Color(0.94f, 0.27f, 0.27f),  // 红
            new Color(0.96f, 0.62f, 0.04f),  // 金
            new Color(0.08f, 0.72f, 0.65f),  // 青
            new Color(0.39f, 0.40f, 0.95f),  // 靛
            new Color(0.93f, 0.27f, 0.60f),  // 粉
        };

        [Header("换装渲染器")]
        public SpriteRenderer BodyRenderer;
        public SpriteRenderer UnderwearRenderer;
        public SpriteRenderer SocksRenderer;
        public SpriteRenderer BottomRenderer;
        public SpriteRenderer TopRenderer;
        public SpriteRenderer AccessoryRenderer;
        public SpriteRenderer HairBackRenderer;
        public SpriteRenderer HairFrontRenderer;
        public SpriteRenderer FaceRenderer;

        [Header("Sorting Group")]
        public SortingGroup SortingGroup;

        /// <summary>
        /// 更新外观颜色（不使用Sprite时）
        /// </summary>
        public void UpdateColors()
        {
            if (BodyRenderer != null)
                BodyRenderer.color = SkinTones[Mathf.Clamp(SkinToneIndex, 0, SkinTones.Length - 1)];
            
            Color hairColor = HairColors[Mathf.Clamp(HairColorIndex, 0, HairColors.Length - 1)];
            if (HairBackRenderer != null) HairBackRenderer.color = hairColor;
            if (HairFrontRenderer != null) HairFrontRenderer.color = hairColor;
            
            if (FaceRenderer != null)
                FaceRenderer.color = EyeColors[Mathf.Clamp(EyeColorIndex, 0, EyeColors.Length - 1)];
        }

        /// <summary>
        /// 设置某部位的Sprite
        /// </summary>
        public void SetClothingSprite(Equipment.EquipmentSlot slot, Sprite sprite)
        {
            switch (slot)
            {
                case Equipment.EquipmentSlot.Underwear:
                    if (UnderwearRenderer != null) UnderwearRenderer.sprite = sprite;
                    break;
                case Equipment.EquipmentSlot.Socks:
                    if (SocksRenderer != null) SocksRenderer.sprite = sprite;
                    break;
                case Equipment.EquipmentSlot.Bottom:
                    if (BottomRenderer != null) BottomRenderer.sprite = sprite;
                    break;
                case Equipment.EquipmentSlot.Top:
                    if (TopRenderer != null) TopRenderer.sprite = sprite;
                    break;
                case Equipment.EquipmentSlot.Accessory:
                    if (AccessoryRenderer != null) AccessoryRenderer.sprite = sprite;
                    break;
            }
        }
    }
}
