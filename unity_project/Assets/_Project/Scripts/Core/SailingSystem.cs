using UnityEngine;
using System;
using System.Collections;
using System.Collections.Generic;
using BurstFishingKingdom.Battle;

namespace BurstFishingKingdom.Core
{
    /// <summary>
    /// 出海/航行系统
    /// 管理海域选择、航行事件、进入战斗
    /// </summary>
    public class SailingSystem : MonoBehaviour
    {
        public static SailingSystem Instance { get; private set; }

        [Header("海域列表")]
        public List<SeaArea> SeaAreas = new();

        [Header("航行状态")]
        public bool IsSailing = false;
        public SeaArea CurrentArea;
        public float SailProgress = 0f;

        [Header("随机事件")]
        public List<SailEvent> SailEvents = new();
        public float EventTriggerChance = 0.3f;

        public event Action OnSailStarted;
        public event Action OnSailEnded;
        public event Action<string> OnEventTriggered;
        public event Action<BossData> OnBossEncountered;

        private Coroutine _sailCoroutine;

        private void Awake()
        {
            if (Instance != null && Instance != this) { Destroy(gameObject); return; }
            Instance = this;
            InitializeSeaAreas();
        }

        private void InitializeSeaAreas()
        {
            SeaAreas = new List<SeaArea>
            {
                new SeaArea
                {
                    AreaId = "coastal",
                    AreaName = "近海区域",
                    Description = "安全的近海，适合新手。",
                    Difficulty = 1,
                    MinShipLevel = 1,
                    BossIds = new List<string> { "coastal_crab" },
                    SailTime = 3f
                },
                new SeaArea
                {
                    AreaId = "stream",
                    AreaName = "溪流区",
                    Description = "淡水与海水交汇，鱼类丰富。",
                    Difficulty = 2,
                    MinShipLevel = 1,
                    BossIds = new List<string> { "stream_king" },
                    SailTime = 5f
                },
                new SeaArea
                {
                    AreaId = "mid_sea",
                    AreaName = "中海区",
                    Description = "较深的海域，需要更好的装备。",
                    Difficulty = 3,
                    MinShipLevel = 2,
                    BossIds = new List<string> { "mid_sea_serpent" },
                    SailTime = 8f
                },
                new SeaArea
                {
                    AreaId = "deep_sea",
                    AreaName = "深海区",
                    Description = "危险的海域，传说中的海兽出没。",
                    Difficulty = 5,
                    MinShipLevel = 3,
                    BossIds = new List<string> { "abyss_leviathan" },
                    SailTime = 12f
                }
            };
        }

        /// <summary>
        /// 开始出海
        /// </summary>
        public void StartSailing(string areaId)
        {
            var area = SeaAreas.Find(a => a.AreaId == areaId);
            if (area == null) return;

            var playerData = GameManager.Instance.PlayerData;
            if (playerData.CurrentShipLevel < area.MinShipLevel)
            {
                Debug.Log($"[Sailing] 船只等级不足，需要 {area.MinShipLevel} 级");
                return;
            }

            CurrentArea = area;
            IsSailing = true;
            SailProgress = 0f;

            // 重置船员修补状态
            var crewSystem = FindObjectOfType<NPC.CrewSystem>();
            crewSystem?.ResetRepairStatus();

            OnSailStarted?.Invoke();
            _sailCoroutine = StartCoroutine(SailingCoroutine(area));
        }

        private IEnumerator SailingCoroutine(SeaArea area)
        {
            float elapsed = 0f;

            while (elapsed < area.SailTime)
            {
                elapsed += Time.deltaTime;
                SailProgress = elapsed / area.SailTime;

                // 随机触发事件
                if (UnityEngine.Random.value < EventTriggerChance * Time.deltaTime)
                {
                    TriggerRandomEvent();
                }

                yield return null;
            }

            // 航行结束，遭遇BOSS
            SailProgress = 1f;
            EncounterBoss(area);
        }

        private void TriggerRandomEvent()
        {
            if (SailEvents.Count == 0) return;
            var evt = SailEvents[UnityEngine.Random.Range(0, SailEvents.Count)];
            OnEventTriggered?.Invoke(evt.Description);

            // 应用事件效果
            var playerData = GameManager.Instance.PlayerData;
            switch (evt.EventType)
            {
                case EventType.GoodWind:
                    Debug.Log("[Sailing] 顺风！航行速度加快");
                    break;
                case EventType.FishShoal:
                    Debug.Log("[Sailing] 发现鱼群！");
                    playerData.AddGold(UnityEngine.Random.Range(10, 30));
                    break;
                case EventType.Storm:
                    Debug.Log("[Sailing] 遭遇暴风雨！");
                    var equip = playerData.GetComponent<Equipment.EquipmentManager>();
                    equip?.TakeDamage(Equipment.EquipmentSlot.Top, UnityEngine.Random.Range(5, 15));
                    break;
            }
        }

        private void EncounterBoss(SeaArea area)
        {
            string bossId = area.BossIds[UnityEngine.Random.Range(0, area.BossIds.Count)];
            var bossData = Resources.Load<BossData>("Data/Bosses/" + bossId);

            if (bossData != null)
            {
                OnBossEncountered?.Invoke(bossData);
                Debug.Log($"[Sailing] 遭遇海兽: {bossData.BossName}");
            }
            else
            {
                // 如果没有找到BOSS数据，创建一个默认的
                var defaultBoss = ScriptableObject.CreateInstance<BossData>();
                defaultBoss.BossName = "神秘海兽";
                defaultBoss.MaxHp = 100 + area.Difficulty * 50;
                defaultBoss.Defense = 5 + area.Difficulty * 5;
                defaultBoss.Attack = 20 + area.Difficulty * 10;
                OnBossEncountered?.Invoke(defaultBoss);
            }
        }

        /// <summary>
        /// 中止航行/返航
        /// </summary>
        public void ReturnToPort()
        {
            if (_sailCoroutine != null)
                StopCoroutine(_sailCoroutine);

            IsSailing = false;
            SailProgress = 0f;
            OnSailEnded?.Invoke();
            GameManager.Instance.LoadScene(GameScene.ShipCabin);
        }
    }

    [Serializable]
    public class SeaArea
    {
        public string AreaId;
        public string AreaName;
        public string Description;
        public int Difficulty;
        public int MinShipLevel;
        public List<string> BossIds;
        public float SailTime;
    }

    [Serializable]
    public class SailEvent
    {
        public string EventName;
        public string Description;
        public EventType EventType;
    }

    public enum EventType
    {
        GoodWind,   // 顺风
        FishShoal,  // 鱼群
        Storm,      // 暴风雨
        Whirlpool,  // 漩涡
        Treasure,   // 宝藏
        GhostShip   // 幽灵船
    }
}
