using System;
using System.IO;
using System.Configuration;

class Program
{
    static void Main(string[] args)
    {
        string filePath = "path/to/your/file.ini";

        // 读取 INI 文件
        var config = ConfigurationManager.OpenExeConfiguration(ConfigurationUserLevel.None);
        var settings = config.AppSettings.Settings;

        if (File.Exists(filePath))
        {
            var lines = File.ReadAllLines(filePath);

            foreach (var line in lines)
            {
                if (line.StartsWith("prompt="))
                {
                    settings["prompt"] = line.Split('=')[1];
                }
                else if (line.StartsWith("model="))
                {
                    settings["model"] = line.Split('=')[1];
                }
                else if (line.StartsWith("BlockSplit="))
                {
                    settings["BlockSplit"] = line.Split('=')[1];
                }
            }

            // 修改值
            settings["prompt"].Value = "you are a superman";
            settings["model"].Value = "SparkPlus";
            settings["BlockSplit"].Value = "2";

            // 将修改后的配置写回文件
            File.WriteAllLines(filePath, new[]
            {
                $"prompt={settings["prompt"].Value}",
                $"model={settings["model"].Value}",
                $"BlockSplit={settings["BlockSplit"].Value}"
            });

            Console.WriteLine("INI 文件已成功修改。");
        }
        else
        {
            Console.WriteLine("文件不存在。");
        }
    }
}
