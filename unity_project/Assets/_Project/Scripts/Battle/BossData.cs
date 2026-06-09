using UnityEngine;
using System;
using System.Collections.Generic;

namespace BurstFishingKingdom.Battle
{
    /// <summary>
    /// BOSS数据 ScriptableObject
    /// </summary>
    [CreateAssetMenu(fileName = "NewBoss", menuName = "若若的钓鱼王国/BOSS")]
    public class BossData : ScriptableObject
    {
        public string BossId;
        public string BossName;
        [TextArea(2, 4)] public string Description;
        public Sprite BossSprite;
        public Sprite BossIcon;
        
        [Header("属性")]
        public int MaxHp = 200;
        [HideInInspector] public int CurrentHp;
        public int Defense = 10;
        public int Attack = 35;
        
        [Header("奖励")]
        public int MinGold = 50;
        public int MaxGold = 120;
        public int MinExp = 20;
        public int MaxExp = 50;
        
        [Header("掉落")]
        public List<BossDrop> Drops = new();
    }

    [Serializable]
    public class BossDrop
    {
        public string ItemId;
        public string ItemName;
        public float DropChance = 0.3f;
        public int MinCount = 1;
        public int MaxCount = 1;
    }
}
