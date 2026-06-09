using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System;

namespace BurstFishingKingdom.UI
{
    /// <summary>
    /// 人物面板UI
    /// 左侧：全身角色预览（换装实时渲染）
    /// 右侧：6格装备栏
    /// </summary>
    public class CharacterPanelUI : MonoBehaviour
    {
        [Header("角色预览")]
        public RectTransform CharacterPreviewArea;
        public Player.PlayerAppearance Appearance;
        public Camera PreviewCamera;
        public RawImage PreviewImage;
        public RenderTexture PreviewRenderTexture;

        [Header("装备栏")]
        public EquipmentSlotUI[] EquipmentSlots;

        [Header("属性显示")]
        public TextMeshProUGUI AttackText;
        public TextMeshProUGUI DefenseText;
        public TextMeshProUGUI CharmText;

        [Header("船员配置")]
        public GameObject CrewPanel;
        public TextMeshProUGUI CrewNameText;
        public TextMeshProUGUI CrewDPSText;
        public TextMeshProUGUI CrewRepairText;
        public Button ToggleCrewButton;

        private Equipment.EquipmentManager _equipmentManager;
        private NPC.CrewSystem _crewSystem;

        private void Awake()
        {
            _equipmentManager = FindObjectOfType<Player.PlayerData>()?.GetComponent<Equipment.EquipmentManager>();
            _crewSystem = FindObjectOfType<NPC.CrewSystem>();
        }

        private void OnEnable()
        {
            if (_equipmentManager != null)
            {
                _equipmentManager.OnEquipped += OnItemEquipped;
                _equipmentManager.OnUnequipped += OnItemUnequipped;
            }
            UpdateAllUI();
        }

        private void OnDisable()
        {
            if (_equipmentManager != null)
            {
                _equipmentManager.OnEquipped -= OnItemEquipped;
                _equipmentManager.OnUnequipped -= OnItemUnequipped;
            }
        }

        /// <summary>
        /// 更新全部UI
        /// </summary>
        public void UpdateAllUI()
        {
            UpdateEquipmentSlots();
            UpdateStats();
            UpdateCrewPanel();
        }

        private void UpdateEquipmentSlots()
        {
            if (_equipmentManager == null) return;

            foreach (var slotUI in EquipmentSlots)
            {
                var item = _equipmentManager.GetEquipped(slotUI.Slot);
                slotUI.SetItem(item);
            }
        }

        private void UpdateStats()
        {
            if (_equipmentManager == null) return;
            
            if (AttackText != null) AttackText.text = $"⚔️ {_equipmentManager.GetTotalAttack()}";
            if (DefenseText != null) DefenseText.text = $"🛡️ {_equipmentManager.GetTotalDefense()}";
            
            int charm = 0;
            foreach (Equipment.EquipmentSlot slot in Enum.GetValues(typeof(Equipment.EquipmentSlot)))
            {
                charm += _equipmentManager.GetEquipped(slot)?.Charm ?? 0;
            }
            if (CharmText != null) CharmText.text = $"💕 {charm}";
        }

        private void UpdateCrewPanel()
        {
            if (_crewSystem == null || CrewPanel == null) return;

            bool hasSpouse = !string.IsNullOrEmpty(_crewSystem.SpouseId);
            CrewPanel.SetActive(hasSpouse);

            if (!hasSpouse) return;

            var crew = _crewSystem.GetActiveCrew();
            if (crew == null) return;

            if (CrewNameText != null) CrewNameText.text = crew.Name;
            if (CrewDPSText != null) CrewDPSText.text = $"DPS: {_crewSystem.GetCurrentDPS()}/回合";
            if (CrewRepairText != null) CrewRepairText.text = $"修补: {Mathf.RoundToInt(_crewSystem.GetCurrentRepairPercent() * 100)}%";
            
            if (ToggleCrewButton != null)
            {
                bool isActive = _crewSystem.HasActiveCrew();
                ToggleCrewButton.GetComponentInChildren<TextMeshProUGUI>().text = isActive ? "❌ 留守" : "✅ 同行";
            }
        }

        private void OnItemEquipped(Equipment.EquipmentSlot slot, Equipment.ClothingItemSO item)
        {
            UpdateEquipmentSlots();
            UpdateStats();
        }

        private void OnItemUnequipped(Equipment.EquipmentSlot slot, Equipment.ClothingItemSO item)
        {
            UpdateEquipmentSlots();
            UpdateStats();
        }

        /// <summary>
        /// 点击装备槽
        /// </summary>
        public void OnSlotClicked(int slotIndex)
        {
            // 打开装备选择弹窗或从背包装备
            Debug.Log($"[CharacterPanelUI] 点击装备槽: {(Equipment.EquipmentSlot)slotIndex}");
        }

        /// <summary>
        /// 切换船员同行/留守
        /// </summary>
        public void ToggleCrew()
        {
            if (_crewSystem == null) return;
            
            if (_crewSystem.HasActiveCrew())
                _crewSystem.RemoveCrew();
            else
            {
                // 重新设置船员为配偶
                var spouse = FindObjectOfType<NPC.RomanceSystem>()?.GetRelationById(_crewSystem.SpouseId);
                // TODO: 从NPCData加载
            }
            
            UpdateCrewPanel();
        }
    }

    /// <summary>
    /// 单个装备槽UI
    /// </summary>
    [System.Serializable]
    public class EquipmentSlotUI
    {
        public Equipment.EquipmentSlot Slot;
        public Image IconImage;
        public Image QualityBorder;
        public TextMeshProUGUI DurabilityText;
        public Button SlotButton;

        public void SetItem(Equipment.ClothingItemSO item)
        {
            if (item == null)
            {
                IconImage.sprite = null;
                IconImage.color = new Color(1, 1, 1, 0.2f);
                QualityBorder.color = Color.clear;
                DurabilityText.text = "";
                return;
            }

            IconImage.sprite = item.NormalSprite;
            IconImage.color = Color.white;
            QualityBorder.color = item.GetQualityColor();
            
            // 耐久度显示
            var equipManager = GameManager.Instance.PlayerData.GetComponent<Equipment.EquipmentManager>();
            if (equipManager != null && equipManager.CurrentDurability.ContainsKey(Slot))
            {
                int current = equipManager.CurrentDurability[Slot];
                DurabilityText.text = $"{current}/{item.MaxDurability}";
                DurabilityText.color = current < item.MaxDurability * 0.25f ? Color.red : Color.white;
            }
        }
    }
}
