using UnityEngine;
using System;
using System.Collections.Generic;

namespace BurstFishingKingdom.Equipment
{
    /// <summary>
    /// 装备管理器
    /// 管理6个装备槽，处理换装、耐久度、爆衣效果
    /// </summary>
    public class EquipmentManager : MonoBehaviour
    {
        [Header("装备槽")]
        [SerializeField] private ClothingItemSO _underwear;
        [SerializeField] private ClothingItemSO _socks;
        [SerializeField] private ClothingItemSO _bottom;
        [SerializeField] private ClothingItemSO _top;
        [SerializeField] private ClothingItemSO _accessory;
        [SerializeField] private ClothingItemSO _weapon;

        [Header("当前耐久度")]
        public Dictionary<EquipmentSlot, int> CurrentDurability = new();

        public event Action<EquipmentSlot, ClothingItemSO> OnEquipped;
        public event Action<EquipmentSlot, ClothingItemSO> OnUnequipped;
        public event Action<EquipmentSlot, int> OnDurabilityChanged;
        public event Action<EquipmentSlot, DurabilityStage> OnDurabilityStageChanged;

        private void Awake()
        {
            // 初始化耐久度字典
            foreach (EquipmentSlot slot in Enum.GetValues(typeof(EquipmentSlot)))
            {
                CurrentDurability[slot] = GetEquipped(slot)?.MaxDurability ?? 0;
            }
        }

        /// <summary>
        /// 装备物品到指定槽位
        /// </summary>
        public void Equip(EquipmentSlot slot, ClothingItemSO item)
        {
            if (item != null && item.Slot != slot)
            {
                Debug.LogWarning($"[EquipmentManager] 物品 {item.ItemName} 不能装备到 {slot}");
                return;
            }

            // 卸下旧装备
            var oldItem = GetEquipped(slot);
            if (oldItem != null)
            {
                OnUnequipped?.Invoke(slot, oldItem);
            }

            // 装备新物品
            SetEquipped(slot, item);
            CurrentDurability[slot] = item?.MaxDurability ?? 0;
            
            // 更新外观
            UpdateAppearance(slot, item);
            
            OnEquipped?.Invoke(slot, item);
            Debug.Log($"[EquipmentManager] 装备 {item?.ItemName} 到 {slot}");
        }

        /// <summary>
        /// 卸下指定槽位的装备
        /// </summary>
        public void Unequip(EquipmentSlot slot)
        {
            var item = GetEquipped(slot);
            if (item == null) return;
            
            SetEquipped(slot, null);
            CurrentDurability[slot] = 0;
            UpdateAppearance(slot, null);
            
            OnUnequipped?.Invoke(slot, item);
        }

        /// <summary>
        /// 对装备造成伤害（磨损）
        /// </summary>
        public void TakeDamage(EquipmentSlot slot, int damage)
        {
            if (!CurrentDurability.ContainsKey(slot)) return;
            
            var item = GetEquipped(slot);
            if (item == null) return;

            int defense = item.Defense;
            int actualDamage = Mathf.Max(damage - defense, 1);
            
            int before = CurrentDurability[slot];
            CurrentDurability[slot] = Mathf.Max(0, CurrentDurability[slot] - actualDamage);
            int after = CurrentDurability[slot];

            OnDurabilityChanged?.Invoke(slot, CurrentDurability[slot]);

            // 检查阶段变化
            var oldStage = GetDurabilityStage(before, item.MaxDurability);
            var newStage = GetDurabilityStage(after, item.MaxDurability);
            if (oldStage != newStage)
            {
                OnDurabilityStageChanged?.Invoke(slot, newStage);
                UpdateDurabilityVisual(slot, newStage);
            }

            Debug.Log($"[EquipmentManager] {slot} 受到 {actualDamage} 磨损，剩余 {after}/{item.MaxDurability}");
        }

