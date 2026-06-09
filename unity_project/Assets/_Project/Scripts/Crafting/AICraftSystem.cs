using UnityEngine;
using System.Collections.Generic;
using System.Linq;

namespace BurstFishingKingdom.Crafting
{
    /// <summary>
    /// AI制衣系统
    /// 通过关键词解析将自然语言描述转换为配方
    /// </summary>
    public class AICraftSystem : MonoBehaviour
    {
        [Header("关键词映射")]
        public List<StyleKeyword> StyleKeywords = new();
        public List<ColorKeyword> ColorKeywords = new();
        public List<TierKeyword> TierKeywords = new();
        public List<AccessoryKeyword> AccessoryKeywords = new();
        public List<CharacterPreset> CharacterPresets = new();

        /// <summary>
        /// 解析玩家输入的文本，生成配方
        /// </summary>
        public ClothingRecipe GenerateRecipe(string input)
        {
            var recipe = new ClothingRecipe { InputText = input };
            
            // 解析款式
            foreach (var kw in StyleKeywords)
            {
                if (input.Contains(kw.Keyword))
                {
                    recipe.StyleName = kw.StyleName;
                    recipe.FabricNeed = kw.FabricAmount;
                    break;
                }
            }
            if (string.IsNullOrEmpty(recipe.StyleName))
            {
                recipe.StyleName = "定制衣服";
                recipe.FabricNeed = 3;
            }

            // 解析颜色
            foreach (var kw in ColorKeywords)
            {
                if (input.Contains(kw.Keyword) && !recipe.Colors.Contains(kw.DyeId))
                {
                    recipe.Colors.Add(kw.DyeId);
                }
            }
            if (recipe.Colors.Count == 0) recipe.Colors.Add("white");

            // 解析品质
            foreach (var kw in TierKeywords)
            {
                if (input.Contains(kw.Keyword))
                {
                    recipe.TargetQuality = Mathf.Max(recipe.TargetQuality, kw.Quality);
                    if (kw.Accessories != null)
                    {
                        recipe.Accessories.AddRange(kw.Accessories);
                    }
                }
            }

            // 解析配饰
            foreach (var kw in AccessoryKeywords)
            {
                if (input.Contains(kw.Keyword) && !recipe.Accessories.Any(a => a.ItemId == kw.ItemId))
                {
                    recipe.Accessories.Add(new AccessoryRequirement 
                    { 
                        ItemId = kw.ItemId, 
                        Amount = kw.Amount,
                        Quality = kw.Quality 
                    });
                }
            }

            // 角色预设
            foreach (var preset in CharacterPresets)
            {
                if (input.Contains(preset.CharacterName))
                {
                    recipe.TargetQuality = Mathf.Max(recipe.TargetQuality, preset.Quality);
                    recipe.StyleName = preset.StyleName;
                    foreach (var c in preset.Colors)
                    {
                        if (!recipe.Colors.Contains(c)) recipe.Colors.Add(c);
                    }
                    foreach (var acc in preset.Accessories)
                    {
                        if (!recipe.Accessories.Any(a => a.ItemId == acc))
                        {
                            recipe.Accessories.Add(new AccessoryRequirement { ItemId = acc, Amount = 1, Quality = 2 });
                        }
                    }
                }
            }

            // 生成材料列表
            recipe.Materials = GenerateMaterials(recipe);
            
            // 生成名字
            recipe.OutputName = GenerateClothName(recipe);

            return recipe;
        }

        private List<CraftMaterial> GenerateMaterials(ClothingRecipe recipe)
        {
            var materials = new List<CraftMaterial>();
            
            // 基础布料
            materials.Add(new CraftMaterial
            {
                ItemId = "fabric",
                Name = "丝绸布料",
                Amount = Mathf.CeilToInt(recipe.FabricNeed),
                Quality = recipe.TargetQuality
            });

            // 丝线
            materials.Add(new CraftMaterial
            {
                ItemId = "thread",
                Name = "丝线",
                Amount = Mathf.CeilToInt(recipe.FabricNeed * 0.7f),
                Quality = Mathf.Max(recipe.TargetQuality - 1, 0)
            });

            // 染料
            foreach (var dyeColor in recipe.Colors)
            {
                var dyeInfo = GetDyeInfo(dyeColor);
                materials.Add(new CraftMaterial
                {
                    ItemId = "dye_" + dyeColor,
                    Name = dyeInfo.Name,
                    Amount = 2,
                    Quality = dyeColor == "purple" || dyeColor == "gold" ? 3 : 1
                });
            }

            // 配饰
            foreach (var acc in recipe.Accessories)
            {
                materials.Add(new CraftMaterial
                {
                    ItemId = acc.ItemId,
                    Name = GetMaterialName(acc.ItemId),
                    Amount = acc.Amount,
                    Quality = acc.Quality
                });
            }

            // 高品质需要BOSS材料
            if (recipe.TargetQuality >= 3)
            {
                materials.Add(new CraftMaterial
                {
                    ItemId = "boss_scale",
                    Name = "海兽鳞片",
                    Amount = 1,
                    Quality = 3
                });
            }

            return materials;
        }

