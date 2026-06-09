using UnityEngine;
using System;
using TMPro;

namespace BurstFishingKingdom.Core
{
    /// <summary>
    /// 离线收益管理器
    /// 计算玩家离线期间的挂机收益
    /// </summary>
    public class OfflineRewardManager : MonoBehaviour
    {
        [Header("UI引用")]
        public GameObject RewardPanel;
        public TextMeshProUGUI OfflineTimeText;
        public TextMeshProUGUI GoldRewardText;
        public TextMeshProUGUI ExpRewardText;

        [Header("上限设置")]
        public float MaxOfflineHours = 8f;

        /// <summary>
        /// 计算并显示离线收益
        /// </summary>
        public void CalculateAndShow(string lastSaveTimeStr)
        {
            if (!DateTime.TryParse(lastSaveTimeStr, out DateTime lastSaveTime))
            {
                Debug.Log("[OfflineReward] 无法解析上次保存时间");
                return;
            }

            double offlineSeconds = (DateTime.Now - lastSaveTime).TotalSeconds;
            double offlineHours = offlineSeconds / 3600.0;
            
            // 应用上限
            double cappedHours = Math.Min(offlineHours, MaxOfflineHours);
            double actualSeconds = cappedHours * 3600.0;

            // 获取天赋加成
            var talentSystem = FindObjectOfType<Player.TalentSystem>();
            float goldPerSec = talentSystem?.GetGoldPerSecond() ?? 0.1f;
            float expPerSec = talentSystem?.GetExpPerSecond() ?? 0.05f;

            int goldReward = Mathf.FloorToInt((float)(actualSeconds * goldPerSec));
            int expReward = Mathf.FloorToInt((float)(actualSeconds * expPerSec));

            if (goldReward > 0 || expReward > 0)
            {
                ShowRewardPanel(offlineHours, cappedHours, goldReward, expReward);
                
                // 发放奖励
                var playerData = GameManager.Instance.PlayerData;
                playerData?.AddGold(goldReward);
                playerData?.AddExp(expReward);
                
                Debug.Log($"[OfflineReward] 离线{offlineHours:F1}小时(上限{cappedHours:F1}h)，获得金币x{goldReward} 经验x{expReward}");
            }
        }

        private void ShowRewardPanel(double actualHours, double cappedHours, int gold, int exp)
        {
            if (RewardPanel == null) return;
            
            RewardPanel.SetActive(true);
            
            if (OfflineTimeText != null)
                OfflineTimeText.text = $"离线时长: {actualHours:F1}小时\n(实际计算: {cappedHours:F1}小时)";
            
            if (GoldRewardText != null)
                GoldRewardText.text = $"💰 +{gold}";
            
            if (ExpRewardText != null)
                ExpRewardText.text = $"⭐ +{exp}";
        }

        public void CloseRewardPanel()
        {
            if (RewardPanel != null) RewardPanel.SetActive(false);
        }
    }
}
