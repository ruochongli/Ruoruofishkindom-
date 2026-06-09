using UnityEngine;
using System;
using System.Collections.Generic;

namespace BurstFishingKingdom.NPC
{
    /// <summary>
    /// 恋爱养成系统
    /// 管理好感度、关系阶段、告白、求婚、结婚
    /// </summary>
    public class RomanceSystem : MonoBehaviour
    {
        public static RomanceSystem Instance { get; private set; }

        [Header("阶段阈值")]
        public int[] StageThresholds = { 0, 10, 30, 60, 90, 120, 150 };

        [Header("NPC关系数据")]
        public Dictionary<string, NPCRelation> Relations = new();

        public event Action<NPCData, RelationshipStage> OnStageChanged;
        public event Action<NPCData, int> OnFavorChanged;

        private void Awake()
        {
            if (Instance != null && Instance != this) { Destroy(gameObject); return; }
            Instance = this;
        }

        /// <summary>
        /// 增加好感度
        /// </summary>
        public void AddFavor(NPCData npc, int amount)
        {
            if (!Relations.ContainsKey(npc.NPCId))
            {
                Relations[npc.NPCId] = new NPCRelation { NPCId = npc.NPCId, Favor = 0, Stage = RelationshipStage.Stranger };
            }

            var relation = Relations[npc.NPCId];
            int oldFavor = relation.Favor;
            relation.Favor = Mathf.Min(relation.Favor + amount, npc.MaxFavor);
            
            npc.Favor = relation.Favor;
            
            OnFavorChanged?.Invoke(npc, relation.Favor);

            // 检查阶段提升
            CheckStageUp(npc, relation);
        }

        /// <summary>
        /// 检查是否可以进入下一阶段
        /// </summary>
        private void CheckStageUp(NPCData npc, NPCRelation relation)
        {
            int currentStageIndex = (int)relation.Stage;
            for (int i = currentStageIndex + 1; i < StageThresholds.Length; i++)
            {
                if (relation.Favor >= StageThresholds[i])
                {
                    var oldStage = relation.Stage;
                    relation.Stage = (RelationshipStage)i;
                    npc.Stage = relation.Stage;
                    
                    OnStageChanged?.Invoke(npc, relation.Stage);
                    
                    // 特殊事件
                    if (relation.Stage == RelationshipStage.Lover)
                        Debug.Log($"🎉 {npc.Name}接受了你的告白！你们成为了恋人！");
                    else if (relation.Stage == RelationshipStage.Engaged)
                        Debug.Log($"💍 {npc.Name}答应了你的求婚！你们订婚了！");
                    else if (relation.Stage == RelationshipStage.Married)
                    {
                        Debug.Log($"💒 恭喜！你和{npc.Name}结婚了！");
                        var crewSystem = FindObjectOfType<CrewSystem>();
                        if (crewSystem != null)
                        {
                            crewSystem.SpouseId = npc.NPCId;
                            crewSystem.SetCrew(npc);
                        }
                        var playerData = GameManager.Instance.PlayerData;
                        playerData.SpouseNPCId = npc.NPCId;
                    }
                }
            }
        }

        /// <summary>
        /// 告白（从暧昧→恋人）
        /// </summary>
        public bool ProposeLove(NPCData npc)
        {
            var relation = GetRelation(npc);
            if (relation.Stage != RelationshipStage.Intimate) return false;
            
            AddFavor(npc, 20); // 足够提升到恋人
            return true;
        }

        /// <summary>
        /// 求婚（从恋人→订婚）
        /// </summary>
        public bool ProposeMarriage(NPCData npc)
        {
            var relation = GetRelation(npc);
            if (relation.Stage != RelationshipStage.Lover) return false;
            
            AddFavor(npc, 30); // 足够提升到订婚
            return true;
        }

        /// <summary>
        /// 结婚（从订婚→已婚）
        /// </summary>
        public bool Marry(NPCData npc)
        {
            var relation = GetRelation(npc);
            if (relation.Stage != RelationshipStage.Engaged) return false;
            
            AddFavor(npc, 30); // 足够提升到已婚
            return true;
        }

        /// <summary>
        /// 获取关系数据
        /// </summary>
        public NPCRelation GetRelation(NPCData npc)
        {
            if (!Relations.ContainsKey(npc.NPCId))
            {
                Relations[npc.NPCId] = new NPCRelation { NPCId = npc.NPCId, Favor = npc.Favor, Stage = npc.Stage };
            }
            return Relations[npc.NPCId];
        }
    }

    [Serializable]
    public class NPCRelation
    {
        public string NPCId;
        public int Favor;
        public RelationshipStage Stage;
        public string CurrentOutfit;
    }
}