        private string GenerateClothName(ClothingRecipe recipe)
        {
            string prefix = recipe.TargetQuality switch
            {
                5 => "神话·",
                4 => "传说·",
                3 => "史诗·",
                2 => "精致·",
                1 => "",
                _ => ""
            };

            string colorStr = recipe.Colors.Count > 0 ? GetColorName(recipe.Colors[0]) : "";
            return $"{prefix}{colorStr}{recipe.StyleName}";
        }

        private string GetColorName(string dyeId)
        {
            return dyeId switch
            {
                "red" => "红色", "blue" => "蓝色", "black" => "黑色",
                "white" => "白色", "purple" => "紫色", "gold" => "金色",
                "green" => "绿色", "pink" => "粉色",
                _ => ""
            };
        }

        private DyeInfo GetDyeInfo(string dyeId)
        {
            return dyeId switch
            {
                "red" => new DyeInfo { Name = "红色花卉染剂", Source = "种植红玫瑰提炼" },
                "blue" => new DyeInfo { Name = "蓝色海藻染剂", Source = "中海区采集蓝海藻" },
                "black" => new DyeInfo { Name = "黑色墨鱼汁", Source = "近海区钓乌贼" },
                "white" => new DyeInfo { Name = "白色贝壳粉", Source = "沙滩采集贝壳" },
                "purple" => new DyeInfo { Name = "紫色曼陀罗染剂", Source = "种植紫色曼陀罗" },
                "gold" => new DyeInfo { Name = "金色龙血染剂", Source = "传说鱼掉落" },
                "green" => new DyeInfo { Name = "绿色苔藓染剂", Source = "雨林采集苔藓" },
                "pink" => new DyeInfo { Name = "樱花花瓣染剂", Source = "春季限定采集" },
                _ => new DyeInfo { Name = "未知染剂", Source = "???" }
            };
        }

        private string GetMaterialName(string itemId)
        {
            return itemId switch
            {
                "lace" => "蕾丝边", "ribbon" => "丝带", "pearl" => "珍珠扣",
                "gem" => "宝石", "glow" => "夜光海藻", "fire_scale" => "火鳞碎片",
                "dragon_scale" => "龙鳞", "golden_thread" => "金线",
                "phoenix_feather" => "凤凰羽", "feather" => "羽绒饰",
                "silk_thread" => "高级丝线", "frill" => "荷叶边",
                "boss_scale" => "海兽鳞片", _ => itemId
            };
        }
    }

    // 数据结构
    [System.Serializable]
    public class ClothingRecipe
    {
        public string InputText;
        public string OutputName;
        public string StyleName;
        public int TargetQuality = 1;
        public float FabricNeed = 3;
        public List<string> Colors = new();
        public List<AccessoryRequirement> Accessories = new();
        public List<CraftMaterial> Materials = new();
    }

    [System.Serializable]
    public class CraftMaterial
    {
        public string ItemId;
        public string Name;
        public int Amount;
        public int Quality;
    }

    [System.Serializable]
    public class AccessoryRequirement
    {
        public string ItemId;
        public int Amount;
        public int Quality;
    }

    [System.Serializable]
    public class StyleKeyword { public string Keyword; public string StyleName; public int FabricAmount; }
    [System.Serializable]
    public class ColorKeyword { public string Keyword; public string DyeId; }
    [System.Serializable]
    public class TierKeyword { public string Keyword; public int Quality; public string[] Accessories; }
    [System.Serializable]
    public class AccessoryKeyword { public string Keyword; public string ItemId; public int Amount; public int Quality; }
    [System.Serializable]
    public class CharacterPreset { public string CharacterName; public int Quality; public string StyleName; public string[] Colors; public string[] Accessories; }
    [System.Serializable]
    public class DyeInfo { public string Name; public string Source; }
}
