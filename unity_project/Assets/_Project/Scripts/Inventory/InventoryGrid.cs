using UnityEngine;
using System;
using System.Collections.Generic;

namespace BurstFishingKingdom.Inventory
{
    /// <summary>
    /// 格子背包系统
    /// 类似星露谷的64格背包，支持拖拽和堆叠
    /// </summary>
    public class InventoryGrid : MonoBehaviour
    {
        [Header("背包配置")]
        public int GridWidth = 8;
        public int GridHeight = 8;
        public int MaxSlots => GridWidth * GridHeight;

        [Header("当前数据")]
        public List<InventorySlot> Slots = new();

        public event Action<int> OnSlotChanged;
        public event Action<ItemSO, int> OnItemAdded;
        public event Action<ItemSO, int> OnItemRemoved;

        private void Awake()
        {
            InitializeSlots();
        }

        private void InitializeSlots()
        {
            Slots.Clear();
            for (int i = 0; i < MaxSlots; i++)
            {
                Slots.Add(new InventorySlot { Index = i });
            }
        }

        /// <summary>
        /// 添加物品到背包
        /// </summary>
        /// <returns>成功添加的数量</returns>
        public int AddItem(ItemSO item, int count, Equipment.ItemQuality quality = Equipment.ItemQuality.Common)
        {
            if (item == null || count <= 0) return 0;

            int remaining = count;

            // 先尝试堆叠到已有物品
            if (item.MaxStack > 1)
            {
                for (int i = 0; i < MaxSlots && remaining > 0; i++)
                {
                    var slot = Slots[i];
                    if (slot.Item == item && slot.Quality == quality && slot.Count < item.MaxStack)
                    {
                        int canStack = Mathf.Min(remaining, item.MaxStack - slot.Count);
                        slot.Count += canStack;
                        remaining -= canStack;
                        OnSlotChanged?.Invoke(i);
                    }
                }
            }

            // 再放到空格子
            for (int i = 0; i < MaxSlots && remaining > 0; i++)
            {
                if (Slots[i].IsEmpty)
                {
                    Slots[i].Item = item;
                    Slots[i].Quality = quality;
                    Slots[i].Count = Mathf.Min(remaining, item.MaxStack);
                    remaining -= Slots[i].Count;
                    OnSlotChanged?.Invoke(i);
                }
            }

            int added = count - remaining;
            if (added > 0) OnItemAdded?.Invoke(item, added);
            
            if (remaining > 0)
            {
                Debug.LogWarning($"[InventoryGrid] 背包已满，{remaining}个{item.ItemName}无法放入");
            }
            
            return added;
        }

        /// <summary>
        /// 移除物品
        /// </summary>
        public bool RemoveItem(int slotIndex, int count = 1)
        {
            if (slotIndex < 0 || slotIndex >= MaxSlots) return false;
            
            var slot = Slots[slotIndex];
            if (slot.IsEmpty || slot.Count < count) return false;

            var item = slot.Item;
            slot.Count -= count;
            
            if (slot.Count <= 0)
            {
                slot.Clear();
            }
            
            OnSlotChanged?.Invoke(slotIndex);
            OnItemRemoved?.Invoke(item, count);
            return true;
        }

        /// <summary>
        /// 移动物品到另一个格子
        /// </summary>
        public bool MoveItem(int fromIndex, int toIndex)
        {
            if (fromIndex == toIndex) return false;
            if (fromIndex < 0 || fromIndex >= MaxSlots) return false;
            if (toIndex < 0 || toIndex >= MaxSlots) return false;

            var fromSlot = Slots[fromIndex];
            var toSlot = Slots[toIndex];

            if (fromSlot.IsEmpty) return false;

            // 目标为空，直接移动
            if (toSlot.IsEmpty)
            {
                Slots[toIndex] = fromSlot.Clone();
                Slots[fromIndex].Clear();
                OnSlotChanged?.Invoke(fromIndex);
                OnSlotChanged?.Invoke(toIndex);
                return true;
            }

            // 同类型可堆叠
            if (toSlot.Item == fromSlot.Item && toSlot.Quality == fromSlot.Quality && fromSlot.Item.MaxStack > 1)
            {
                int canStack = Mathf.Min(fromSlot.Count, fromSlot.Item.MaxStack - toSlot.Count);
                toSlot.Count += canStack;
                fromSlot.Count -= canStack;
                
                if (fromSlot.Count <= 0) fromSlot.Clear();
                
                OnSlotChanged?.Invoke(fromIndex);
                OnSlotChanged?.Invoke(toIndex);
                return true;
            }

            // 交换
            var temp = Slots[toIndex].Clone();
            Slots[toIndex] = fromSlot.Clone();
            Slots[fromIndex] = temp;
            OnSlotChanged?.Invoke(fromIndex);
            OnSlotChanged?.Invoke(toIndex);
            return true;
        }

        /// <summary>
        /// 获取物品总数量
        /// </summary>
        public int GetItemCount(string itemId)
        {
            int total = 0;
            foreach (var slot in Slots)
            {
                if (slot.Item != null && slot.Item.ItemId == itemId)
                    total += slot.Count;
            }
            return total;
        }

        /// <summary>
        /// 检查是否有足够材料
        /// </summary>
        public bool HasEnoughMaterials(string itemId, int requiredAmount)
        {
            return GetItemCount(itemId) >= requiredAmount;
        }

        /// <summary>
        /// 消耗材料
        /// </summary>
        public bool ConsumeMaterials(string itemId, int amount)
        {
            if (GetItemCount(itemId) < amount) return false;

            int remaining = amount;
            for (int i = 0; i < MaxSlots && remaining > 0; i++)
            {
                if (Slots[i].Item != null && Slots[i].Item.ItemId == itemId)
                {
                    int consume = Mathf.Min(remaining, Slots[i].Count);
                    RemoveItem(i, consume);
                    remaining -= consume;
                }
            }
            return remaining == 0;
        }
    }

    /// <summary>
    /// 单个格子数据
    /// </summary>
    [Serializable]
    public class InventorySlot
    {
        public int Index;
        public ItemSO Item;
        public int Count;
        public Equipment.ItemQuality Quality;

        public bool IsEmpty => Item == null || Count <= 0;

        public void Clear()
        {
            Item = null;
            Count = 0;
            Quality = Equipment.ItemQuality.Common;
        }

        public InventorySlot Clone()
        {
            return new InventorySlot
            {
                Index = this.Index,
                Item = this.Item,
                Count = this.Count,
                Quality = this.Quality
            };
        }
    }
}
