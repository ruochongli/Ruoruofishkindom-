using UnityEngine;
using System;
using System.Collections.Generic;

namespace BurstFishingKingdom.Player
{
    /// <summary>
    /// 天赋系统
    /// 提供离线挂机收益和战斗被动加成
    /// </summary>
    public class TalentSystem : MonoBehaviour
    {
        public static TalentSystem Instance { get; private set; }

        [Header("天赋列表")]
        public List<Talent> Talents = new();

        [Header("基础挂机收益")]
        public float BaseGoldPerSecond = 0.1f;
        public float BaseExpPerSecond = 0.05f;

        public event Action<string, int> OnTalentUpgraded;

        private void Awake()
        {
            if (Instance != null && Instance != this) { Destroy(gameObject); return; }
            Instance = this;
            InitializeTalents();
        }

        private void InitializeTalents()
        {
            Talents = new List<Talent>
            {
                new Talent
                {
                    Id = "offline_gold",
                    Name = "深海渔夫",
                    Description = "即使在休息时，你也能从深海中获得金币。",
                    Icon = null,
                    MaxLevel = 10,
                    CurrentLevel = 0,
                    Category = TalentCategory.Idle,
                    BaseValue = 0.1f,
                    ValuePerLevel = 0.05f,
                    UpgradeCost = 100
                },
                new Talent
                {
                    Id = "offline_exp",
                    Name = "钓鱼直觉",
                    Description = "通过观察海流和鱼群，你的经验不断增长。",
                    Icon = null,
                    MaxLevel = 10,
                    CurrentLevel = 0,
                    Category = TalentCategory.Idle,
                    BaseValue = 0.05f,
                    ValuePerLevel = 0.03f,
                    UpgradeCost = 100
                },
                new Talent
                {
                    Id = "combat_damage",
                    Name = "战斗本能",
                    Description = "在危急时刻爆发出更强的战斗力。",
                    Icon = null,
                    MaxLevel = 5,
                    CurrentLevel = 0,
                    Category = TalentCategory.Combat,
                    BaseValue = 0f,
                    ValuePerLevel = 0.1f,
                    UpgradeCost = 200
                },
                new Talent
                {
                    Id = "durability_save",
                    Name = "织补技巧",
                    Description = "减少战斗中衣服的磨损速度。",
                    Icon = null,
                    MaxLevel = 5,
                    CurrentLevel = 0,
                    Category = TalentCategory.Survival,
                    BaseValue = 0f,
                    ValuePerLevel = 0.1f,
                    UpgradeCost = 150
                },
                new Talent
                {
                    Id = "fish_quality",
                    Name = "幸运钓手",
                    Description = "提高钓到稀有鱼的概率。",
                    Icon = null,
                    MaxLevel = 5,
                    CurrentLevel = 0,
                    Category = TalentCategory.Survival,
                    BaseValue = 0f,
                    ValuePerLevel = 0.05f,
                    UpgradeCost = 150
                },
                new Talent
                {
                    Id = "romance_bonus",
                    Name = "魅力四射",
                    Description = "与NPC互动时获得更多好感度。",
                    Icon = null,
                    MaxLevel = 5,
                    CurrentLevel = 0,
                    Category = TalentCategory.Social,
                    BaseValue = 0f,
                    ValuePerLevel = 0.15f,
                    UpgradeCost = 150
                },
                new Talent
                {
                    Id = "crew_boost",
                    Name = "船长威严",
                    Description = "提升配偶船员的DPS和修补效率。",
                    Icon = null,
                    MaxLevel = 5,
                    CurrentLevel = 0,
                    Category = TalentCategory.Social,
                    BaseValue = 0f,
                    ValuePerLevel = 0.1f,
                    UpgradeCost = 200
                }
            };
        }

        /// <summary>
        /// 升级天赋
        /// </summary>
        public bool UpgradeTalent(string talentId)
        {
            var talent = Talents.Find(t => t.Id == talentId);
            if (talent == null) return false;
            if (talent.IsMaxLevel) return false;

            int cost = talent.GetUpgradeCost();
            var playerData = GameManager.Instance.PlayerData;
            if (playerData.Gold < cost) return false;

            playerData.AddGold(-cost);
            talent.CurrentLevel++;
            OnTalentUpgraded?.Invoke(talentId, talent.CurrentLevel);
            
            Debug.Log($"[TalentSystem] 天赋「{talent.Name}」升级到 Lv.{talent.CurrentLevel}");
            return true;
        }

        /// <summary>
        /// 获取每秒金币收益
        /// </summary>
        public float GetGoldPerSecond()
        {
            var talent = Talents.Find(t => t.Id == "offline_gold");
            float bonus = talent?.GetCurrentValue() ?? 0f;
            return BaseGoldPerSecond + bonus;
        }

        /// <summary>
        /// 获取每秒经验收益
        /// </summary>
        public float GetExpPerSecond()
        {
            var talent = Talents.Find(t => t.Id == "offline_exp");
            float bonus = talent?.GetCurrentValue() ?? 0f;
            return BaseExpPerSecond + bonus;
        }

        /// <summary>
        /// 获取战斗伤害加成
        /// </summary>
        public float GetDamageMultiplier()
        {
            var talent = Talents.Find(t => t.Id == "combat_damage");
            return 1f + (talent?.GetCurrentValue() ?? 0f);
        }

        /// <summary>
        /// 获取船员加成倍率
        /// </summary>
        public float GetCrewMultiplier()
        {
            var talent = Talents.Find(t => t.Id == "crew_boost");
            return 1f + (talent?.GetCurrentValue() ?? 0f);
        }

        /// <summary>
        /// 获取好感度加成
        /// </summary>
        public float GetFavorMultiplier()
        {
            var talent = Talents.Find(t => t.Id == "romance_bonus");
            return 1f + (talent?.GetCurrentValue() ?? 0f);
        }

        /// <summary>
        /// 获取耐久减免
        /// </summary>
        public float GetDurabilityReduction()
        {
            var talent = Talents.Find(t => t.Id == "durability_save");
            return talent?.GetCurrentValue() ?? 0f;
        }
    }

    [Serializable]
    public class Talent
    {
        public string Id;
        public string Name;
        public string Description;
        public Sprite Icon;
        public int MaxLevel;
        public int CurrentLevel;
        public TalentCategory Category;
        public float BaseValue;
        public float ValuePerLevel;
        public int UpgradeCost;

        public bool IsMaxLevel => CurrentLevel >= MaxLevel;

        public float GetCurrentValue()
        {
            return BaseValue + ValuePerLevel * CurrentLevel;
        }

        public int GetUpgradeCost()
        {
            return Mathf.FloorToInt(UpgradeCost * Mathf.Pow(1.5f, CurrentLevel));
        }
    }

    public enum TalentCategory
    {
        Idle,       // 挂机
        Combat,     // 战斗
        Survival,   // 生存
        Social      // 社交
    }
}