        /// <summary>
        /// 修复装备
        /// </summary>
        public void Repair(EquipmentSlot slot, int amount)
        {
            var item = GetEquipped(slot);
            if (item == null) return;
            
            CurrentDurability[slot] = Mathf.Min(CurrentDurability[slot] + amount, item.MaxDurability);
            OnDurabilityChanged?.Invoke(slot, CurrentDurability[slot]);
            UpdateDurabilityVisual(slot, DurabilityStage.Full);
        }

        /// <summary>
        /// 获取装备ID（用于存档）
        /// </summary>
        public string GetEquippedId(EquipmentSlot slot)
        {
            return GetEquipped(slot)?.ItemId ?? "";
        }

        /// <summary>
        /// 获取已装备物品
        /// </summary>
        public ClothingItemSO GetEquipped(EquipmentSlot slot)
        {
            return slot switch
            {
                EquipmentSlot.Underwear => _underwear,
                EquipmentSlot.Socks => _socks,
                EquipmentSlot.Bottom => _bottom,
                EquipmentSlot.Top => _top,
                EquipmentSlot.Accessory => _accessory,
                EquipmentSlot.Weapon => _weapon,
                _ => null
            };
        }

        /// <summary>
        /// 获取总防御值
        /// </summary>
        public int GetTotalDefense()
        {
            int total = 0;
            foreach (EquipmentSlot slot in Enum.GetValues(typeof(EquipmentSlot)))
            {
                total += GetEquipped(slot)?.Defense ?? 0;
            }
            return total;
        }

        /// <summary>
        /// 获取总攻击力
        /// </summary>
        public int GetTotalAttack()
        {
            int total = 0;
            foreach (EquipmentSlot slot in Enum.GetValues(typeof(EquipmentSlot)))
            {
                total += GetEquipped(slot)?.Attack ?? 0;
            }
            return total;
        }

        private void SetEquipped(EquipmentSlot slot, ClothingItemSO item)
        {
            switch (slot)
            {
                case EquipmentSlot.Underwear: _underwear = item; break;
                case EquipmentSlot.Socks: _socks = item; break;
                case EquipmentSlot.Bottom: _bottom = item; break;
                case EquipmentSlot.Top: _top = item; break;
                case EquipmentSlot.Accessory: _accessory = item; break;
                case EquipmentSlot.Weapon: _weapon = item; break;
            }
        }

        /// <summary>
        /// 获取耐久度阶段（4阶段：完整/轻微破损/中度破损/完全损坏）
        /// </summary>
        public DurabilityStage GetDurabilityStage(int current, int max)
        {
            if (max == 0) return DurabilityStage.Full;
            float ratio = (float)current / max;
            if (ratio <= 0) return DurabilityStage.Destroyed;
            if (ratio <= 0.15f) return DurabilityStage.Broken;
            if (ratio <= 0.45f) return DurabilityStage.Damaged;
            return DurabilityStage.Full;
        }

        private void UpdateAppearance(EquipmentSlot slot, ClothingItemSO item)
        {
            var appearance = GetComponent<Player.PlayerAppearance>();
            if (appearance == null) return;
            
            Sprite sprite = item?.NormalSprite;
            appearance.SetClothingSprite(slot, sprite);
        }

        private void UpdateDurabilityVisual(EquipmentSlot slot, DurabilityStage stage)
        {
            var appearance = GetComponent<Player.PlayerAppearance>();
            if (appearance == null) return;

            var item = GetEquipped(slot);
            if (item == null) return;

            Sprite sprite = stage switch
            {
                DurabilityStage.Full => item.NormalSprite,
                DurabilityStage.Damaged => item.DamagedSprite ?? item.NormalSprite,
                DurabilityStage.Broken => item.BrokenSprite ?? item.DamagedSprite ?? item.NormalSprite,
                DurabilityStage.Destroyed => null,
                _ => item.NormalSprite
            };

            appearance.SetClothingSprite(slot, sprite);
        }
    }
}
