using UnityEngine;
using UnityEngine.UI;
using TMPro;

namespace BurstFishingKingdom.UI
{
    /// <summary>
    /// 主菜单
    /// </summary>
    public class MainMenu : MonoBehaviour
    {
        [Header("按钮")]
        public Button StartGameButton;
        public Button ContinueButton;
        public Button SettingsButton;
        public Button QuitButton;

        [Header("面板")]
        public GameObject SettingsPanel;
        public GameObject CharacterCreationPanel;

        [Header("版本信息")]
        public TextMeshProUGUI VersionText;

        private void Start()
        {
            if (StartGameButton != null)
                StartGameButton.onClick.AddListener(OnStartGame);

            if (ContinueButton != null)
            {
                ContinueButton.onClick.AddListener(OnContinueGame);
                // 检查是否有存档
                ContinueButton.interactable = System.IO.File.Exists(
                    System.IO.Path.Combine(Application.persistentDataPath, "save.json"));
            }

            if (SettingsButton != null)
                SettingsButton.onClick.AddListener(() => SettingsPanel?.SetActive(true));

            if (QuitButton != null)
                QuitButton.onClick.AddListener(OnQuit);

            if (VersionText != null)
                VersionText.text = $"v{Application.version}";
        }

        private void OnStartGame()
        {
            // 显示创角界面
            if (CharacterCreationPanel != null)
            {
                CharacterCreationPanel.SetActive(true);
            }
            else
            {
                // 直接开始（使用默认角色）
                StartNewGame();
            }
        }

        public void StartNewGame()
        {
            // 删除旧存档
            string savePath = System.IO.Path.Combine(Application.persistentDataPath, "save.json");
            if (System.IO.File.Exists(savePath))
                System.IO.File.Delete(savePath);

            Core.GameManager.Instance.LoadScene(Core.GameScene.ShipCabin);
        }

        private void OnContinueGame()
        {
            Core.GameManager.Instance.LoadScene(Core.GameScene.ShipCabin);
        }

        private void OnQuit()
        {
#if UNITY_EDITOR
            UnityEditor.EditorApplication.isPlaying = false;
#else
            Application.Quit();
#endif
        }
    }
}
