using UnityEngine;
using System;
using System.Collections.Generic;

namespace BurstFishingKingdom.NPC
{
    /// <summary>
    /// NPC数据 ScriptableObject
    /// </summary>
    [CreateAssetMenu(fileName = "NewNPC", menuName = "爆衣钓鱼王国/NPC")]
    public class NPCData : ScriptableObject
    {
        public string NPCId;
        public string Name;
        public Gender Gender;
        public Sprite Portrait;
        public Sprite FullbodySprite;
        public Sexuality Sexuality;
        public string HomeCityId;
        
        [Header("好感度")]
        public int Favor = 0;
        public int MaxFavor = 200;
        public RelationshipStage Stage = RelationshipStage.Stranger;
        
        [Header("日程")]
        public List<ScheduleSlot> DailySchedule = new();
        
        [Header("对话")]
        public NPCLines Lines;
        
        [Header("礼物偏好")]
        public List<string> LikedCategories = new();
        public List<string> DislikedCategories = new();
        public string FavoriteItemId;
        
        [Header("战斗数据（婚后船员）")]
        public NPCCombatData CombatData;

        public string GetStageName()
        {
            return Stage switch
            {
                RelationshipStage.Stranger => "陌生",
                RelationshipStage.Acquaintance => "认识",
                RelationshipStage.Friendly => "友好",
                RelationshipStage.Intimate => "暧昧",
                RelationshipStage.Lover => "恋人",
                RelationshipStage.Engaged => "订婚",
                RelationshipStage.Married => "已婚",
                _ => "未知"
            };
        }

        public bool CanRomance(Gender playerGender)
        {
            return Sexuality switch
            {
                Sexuality.Hetero => (Gender == Gender.Female && playerGender == Gender.Male) || (Gender == Gender.Male && playerGender == Gender.Female),
                Sexuality.Homo => (Gender == Gender.Female && playerGender == Gender.Female) || (Gender == Gender.Male && playerGender == Gender.Male),
                Sexuality.Bi or Sexuality.Pan or Sexuality.PlayerOnly => true,
                _ => false
            };
        }
    }

    public enum Gender { Female, Male }
    public enum Sexuality { Hetero, Homo, Bi, Pan, PlayerOnly }
    public enum RelationshipStage { Stranger, Acquaintance, Friendly, Intimate, Lover, Engaged, Married }

    [Serializable]
    public class ScheduleSlot
    {
        public int StartHour;
        public int EndHour;
        public string LocationId;
        public string LocationName;
        public string Activity;
        public bool IsRomanceBonus;
    }

    [Serializable]
    public class NPCLines
    {
        public string[] Stranger;
        public string[] Acquaintance;
        public string[] Friendly;
        public string[] Intimate;
        public string[] Lover;
        public string[] Engaged;
        public string[] Married;
    }

    [Serializable]
    public class NPCCombatData
    {
        public int BaseDPS = 10;
        public float CritChance = 0.05f;
        public float CritMultiplier = 2f;
        public float BaseRepairPercent = 0.2f;
        public string[] BattleStartLines;
        public string[] PlayerShameLines;
        public string[] PlayerSkillLines;
        public string[] VictoryLines;
        public string[] RepairLines;
    }
}
