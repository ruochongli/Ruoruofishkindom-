using UnityEngine;

namespace BurstFishingKingdom.Core
{
    /// <summary>
    /// 游戏核心管理器 - 单例模式
    /// 负责游戏状态管理、场景切换、全局数据访问
    /// </summary>
    public class GameManager : MonoBehaviour
    {
        public static GameManager Instance { get; private set; }

        [Header("游戏状态")]
        public GameState CurrentState = GameState.MainMenu;
        
        [Header("系统引用")]
        public Player.PlayerData PlayerData;
        public SaveManager SaveManager;
        public TimeManager TimeManager;
        public OfflineRewardManager OfflineReward;

        [Header("游戏配置")]
        public int MaxOfflineHours = 8;
        public float GameTimeScale = 1f;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
            DontDestroyOnLoad(gameObject);
            
            InitializeSystems();
        }

        private void InitializeSystems()
        {
            // 初始化所有子系统
            SaveManager = GetComponent<SaveManager>();
            TimeManager = GetComponent<TimeManager>();
            OfflineReward = GetComponent<OfflineRewardManager>();
            
            // 尝试加载存档
            SaveManager?.TryLoadGame();
        }

        /// <summary>
        /// 切换游戏场景
        /// </summary>
        public void LoadScene(GameScene scene)
        {
            string sceneName = scene switch
            {
                GameScene.ShipCabin => "01_ShipCabin",
                GameScene.City => "02_City",
                GameScene.Sea => "03_Sea",
                _ => "00_Bootstrap"
            };
            UnityEngine.SceneManagement.SceneManager.LoadScene(sceneName);
        }

        /// <summary>
        /// 退出游戏时保存
        /// </summary>
        private void OnApplicationQuit()
        {
            SaveManager?.SaveGame();
        }

        /// <summary>
        /// 应用进入后台时保存
        /// </summary>
        private void OnApplicationPause(bool pause)
        {
            if (pause) SaveManager?.SaveGame();
        }
    }

    public enum GameState
    {
        MainMenu,
        InShip,
        InCity,
        Sailing,
        Fishing,
        Battling,
        InUI
    }

    public enum GameScene
    {
        Bootstrap,
        ShipCabin,
        City,
        Sea
    }
}
