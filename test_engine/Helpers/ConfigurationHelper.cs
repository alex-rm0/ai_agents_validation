// Mantido apenas para compatibilidade com código legado.
// Para novos projetos, use FunctionalTests.Config.TestConfig.

using Microsoft.Extensions.Configuration;

namespace FunctionalTests.Helpers;

public static class ConfigurationHelper
{
    private static readonly IConfigurationRoot _config = new ConfigurationBuilder()
        .SetBasePath(AppContext.BaseDirectory)
        .AddJsonFile("appsettings.json", optional: false, reloadOnChange: false)
        .AddEnvironmentVariables()
        .Build();

    public static string GetBaseUrl() =>
        Environment.GetEnvironmentVariable("BASE_URL")
        ?? _config["BaseUrl"]
        ?? throw new InvalidOperationException("BaseUrl is not configured.");

    public static string GetLoginPath()
    {
        var value =
            Environment.GetEnvironmentVariable("LOGIN_PATH")
            ?? _config["LoginPath"]
            ?? "";

        Console.WriteLine($"[Config] LoginPath: '{value}'");

        return value;
    }

    public static string GetTestUser() =>
        Environment.GetEnvironmentVariable("TEST_USER")
        ?? _config["TestUser"]
        ?? throw new InvalidOperationException("TestUser is not configured.");

    public static string GetTestPassword() =>
        Environment.GetEnvironmentVariable("TEST_PASSWORD")
        ?? _config["TestPassword"]
        ?? throw new InvalidOperationException("TestPassword is not configured.");

    public static string GetUsernameSelector() =>
        Environment.GetEnvironmentVariable("USERNAME_SELECTOR")
        ?? _config["UsernameSelector"]
        ?? "input[type='text']";

    public static string GetPasswordSelector() =>
        Environment.GetEnvironmentVariable("PASSWORD_SELECTOR")
        ?? _config["PasswordSelector"]
        ?? "input[type='password']";

    public static string GetLoginButtonSelector() =>
        Environment.GetEnvironmentVariable("LOGIN_BUTTON_SELECTOR")
        ?? _config["LoginButtonSelector"]
        ?? "button[type='submit']";
}