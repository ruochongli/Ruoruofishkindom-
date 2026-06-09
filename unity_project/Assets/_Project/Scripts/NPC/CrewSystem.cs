using UnityEngine;
using System;

namespace BurstFishingKingdom.NPC
{
    /// <summary>
    /// 船员系统
    /// 管理婚后配偶作为船员的功能：DPS输出、战后修补
    /// </summary>
    public class CrewSystem : MonoBehaviour
    {
        [Header("当前船员")]
        public NPCData ActiveCrew;
        
        [Header("婚姻数据")]
        public string SpouseId;
        public int MarriageDays = 0;
        public bool RepairUsedThisTrip = false;

        public event Action OnCrewChanged;
        public event Action<int> OnCrewAttacked;
        public event Action OnCrewRepaired;

        /// <summary>
        /// 是否有活跃船员
        /// </summary>
        public bool HasActiveCrew() => ActiveCrew != null;

        /// <summary>
        /// 获取当前船员
        /// </summary>
        public NPCData GetActiveCrew() => ActiveCrew;

        /// <summary>
        /// 设置船员
        /// </summary>
        public void SetCrew(NPCData npc)
        {
            ActiveCrew = npc;
            OnCrewChanged?.Invoke();
        }

        /// <summary>
        /// 移除船员
        /// </summary>
        public void RemoveCrew()
        {
            ActiveCrew = null;
            OnCrewChanged?.Invoke();
        }

        /// <summary>
        /// 获取当前DPS（含婚姻天数加成）
        /// </summary>
        public int GetCurrentDPS()
        {
            if (ActiveCrew?.CombatData == null) return 0;
            
            float multiplier = MarriageDays switch
            {
                >= 180 => 2.0f,
                >= 90 => 1.5f,
                >= 30 => 1.2f,
                _ => 1.0f
            };

            // 天赋加成
            var talentSystem = FindObjectOfType<Player.TalentSystem>();
            if (talentSystem != null) multiplier *= talentSystem.GetCrewMultiplier();

            return Mathf.FloorToInt(ActiveCrew.CombatData.BaseDPS * multiplier);
        }

        /// <summary>
        /// 获取当前修补百分比
        /// </summary>
        public float GetCurrentRepairPercent()
        {
            if (ActiveCrew?.CombatData == null) return 0f;
            
            float multiplier = MarriageDays switch
            {
                >= 180 => 2.0f,
                >= 90 => 1.6f,
                >= 30 => 1.3f,
                _ => 1.0f
            };

            return Mathf.Min(ActiveCrew.CombatData.BaseRepairPercent * multiplier, 0.5f);
        }

        /// <summary>
        /// 战后修补玩家衣服
        /// </summary>
        public void RepairPlayerClothes()
        {
            if (ActiveCrew == null) return;
            if (RepairUsedThisTrip) return;

            var equipManager = GameManager.Instance.PlayerData.GetComponent<Equipment.EquipmentManager>();
            float repairPct = GetCurrentRepairPercent();

            foreach (Equipment.EquipmentSlot slot in System.Enum.GetValues(typeof(Equipment.EquipmentSlot)))
            {
                var item = equipManager.GetEquipped(slot);
                if (item == null) continue;
                
                int repairAmount = Mathf.FloorToInt(item.MaxDurability * repairPct);
                equipManager.Repair(slot, repairAmount);
            }

            RepairUsedThisTrip = true;
            OnCrewRepaired?.Invoke();
            
            // 随机台词
            var line = ActiveCrew.CombatData.RepairLines[UnityEngine.Random.Range(0, ActiveCrew.CombatData.RepairLines.Length)];
            Debug.Log($"💕 {ActiveCrew.Name}: \"{line}\"");
        }

        /// <summary>
        /// 出海前重置修补状态
        /// </summary>
        public void ResetRepairStatus()
        {
            RepairUsedThisTrip = false;
        }

        /// <summary>
        /// 增加婚姻天数
        /// </summary>
        public void AddMarriageDay()
        {
            MarriageDays++;
        }
    }
}
