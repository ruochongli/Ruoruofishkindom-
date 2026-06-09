using UnityEngine;

namespace BurstFishingKingdom.Core
{
    /// <summary>
    /// 游戏启动引导
    /// 确保 GameManager 单例存在，加载初始场景
    /// </summary>
    public class GameBootstrap : MonoBehaviour
    {
        [Header("GameManager Prefab")]
        public GameObject GameManagerPrefab;

        [Header("启动设置")]
        public bool SkipToGameplay = false;
        public GameScene StartScene = GameScene.ShipCabin;

        private void Awake()
        {
            // 确保 GameManager 存在
            if (GameManager.Instance == null)
            {
                if (GameManagerPrefab != null)
                {
                    Instantiate(GameManagerPrefab);
                }
                else
                {
                    // 创建默认 GameManager
                    var go = new GameObject("GameManager");
                    go.AddComponent<GameManager>();
                    go.AddComponent<SaveManager>();
                    go.AddComponent<TimeManager>();
                    go.AddComponent<OfflineRewardManager>();
                    go.AddComponent<DailyShopSystem>();
                    go.AddComponent<CitySystem>();
                    go.AddComponent<ShipCabinSystem>();
                    go.AddComponent<SailingSystem>();
                    go.AddComponent<NPC.RomanceSystem>();
                    go.AddComponent<NPC.CrewSystem>();
                    go.AddComponent<Player.TalentSystem>();
                }
            }

            // 确保 Player 存在
            var playerData = FindObjectOfType<Player.PlayerData>();
            if (playerData == null)
            {
                var playerGo = new GameObject("Player");
                playerData = playerGo.AddComponent<Player.PlayerData>();
                playerGo.AddComponent<Player.PlayerAppearance>();
                playerGo.AddComponent<Equipment.EquipmentManager>();
                playerGo.AddComponent<Inventory.InventoryGrid>();
            }

            // 关联到 GameManager
            if (GameManager.Instance.PlayerData == null)
            {
                GameManager.Instance.PlayerData = playerData;
            }
        }

        private void Start()
        {
            if (SkipToGameplay)
            {
                GameManager.Instance.LoadScene(StartScene);
            }
        }
    }
}
