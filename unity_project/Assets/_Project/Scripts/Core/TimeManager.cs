using UnityEngine;
using System;

namespace BurstFishingKingdom.Core
{
    /// <summary>
    /// 游戏时间管理器
    /// 管理游戏内时间、日期、NPC日程
    /// </summary>
    public class TimeManager : MonoBehaviour
    {
        public static TimeManager Instance { get; private set; }

        [Header("当前时间")]
        public int CurrentHour = 8;      // 0-23
        public int CurrentDay = 1;       // 总天数
        public Season CurrentSeason = Season.Spring;
        public Weather CurrentWeather = Weather.Sunny;

        [Header("时间配置")]
        public float RealSecondsPerGameHour = 60f;  // 现实中60秒=游戏中1小时
        public bool TimePaused = false;

        private float _timeAccumulator;
        public event Action<int> OnHourChanged;
        public event Action<int> OnDayChanged;

        private void Awake()
        {
            if (Instance != null && Instance != this) { Destroy(gameObject); return; }
            Instance = this;
        }

        private void Update()
        {
            if (TimePaused) return;
            
            _timeAccumulator += Time.deltaTime * GameManager.Instance.GameTimeScale;
            
            if (_timeAccumulator >= RealSecondsPerGameHour)
            {
                _timeAccumulator -= RealSecondsPerGameHour;
                AdvanceHour();
            }
        }

        /// <summary>
        /// 推进1小时
        /// </summary>
        public void AdvanceHour(int hours = 1)
        {
            for (int i = 0; i < hours; i++)
            {
                CurrentHour++;
                if (CurrentHour >= 24)
                {
                    CurrentHour = 0;
                    AdvanceDay();
                }
                OnHourChanged?.Invoke(CurrentHour);
            }
        }

        private void AdvanceDay()
        {
            CurrentDay++;
            // 更新季节
            CurrentSeason = (Season)((CurrentDay / 30) % 4);
            // 随机天气
            CurrentWeather = UnityEngine.Random.value > 0.7f ? Weather.Rainy : Weather.Sunny;
            
            // 触发每日事件
            OnDayChanged?.Invoke(CurrentDay);
            
            Debug.Log($"[TimeManager] 第{CurrentDay}天 - {CurrentSeason} - {CurrentWeather}");
        }

        /// <summary>
        /// 获取NPC当前位置
        /// </summary>
        public string GetNPCLocation(NPC.NPCSchedule schedule)
        {
            foreach (var slot in schedule.DailySlots)
            {
                int start = slot.StartHour;
                int end = slot.EndHour;
                bool isCurrent = end < start 
                    ? (CurrentHour >= start || CurrentHour < end)
                    : (CurrentHour >= start && CurrentHour < end);
                if (isCurrent) return slot.LocationId;
            }
            return schedule.DailySlots[0].LocationId;
        }
    }

    public enum Season { Spring, Summer, Autumn, Winter }
    public enum Weather { Sunny, Rainy, Stormy, Snowy }
}
