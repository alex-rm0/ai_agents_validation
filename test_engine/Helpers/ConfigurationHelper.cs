// Wrapper de compatibilidade — delega toda a lógica para TestConfig.
// Para novos projetos, usa FunctionalTests.Config.TestConfig directamente.

using FunctionalTests.Config;

namespace FunctionalTests.Helpers;

public static class ConfigurationHelper
{
    public static string GetBaseUrl() => TestConfig.BaseUrl;

    public static string GetLoginPath()
    {
        var value = TestConfig.LoginPath;
        Console.WriteLine($"[Config] LoginPath: '{value}'");
        return value;
    }

    public static string GetTestUser() => TestConfig.TestUser;

    public static string GetTestPassword() => TestConfig.TestPassword;

    public static string GetUsernameSelector() => TestConfig.UsernameSelector;

    public static string GetPasswordSelector() => TestConfig.PasswordSelector;

    public static string GetLoginButtonSelector() => TestConfig.LoginButtonSelector;
}