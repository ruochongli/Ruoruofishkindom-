using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System;
using BurstFishingKingdom.Player;

namespace BurstFishingKingdom.UI
{
    /// <summary>
    /// 创角界面
    /// 性别选择、命名、捏脸
    /// </summary>
    public class CharacterCreationUI : MonoBehaviour
    {
        [Header("基础信息")]
        public TMP_InputField NameInput;
        public Toggle MaleToggle;
        public Toggle FemaleToggle;

        [Header("捏脸参数")]
        public Slider SkinToneSlider;
        public Slider HairStyleSlider;
        public Slider HairColorSlider;
        public Slider EyeColorSlider;

        [Header("预览")]
        public Player.PlayerAppearance PreviewAppearance;
        public TextMeshProUGUI PreviewNameText;

        [Header("按钮")]
        public Button ConfirmButton;
        public Button RandomButton;
        public Button BackButton;

        [Header("提示")]
        public TextMeshProUGUI HintText;

        private void Start()
        {
            if (MaleToggle != null)
                MaleToggle.onValueChanged.AddListener(OnGenderChanged);
            if (FemaleToggle != null)
                FemaleToggle.onValueChanged.AddListener(OnGenderChanged);

            if (NameInput != null)
                NameInput.onValueChanged.AddListener(OnNameChanged);

            if (SkinToneSlider != null)
                SkinToneSlider.onValueChanged.AddListener(v => UpdateAppearance(a => a.SkinToneIndex = Mathf.FloorToInt(v)));
            if (HairStyleSlider != null)
                HairStyleSlider.onValueChanged.AddListener(v => UpdateAppearance(a => a.HairStyleIndex = Mathf.FloorToInt(v)));
            if (HairColorSlider != null)
                HairColorSlider.onValueChanged.AddListener(v => UpdateAppearance(a => a.HairColorIndex = Mathf.FloorToInt(v)));
            if (EyeColorSlider != null)
                EyeColorSlider.onValueChanged.AddListener(v => UpdateAppearance(a => a.EyeColorIndex = Mathf.FloorToInt(v)));

            if (ConfirmButton != null)
                ConfirmButton.onClick.AddListener(OnConfirm);
            if (RandomButton != null)
                RandomButton.onClick.AddListener(OnRandomize);
            if (BackButton != null)
                BackButton.onClick.AddListener(() => gameObject.SetActive(false));

            // 初始化
            OnRandomize();
        }

        private void OnGenderChanged(bool isOn)
        {
            if (!isOn) return;
            var gender = MaleToggle != null && MaleToggle.isOn ? Player.Gender.Male : Player.Gender.Female;
            UpdateAppearance(a => { });
        }

        private void OnNameChanged(string name)
        {
            if (PreviewNameText != null)
                PreviewNameText.text = string.IsNullOrEmpty(name) ? "冒险者" : name;
        }

        private void UpdateAppearance(Action<Player.PlayerAppearance> updater)
        {
            if (PreviewAppearance != null)
            {
                updater(PreviewAppearance);
                PreviewAppearance.UpdateColors();
            }
        }

        private void OnRandomize()
        {
            if (SkinToneSlider != null) SkinToneSlider.value = UnityEngine.Random.Range(0, 6);
            if (HairStyleSlider != null) HairStyleSlider.value = UnityEngine.Random.Range(0, 10);
            if (HairColorSlider != null) HairColorSlider.value = UnityEngine.Random.Range(0, 10);
            if (EyeColorSlider != null) EyeColorSlider.value = UnityEngine.Random.Range(0, 8);

            if (FemaleToggle != null) FemaleToggle.isOn = true;

            string[] randomNames = { "艾莉", "露娜", "希尔薇", "芙洛拉", "塞西莉亚", "安娜", "玛丽", "露易丝" };
            if (NameInput != null) NameInput.text = randomNames[UnityEngine.Random.Range(0, randomNames.Length)];
        }

        private void OnConfirm()
        {
            string playerName = NameInput != null ? NameInput.text : "冒险者";
            if (string.IsNullOrWhiteSpace(playerName) || playerName.Length < 2)
            {
                if (HintText != null) HintText.text = "名字需要至少2个字符";
                return;
            }

            var gender = MaleToggle != null && MaleToggle.isOn ? Player.Gender.Male : Player.Gender.Female;

            // 应用到玩家数据
            var playerData = Core.GameManager.Instance.PlayerData;
            playerData.PlayerName = playerName;
            playerData.PlayerGender = gender;

            if (playerData.Appearance != null && PreviewAppearance != null)
            {
                playerData.Appearance.SkinToneIndex = PreviewAppearance.SkinToneIndex;
                playerData.Appearance.HairStyleIndex = PreviewAppearance.HairStyleIndex;
                playerData.Appearance.HairColorIndex = PreviewAppearance.HairColorIndex;
                playerData.Appearance.EyeColorIndex = PreviewAppearance.EyeColorIndex;
                playerData.Appearance.UpdateColors();
            }

            // 给予初始装备
            var equip = playerData.GetComponent<Equipment.EquipmentManager>();
            // TODO: 装备默认衣服

            Core.GameManager.Instance.SaveManager?.SaveGame();
            Core.GameManager.Instance.LoadScene(Core.GameScene.ShipCabin);
        }
    }
}
