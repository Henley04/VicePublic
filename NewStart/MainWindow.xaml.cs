using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using System;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using System.Diagnostics;
using Microsoft.UI.Windowing;
using WinRT.Interop;
using Microsoft.UI;

namespace SetServerINI
{
    public partial class MainWindow : Window
    {
        private readonly string configFilePath;
        private IConfigurationRoot config;

        public MainWindow()
        {
            InitializeComponent();
            configFilePath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "EvoSphere", "Vice", "Config", "config.ini");
            LoadConfig();
            DisplayPublicIpAsync();
            SetWindowSize(800, 450); // Set the initial window size
        }

        private void LoadConfig()
        {
            Directory.CreateDirectory(Path.GetDirectoryName(configFilePath)); // Ensure the directory exists

            var builder = new ConfigurationBuilder()
                .SetBasePath(Path.GetDirectoryName(configFilePath))
                .AddIniFile(configFilePath, optional: true, reloadOnChange: true);

            config = builder.Build();

            AppIdTextBox.Text = config["Settings:Id"];
            AppSecretTextBox.Text = config["Settings:Secret"];
            PromptTextBox.Text = config["Settings:prompt"];
            SparkAuthTextBox.Text = config["Settings:SparkAuth"];
            ModelComboBox.SelectedItem = config["Settings:model"];
            IfBlockComboBox.SelectedItem = config["Settings:BlockSplit"] == "1" ? "是" : "否";
        }

        private async void DisplayPublicIpAsync()
        {
            string[] ipServices = new string[]
            {
                "https://api.ipify.org",
                "https://ifconfig.me/ip",
                "https://icanhazip.com/",
                "https://ident.me/",
                "https://checkip.amazonaws.com/"
            };

            foreach (var service in ipServices)
            {
                var ip = await GetPublicIpAsync(service);
                if (!string.IsNullOrEmpty(ip))
                {
                    IpTextBlock.Text = $"IP: {ip}";
                    break;
                }
            }
        }

        private async Task<string> GetPublicIpAsync(string url)
        {
            using var client = new HttpClient();
            try
            {
                var response = await client.GetStringAsync(url);
                return response.Trim();
            }
            catch
            {
                return null;
            }
        }

        private async void OnConfirmClick(object sender, RoutedEventArgs e)
        {
            var dialog = new ContentDialog
            {
                Title = "确认",
                Content = "你确定要提交吗？",
                PrimaryButtonText = "确定",
                CloseButtonText = "取消",
                XamlRoot = this.Content.XamlRoot // Set the XamlRoot property
            };

            var result = await dialog.ShowAsync();

            if (result == ContentDialogResult.Primary)
            {
                var builder = new ConfigurationBuilder()
                    .SetBasePath(Path.GetDirectoryName(configFilePath))
                    .AddIniFile(configFilePath, optional: true, reloadOnChange: true);

                config = builder.Build();

                var settings = config.GetSection("Settings");
                settings["Id"] = AppIdTextBox.Text;
                settings["Secret"] = AppSecretTextBox.Text;
                settings["prompt"] = PromptTextBox.Text;
                settings["SparkAuth"] = SparkAuthTextBox.Text;
                settings["model"] = ((ComboBoxItem)ModelComboBox.SelectedItem).Content.ToString();
                settings["BlockSplit"] = ((ComboBoxItem)IfBlockComboBox.SelectedItem).Content.ToString() == "是" ? "1" : "0";

                File.WriteAllText(configFilePath, config.GetDebugView());

                Process.Start(new ProcessStartInfo
                {
                    FileName = Path.Combine(Directory.GetCurrentDirectory(), "Public.exe"),
                    UseShellExecute = true
                });
            }
        }

        private void SetWindowSize(int width, int height)
        {
            IntPtr hwnd = WindowNative.GetWindowHandle(this);
            WindowId windowId = Win32Interop.GetWindowIdFromWindow(hwnd);
            AppWindow appWindow = AppWindow.GetFromWindowId(windowId);
            appWindow.Resize(new Windows.Graphics.SizeInt32(width, height));
        }

        private void About_Click(object sender, RoutedEventArgs e)
        {
            var AboutInfo = new ContentDialog
            {
                Title = "About",
                Content = "Copyright(C) EvoSphere Studio ",
                PrimaryButtonText = "确定",
                XamlRoot = this.Content.XamlRoot // Set the XamlRoot property
            };
        }
    }
}
